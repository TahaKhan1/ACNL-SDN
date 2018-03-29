#!/usr/bin/python
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch , OVSSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf


Nodes=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61]

Links=[[0, 1], [0, 2], [2, 3], [2, 4], [5, 6], [5, 7], [3, 8], [9, 8], [9, 10], [4, 11], [4, 6], [4, 10], [4, 8], [4, 12], [8, 13], [8, 14], [8, 15], [8, 16], [14, 17], [18, 19], [18, 20], [18, 21], [22, 23], [22, 24], [24, 25], [24, 19], [24, 26], [27, 28], [27, 29], [28, 30], [28, 31], [28, 32], [28, 29], [28, 33], [34, 35], [34, 36], [36, 37], [36, 29], [37, 38], [38, 24], [24, 29], [29, 39], [29, 25], [29, 32], [29, 40], [29, 41], [29, 42], [29, 43], [44, 45], [44, 46], [44, 40], [44, 43], [26, 39], [26, 19], [26, 47], [26, 20], [47, 48], [47, 49], [31, 25], [40, 46], [15, 32], [15, 50], [15, 51], [15, 20], [48, 39], [21, 19], [52, 23], [52, 53], [23, 25], [42, 39], [30, 53], [41, 39], [39, 45], [39, 32], [39, 49], [54, 55], [54, 20], [33, 32], [50, 56], [50, 20], [55, 32], [20, 56], [20, 25], [20, 32], [20, 19], [53, 25], [35, 45], [6, 32], [6, 57], [11, 51], [11, 7], [12, 16], [45, 32], [45, 58], [45, 57], [58, 57], [57, 32], [32, 59], [32, 7], [7, 60], [7, 1], [51, 13], [51, 17], [51, 61], [61, 13], [13, 17], [59, 60]]

def emptyNet():
		net=Mininet(controller=Controller )
		info ('*** Adding Controller\n')
		net.addController('c0',controller=RemoteController,ip='127.0.0.1',port=6633)
				
		info( '*** Adding Hosts\n' )
		h1 = net.addHost('h1',ip='10.0.0.1',mac='00:00:00:00:00:01') 
		h2 = net.addHost('h2',ip='10.0.0.2',mac='00:00:00:00:00:02') 
		#h3 = net.addHost('h3',ip='10.0.0.3',mac='00:00:00:00:00:03')
		def emptyNet():

		"Create an empty network and add nodes to it."

		net = Mininet( controller=RemoteController )
		
		for node in Nodes:
			hostt'=
		
		

		info( '*** Adding hosts\n' )
		h=[]
		for i in range (0,HOSTS):
		      host= 'h'+str(i)
		      h.append(net.addHost(host))
		
		
		info( '*** Adding switch\n' )
		s=[]
		for j in range (0,SWITCH):
		     switch = 's'+str(j)
		     s.append(net.addSwitch(switch))
		
		info( '*** Creating links\n' )
		#for index in range (0,SWITCH):
		for index in range(0,HOSTS):
		    net.addLink(s[random.randint(0,SWITCH-1)],h[index])
		
		for k in range (0,SWITCH//MAXNODES):
		    for i in range(k*MAXNODES,(k*MAXNODES)+(MAXNODES-1)):

		        for j in range((i+1),(k*MAXNODES+MAXNODES)):

		            net.addLink(s[i],s[j])
        
        net.addLink(s[(k*MAXNODES)+MAXNODES],s[(k*MAXNODES)+(MAXNODES-1)])

    net.addLink(s[0],s[SWITCH-1])


    info( '*** Starting network\n')
    net.start()

    info( '*** Running CLI\n' )
    CLI( net )

    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()




