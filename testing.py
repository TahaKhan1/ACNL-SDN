from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from time import sleep


## NSF Topology with one node less
Nodes=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,14]
Links=[[1, 7], [1, 11], [1, 12], [2, 6], [2, 10], [3, 6], [3, 8], [3, 12], [4, 8], [4, 10],
        [5, 6], [5, 7], [5, 11], [6, 13], [7, 10], [9, 12], [9, 13],  [10, 11], [4,14], [14,9], [14,13]]


def emptyNet():
    "Create an empty network and add nodes to it."

    net = Mininet(controller=RemoteController)

    info('*** Adding controller\n')
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    info('*** Adding hosts\n')

    h = []
    for i in Nodes:
        host = 'h' + str(i)
        a = list(host)
        if len(a)>2:
            j = a[1] + a[2]
            h.append(net.addHost(host,ip='10.0.0.%s' % j, mac='00:00:00:00:00:0%s' % j))
        else:
            j=a[1]
            h.append(net.addHost(host,ip='10.0.0.%s' % j, mac='00:00:00:00:00:0%s' % j))
    print("hhhhh",h)


    info('*** Adding switch\n')
    s = []
    for j in Nodes:
        switch = 's' + str(j)
        s.append(net.addSwitch(switch))
        """print(s)"""

    info('*** Creating links\n')
    ## One host at each switch
    for index in range(0, len(Nodes)):
        net.addLink(s[index], h[index])

    i = 0;
    for link_pair in Links:
        i = i + 1;
        net.addLink('s' + str(link_pair[0]), 's' + str(link_pair[1]))
        #print('s' + str(link_pair[0]), 's' + str(link_pair[1]), i)
    
    def failure(Links):
    	for i in Links:
			#sleep(20)
			print("Link Down")
			net.configLinkStatus('s' + str(link_pair[0]), 's' + str(link_pair[1]),'down')
			#sleep(5)   
     

    info('*** Starting network\n')
    net.start()
    for i in s:
        i.cmd('ovs-vsctl set bridge', i, 'protocols=OpenFlow13')

    info('*** Running CLI\n')
    CLI(net)    
    #sleep(5)
    failure(Links)     
    #for i in Links:
    	#sleep(20)
    	#print("Link Down")
    	#net.configLinkStatus('s' + str(link_pair[0]), 's' + str(link_pair[1]),'down')
    	#sleep(5)
    	#net.pingAll()
    	
    info('*** Stopping network')
    #net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    emptyNet()

