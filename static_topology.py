#!/usr/bin/python
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch , OVSSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf

def emptyNet():
		"Create an empty network and add nodes to it"
		net=Mininet(controller=Controller )
		info ('*** Adding Controller\n')
		net.addController('c0',controller=RemoteController,ip='127.0.0.1',port=6633)

		info( '*** Adding Hosts\n' )
		h1 = net.addHost('h1',ip='10.0.0.1',mac='00:00:00:00:00:01') 
		h2 = net.addHost('h2',ip='10.0.0.2',mac='00:00:00:00:00:02') 
		#h3 = net.addHost('h3',ip='10.0.0.3',mac='00:00:00:00:00:03')
	

		info( '*** Adding Switches\n' )
		s1 = net.addSwitch('s1')
		s2 = net.addSwitch('s2')
		s3 = net.addSwitch('s3')
		s4 = net.addSwitch('s4')
		s5 = net.addSwitch('s5')
		s6 = net.addSwitch('s6')
			
		info( '*** Add links\n')
		net.addLink(s1, s2)
		net.addLink(s2, s3)
		net.addLink(s3, s4)
		net.addLink(s4, s5)
		net.addLink(s5, s6)
		net.addLink(s6, s1)
		net.addLink(h1, s1)
		#net.addLink(s2, s6)
		#net.addLink(s3, s5)
		net.addLink(h2, s4)
		#net.addLink(h3, s5)
		
		info ( '*** Starting Network\n' )
		net.start()
		s1.cmd('ovs-vsctl set bridge s1 protocols=OpenFlow13')
		 #stp-enable=true')
		s2.cmd('ovs-vsctl set bridge s2 protocols=OpenFlow13')
		 #stp-enable=true')
		s3.cmd('ovs-vsctl set bridge s3 protocols=OpenFlow13')
		 #stp-enable=true')
		s4.cmd('ovs-vsctl set bridge s4 protocols=OpenFlow13')
		 #stp-enable=true')
		s5.cmd('ovs-vsctl set bridge s5 protocols=OpenFlow13')
		 #stp-enable=true')
		s6.cmd('ovs-vsctl set bridge s6 protocols=OpenFlow13')
		 #stp-enable=true')


		info ( '***Running CLI\n' )
		CLI(net)

		info ( '*** Stopping network\n' )
		net.stop()

if __name__=='__main__':
	setLogLevel('info')
	emptyNet()




