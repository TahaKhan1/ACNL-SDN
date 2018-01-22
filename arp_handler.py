
# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
import logging
import struct
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER, CONFIG_DISPATCHER
from ryu.lib.packet import ipv4
from ryu.lib import mac
from ryu.lib.packet import arp

from ryu.topology import event, switches
from ryu.topology.api import get_switch, get_link
from ryu.controller import dpset
from ryu.lib import dpid
from ryu.controller import handler


class SimpleSwitch14(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = {'dpset': dpset.DPSet}

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch14, self).__init__(*args, **kwargs)
        self.topology_api_app = self
        self.mac_to_port = {}
        self.switch_port_table = {}
        self.link_to_port = {}
        self.interior_ports = {}
        self.dpid_port_set = set()
        self.ip_mac_table = {}
        self.ip_dpidport= {}
        self.datapath_list = {}
        self.datapaths= {}
    ######################################################################################
        self.flow_info = ['10.0.0.1','10.0.0.2']
        self.dpid_installed=[]
        self.inverse_dpid_installed=[]
        self.path_rule = {1:{'in_port':3, 'out_port':1},
				 2:{'in_port':3, 'out_port':1}}
				 #3:{'in_port':3, 'out_port':1}}
    #######################################################################################


    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        if datapath.id not in self.datapaths:
            self.logger.info("Registering datapath {}".format(datapath.id))
            self.datapaths[datapath.id]=datapath

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        dp = ev.datapath
        if ev.state == handler.MAIN_DISPATCHER:
            self.datapath_list[dp.id] = dp
            msg = 'Join SW'
        elif ev.state == handler.DEAD_DISPATCHER:
            ret = self.datapath_list.pop(dp.id, None)
            if ret is None:
                msg = 'Leave unknown SW'

            else:
                msg = 'Leave sw'
        self.logger.info('dpid {} {} '.format(msg, self.datapath_list))
        self.logger.info("port state change event triggered")

    def create_port_map(self, switch_list):
        """
            Create interior_port table and access_port table.
        """
        for sw in switch_list:
            dpid = sw.dp.id
            self.switch_port_table.setdefault(dpid, set())
            self.interior_ports.setdefault(dpid, set())

            for p in sw.ports:
                self.switch_port_table[dpid].add(p.port_no)
            self.logger.info('Switch_port_table :{}'.format(self.switch_port_table))

    def create_interior_links(self, link_list):
        """
            Get links`srouce port to dst port  from link_list,
            link_to_port:(src_dpid,dst_dpid)->(src_port,dst_port)
        """

        for link in link_list:
            src = link.src
            dst = link.dst
            self.link_to_port[(src.dpid, dst.dpid)] = (src.port_no, dst.port_no)

            # Find the access ports and interior ports
            if link.src.dpid in self.switches:
                self.interior_ports[link.src.dpid].add(link.src.port_no)
            if link.dst.dpid in self.switches:
                self.interior_ports[link.dst.dpid].add(link.dst.port_no)

        self.logger.info('Link_to_Port {}'.format(self.link_to_port))
        self.logger.info('Interior_Ports {}'.format(self.interior_ports))

    def create_access_ports(self):
        """
            Get ports without link into access_ports
        """
        self.dpid_port_set.clear()
        for sw in self.switch_port_table:
            all_port_table = self.switch_port_table[sw]
            interior_port = self.interior_ports[sw]
            for port in list(all_port_table - interior_port):
                self.logger.info('port:{}'.format(port))
                dpid_port_pair = (sw, port)
                self.dpid_port_set.add(dpid_port_pair)

        self.logger.info('Access_ports : {}'.format(self.dpid_port_set))

    events = [event.EventSwitchEnter,
              event.EventSwitchLeave]

    @set_ev_cls(events)
    def get_switches(self, ev):
        """
            Get topology info and store it.
        """
        switch_list = get_switch(self.topology_api_app, None)
        self.create_port_map(switch_list)
        self.switches = self.switch_port_table.keys()
        self.path_installer()

    @set_ev_cls(event.EventLinkAdd, event.EventLinkDelete)
    def get_links(self, ev):
        links = get_link(self.topology_api_app, None)
        self.create_interior_links(links)
        self.create_access_ports()
        self.logger.info("*********************************************************************************************")

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]

        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)

    def _build_packet_out(self, datapath, buffer_id, src_port, dst_port, data):
        """
            Build packet out object.
        """
        actions = []
        if dst_port:
            actions.append(datapath.ofproto_parser.OFPActionOutput(dst_port))

        msg_data = None
        if buffer_id == datapath.ofproto.OFP_NO_BUFFER:
            if data is None:
                return None
            msg_data = data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath, buffer_id=buffer_id,
            data=msg_data, in_port=src_port, actions=actions)
        return out

    def _register_host_entry(self, arp_src_ip, arp_src_mac, datapathID, port):
        self.ip_mac_table[arp_src_ip] = arp_src_mac
        dpid_port = (datapathID, port)
        self.ip_dpidport[arp_src_ip] = dpid_port

    def arp_forwarding(self, msg, arp_header, from_datapath, ether, ethernet_src, ethernet_dst,in_port):
        ofproto=from_datapath.ofproto
        arp_src_ip=arp_header.src_ip
        arp_dst_ip=arp_header.dst_ip
        arp_src_mac=arp_header.src_mac
        arp_dst_mac=arp_header.dst_mac


        if ethernet_dst == mac.BROADCAST_STR:  # Handle ARP broadcast
            #self.logger.info('This is ARP broadcast received at port {} of switch {} from IP {}, ARP Src Mac {}, ethernet src {} to IP {}, ARP Destn Mac {}, ethernet dst {}'.format(in_port, from_datapath.id,
                              #arp_src_ip, arp_src_mac, ethernet_src, arp_dst_ip, arp_dst_mac, ethernet_dst))

            if self.ip_mac_table.get(arp_src_ip)==None : # No src ip found, so storing it in the table
                self.logger.info("****No mac entry found for IP. adding entry.....****")
                self._register_host_entry(arp_src_ip, arp_src_mac,from_datapath.id, in_port)


            if self.ip_mac_table.get(arp_dst_ip)!= None: #dst_ip exist in ip_mac_table, so proxy it
                ARP_Reply = packet.Packet()
                mac_from_table=self.ip_mac_table.get(arp_dst_ip)
                ARP_Reply.add_protocol(ethernet.ethernet(ethertype=ether.ethertype, dst=ethernet_src, src=mac_from_table))
                ARP_Reply.add_protocol(arp.arp(opcode=arp.ARP_REPLY, src_mac=mac_from_table, src_ip=arp_dst_ip,
                                                dst_mac=arp_src_mac, dst_ip=arp_src_ip))
                ARP_Reply.serialize()
                from_datapath.send_msg(self._build_packet_out(from_datapath, ofproto.OFP_NO_BUFFER, ofproto.OFPP_CONTROLLER,
                                                          in_port, ARP_Reply.data))
                self.logger.info("****Found mac entry for IP. Proxy-ing****")

            else: #no dst_ip in ip_mac_table, flood
                for dpid_port_tup in self.dpid_port_set:
                    if dpid_port_tup not in self.ip_dpidport.values():
                        self.logger.info("********Flooding {}***********".format(dpid_port_tup))
                        datapath= self.datapath_list[dpid_port_tup[0]]
                        datapath.send_msg(self._build_packet_out(datapath,ofproto.OFP_NO_BUFFER,
                                                ofproto.OFPP_CONTROLLER, dpid_port_tup[1], msg.data))

        else: # if ARP packet and its a reply
            #self.logger.info('This is ARP reply received at port {} of switch {} from IP {}, ARP Src Mac {}, ethernet src {} to IP {}, ARP Destn Mac {}, ethernet dst {}'.format(
                              #in_port, from_datapath.id, arp_src_ip, arp_src_mac, ethernet_src, arp_dst_ip, arp_dst_mac, ethernet_dst))
            self._register_host_entry(arp_src_ip, arp_src_mac, from_datapath.id, in_port)
            dpid_inport=self.ip_dpidport.get(arp_dst_ip)
            datapath = self.datapath_list[dpid_inport[0]]
            datapath.send_msg(self._build_packet_out(datapath, ofproto.OFP_NO_BUFFER,
                                                 ofproto.OFPP_CONTROLLER, dpid_inport[1], msg.data))

        self.logger.info("*********************************************************************************************")
        return
      ##############################################Path_installer##############################################################
    
    def _send_flow_mod(self,datapath,flow_info,in_port, out_port):
      self.logger.info('flow_mod message called')
      ofproto=datapath.ofproto
      parser=datapath.ofproto_parser
      actions=[]
      actions.append(parser.OFPActionOutput(out_port))
      match=parser.OFPMatch(in_port=in_port, eth_type=0x800, ipv4_src=flow_info[0],ipv4_dst=flow_info[1])
      
      inst=[parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
      mod=parser.OFPFlowMod(datapath=datapath, priority=1,match=match,instructions=inst)
      self.logger.info('mod {}'.format(mod))
      datapath.send_msg(mod)
      return
    def path_installer(self):
      invert_flow_info = (self.flow_info[1], self.flow_info[0])
      for dp in self.path_rule.keys():
          if dp not in self.dpid_installed:
              self._send_flow_mod(self.datapaths[dp],self.flow_info,self.path_rule[dp]['in_port'], self.path_rule[dp]['out_port'])
              self.dpid_installed.append(dp)
              self._send_flow_mod(self.datapaths[dp],self.flow_info,self.path_rule[dp]['out_port'], self.path_rule[dp]['in_port'])
              #self.logger.info('the flow-rule is installed for the path_rule for dpid: {}'.format(dp))
          else:
              self.logger.info('the flow_rule is already installed for dpid: {}'.format(dp))
        
      #installing the the reverse route...
      for dp in self.path_rule.keys():
          if dp not in self.inverse_dpid_installed:
              self._send_flow_mod(self.datapaths[dp],self.invert_flow_info, self.path_rule[dp]['out_port'], self.path_rule[dp]['in_port'])
              self.inverse_dpid_installed.append(dp)
              self._send_flow_mod(self.datapaths[dp],self.invert_flow_info,self.path_rule[dp]['in_port'], self.path_rule[dp]['out_port'])
              #self.logger.info('the flow-rule is installed for the reverse route of the path_rule for dpid: {}'.format(dp))
      
          else:
              self.logger.info(' the (reverse) rule is already installed for dpid:{}'.format(dp))
    
  ######################################End of path_installer###########################################################
    #Handle packetin
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        in_port = msg.match['in_port']
        datapath = msg.datapath
        pkt = packet.Packet(msg.data)
        parser = datapath.ofproto_parser
        ethernet_header = pkt.get_protocol(ethernet.ethernet)
        ethernet_dst = ethernet_header.dst
        ethernet_src = ethernet_header.src
        arp_header = pkt.get_protocol(arp.arp)

        if ethernet_header.ethertype == ether_types.ETH_TYPE_LLDP:  # ignore lldp packet
            return

        if ethernet_dst[:5] == "33:33":  # ignore IPV6 multicast packet
            match = parser.OFPMatch(in_port=in_port, eth_dst=ethernet_dst)
            actions = []
            self.add_flow(datapath, 1, match, actions)
            return

        self.logger.info("packet in {} {} {} {}".format(datapath.id, ethernet_src, ethernet_dst, in_port))

        if arp_header: #handle arp packets
            self.logger.info("******ARP Processing********")
            self.arp_forwarding(msg, arp_header, datapath, ethernet_header, ethernet_src, ethernet_dst, in_port)

        return










