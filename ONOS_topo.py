#!/usr/bin/python


"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from array import array
import random
SWITCH= 19
HOSTS=10
MAXNODES=3

def emptyNet():

    "Create an empty network and add nodes to it."

    net = Mininet( controller=RemoteController )

    info( '*** Adding controller\n' )
    net.addController ('c0',controller=RemoteController,ip='172.17.0.2',port=6633)

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

    #for l in range (k*MAXNODES+MAXNODES-1,SWITCH-1):
    	#for m in range (l+1, SWITCH):
    		#net.addLink(s[l],s[m])
                
    info( '*** Starting network\n')
    net.start()

    info( '*** Running CLI\n' )
    CLI( net )

    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()
