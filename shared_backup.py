from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.ofproto import ofproto_v1_3
from ryu.lib import mac
import arp_tweaked
import logging
import shared_arpbackup


class Backup_Paths():
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    # _CONTEXTS = {'dpset': dpset.DPSet}

    def __init__(self, msg, link_ids, datapath_list):
        # super(Backup_Paths, self).__init__(*args, **kwargs)
        self.primary_flows = {1: (datapath_list[1], '10.0.0.1', '10.0.0.2', 3, 1),
                              2: (datapath_list[1], '10.0.0.2', '10.0.0.1', 1, 3),
                              3: (datapath_list[2], '10.0.0.1', '10.0.0.2', 1, 2),
                              4: (datapath_list[2], '10.0.0.2', '10.0.0.1', 2, 1),
                              5: (datapath_list[3], '10.0.0.1', '10.0.0.2', 1, 2),
                              6: (datapath_list[3], '10.0.0.2', '10.0.0.1', 2, 1),
                              7: (datapath_list[4], '10.0.0.1', '10.0.0.2', 1, 3),
                              8: (datapath_list[4], '10.0.0.2', '10.0.0.1', 3, 1),
                              9: (datapath_list[1], '10.0.0.1', '10.0.0.2', 3, 1),
                              10: (datapath_list[1], '10.0.0.2', '10.0.0.1', 1, 3),
                              11: (datapath_list[2], '10.0.0.1', '10.0.0.2', 1, 2),
                              12: (datapath_list[2], '10.0.0.2', '10.0.0.1', 2, 1),
                              13: (datapath_list[3], '10.0.0.1', '10.0.0.2', 1, 3),
                              14: (datapath_list[3], '10.0.0.2', '10.0.0.1', 3, 1),
                              15: (datapath_list[5], '10.0.0.1', '10.0.0.2', 3, 1),
                              16: (datapath_list[5], '10.0.0.2', '10.0.0.1', 1, 3),
			      17: (datapath_list[4], '10.0.0.1', '10.0.0.2', 2, 3),
                              18: (datapath_list[4], '10.0.0.2', '10.0.0.1', 3, 2),

                              }

        ##self.paths= {path_id:[flow_ID's]}
        ### Paths_ID's Identifies the different paths from source to destination.

        self.paths = {1: [1, 3, 5, 7],
                      2: [2, 4, 6, 8],
                      3: [9, 11, 13, 15,17],
                      4: [10, 12, 14, 16, 18]
                      }
        # Update dict - change the values to just path IDs
        ## links: paths associated with it.
        self.link_fail_map = {
              1: [1,3],
              2: [2,4],
              3: [],
              4: [4],
              5: [],
              6: [3],
              7: [2,4],
              8: [],
              9: [],
              10: [1,3],
              11: [2],
              12: [],
              13: [3],
              14: [1],
              15: [],
              16: [4]
          }

        # update this to just have path ID key and value only
        self.backup_path_map = {1: 3,
                                3: 1,
                                2: 4,
                                4: 2}
        self.msg = msg
        self.link_ids = link_ids
        self.failed_paths = []
        self.backup_paths = []
        self.backup_ID = []
        self.flows_failed = []
        self.backup_flows = {}
        self.failed_flows = {}
        self.link_failed = {}
        self.backup_path_list = []
        self.failed_links = []
        self.path_failed_list = []

        # flows[0] = self.paths[self.failed_paths[0]]

    def identify_failed_link(self):
        # list of path IDs affected
        dpid = []
        port_no = []
        for i in self.msg.values():
            dpid.append(int(i['dpid']))
            port_no.append(int(i['port_no']))
        print(dpid)
        print(port_no)
        for i in range(1):
            self.link_failed[i + 1] = (dpid[0], dpid[1], port_no[0], port_no[1])
        print(self.link_failed)
        # link_ids = {1: (1, '2', '3', '4'), 2: ('2', '3', '6', '7'), 3: ('4', '7', '8', '9')}
        # fail_map = {1: (1, '2', '3', '4')}
        for i in self.link_failed.values():
            if i in self.link_ids.values():
                print("Affected Links tuple:{}".format(i))
                for key, value in self.link_ids.items():
                    if i == value:
                        self.failed_links.append(key)
                        self.failed_paths.append(self.link_fail_map[key])
        print("Link_ID affected and appending to failed_link:{}".format(self.failed_links))
        print("Path failed IDs and appending to failed_paths:{}".format(self.failed_paths))

        ## Finding the paths affected using link_fail_map

        # pass

    def find_backup_paths(self):
        # iterate failed paths
        for i in self.failed_paths[0]:
            self.backup_ID.append(self.backup_path_map[i])
            print("Back_Up Paths:{}".format(self.backup_ID))

            # look at backup path dict's
            # and create list of backup paths
        # pass

    def backup_flow_rule_IDs(self):
        # iterate backup paths
        for i in self.backup_ID:
            self.backup_paths.append(self.paths[i])

        for i in self.backup_paths[0]:
            self.backup_flows[i] = self.primary_flows[i]
        print("Backup Paths dict: {}".format(self.backup_flows))
        print("Backup Paths : {}".format(self.backup_paths))
        ## Backup_Flows keys are flow ID's we got from paths
        ## and its value is tuple - datapath_list[],src,dst,in_p,out_p

        # looks at paths dict for flows for each backup path
        # store it as a dict whose keys are backup paths
        # pass

    def failed_flow_rule_IDs(self):
        for i in self.failed_paths[0]:
            self.path_failed_list.append(self.paths[i])
        print("Paths Failed List: {}".format(self.path_failed_list))
        for i in self.path_failed_list[0]:
            self.failed_flows[i] = self.primary_flows[i]
        print("Failed Flow ID's: {}".format(self.failed_flows))
        # iterate backup paths
        # looks at paths dict for flows for each backup path
        # store it as a dict whose keys are backup paths
        # pass

    def delete_flows_failed_paths(self):
        for i in self.failed_flows.values():
            print('Failed flow_mod message called')
            ofproto = i[0].ofproto
            parser = i[0].ofproto_parser
            actions = []
            actions.append(parser.OFPActionOutput(i[4]))
            match = parser.OFPMatch(in_port=i[3], eth_type=0x0800, ipv4_src=i[1], ipv4_dst=i[2])
            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
            mod = parser.OFPFlowMod(datapath=i[0], priority=1, match=match, instructions=inst,
                             out_group=ofproto.OFPG_ANY,out_port=ofproto.OFPP_ANY,command=ofproto.OFPFC_DELETE_STRICT)
            i[0].send_msg(mod)

        '''identify_failed_link()
        failed_flow_rule_paths()'''

    def add_flows_backup_paths(self):
        for i in self.backup_flows.values():
            print('Backup_Flows getting Installed')
            ofproto = i[0].ofproto
            parser = i[0].ofproto_parser
            actions = []
            actions.append(parser.OFPActionOutput(i[4]))
            match = parser.OFPMatch(in_port=i[3], eth_type=0x0800, ipv4_src=i[1], ipv4_dst=i[2])
            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
            mod = parser.OFPFlowMod(datapath=i[0], priority=1, match=match, instructions=inst)
            i[0].send_msg(mod)

        '''identify_failed_link()
        find_backup_paths()
        backup_flow_rule_IDs()'''







