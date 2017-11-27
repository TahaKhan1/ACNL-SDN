#!/usr/bin/python3
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from array import array
SWITCH=7
HOST=3
def emptyNet():
		"Create an empty network and add nodes to it"
		net=Mininet(controller=Controller )
		info ('*** Adding Controller\n')
		net.addController('c0',controller=RemoteController,ip='127.0.0.1',port=6633)

		info( '*** Adding Hosts\n' )
		h=[]
		for i in range(0,HOST-1):
			host='h'+str(i)
			h.append(net.addHost(host))
		info( '*** Adding Switches\n' )
		s=[]
		for i in range(0,SWITCH-1):	
			switch='s'+str(i)
			s.append(net.addSwitch(switch))

	        
		info( '*** Adding Links\n' )
		for k in range (0, SWITCH-3):
		net.addLink(s[k],s[k+1])
		net.addLink(s[1],s[5])
		net.addLink(s[2],s[4])
		net.addLink(s[0],h[0])
		net.addLink(s[3],h[1])
		net.addLink(s[0],s[5])
		
    

		info ( '*** Starting Network\n' )
		net.start()
		s[0].cmd('ovs-vsctl set bridge s0 protocols=OpenFlow13')
		s[1].cmd('ovs-vsctl set bridge s1 protocols=OpenFlow13')
		s[2].cmd('ovs-vsctl set bridge s2 protocols=OpenFlow13')
		s[3].cmd('ovs-vsctl set bridge s3 protocols=OpenFlow13')
		s[4].cmd('ovs-vsctl set bridge s4 protocols=OpenFlow13')
    		s[5].cmd('ovs-vsctl set bridge s5 protocols=OpenFlow13')
			

		info ( '***Running CLI\n' )
		CLI(net)

		info ( '*** Stopping network\n' )
		net.stop()

if __name__=='__main__':
	setLogLevel('info')
	emptyNet()

	
			


		
		
