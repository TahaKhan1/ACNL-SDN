from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from time import sleep
import _random
from random import shuffle


Nodes=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,14]
Links=[[1, 7], [1, 11], [1, 12], [2, 6], [2, 10], [3, 6], [3, 8], [3, 12], [4, 8], [4, 10],
        [5, 6], [5, 7], [5, 11], [6, 13], [7, 10], [9, 12], [9, 13],  [10, 11], [4,14], [14,9], [14,13]]

Quake_fail=[[1, 12], [3, 6], [3, 12], [4, 10], [4, 14], [7, 1], [8, 3], [8, 4]]

Src_Dst=[[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[1,13],[1,14],[2,3],[2,4],[2,5],
[2,6],[2,7],[2,8],[2,9],[2,10],[2,11],[2,12],[2,13],[2,14],[3,4],[3,5],[3,6],[3,7],[3,8],[3,9],[3,10],[3,11],[3,12],
[3,13],[3,14],[4,5],[4,6],[4,7],[4,8],[4,9],[4,10],[4,11],[4,12],[4,13],[4,14],[5,6],[5,7],[5,8],[5,9],[5,10],[5,11],[5,12],
[5,13],[5,14],[6,7],[6,8],[6,9],[6,10],[6,11],[6,12],[6,13],[6,14],[7,8],[7,9],[7,10],[7,11],[7,12],[7,13],[7,14],
[8,9],[8,10],[8,11],[8,12],[8,13],[8,14],[9,10],[9,11],[9,12],[9,13],[9,14],[10,11],[10,12],[10,13],[10,14],[11,12],[11,13],[11,14],[12,13],[12,14],[13,14]]       


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


    for link_pair in Links:
        net.addLink('s' + str(link_pair[0]), 's' + str(link_pair[1]))
        #print('s' + str(link_pair[0]), 's' + str(link_pair[1]), i)

    info('*** Starting network\n')
    net.start()
    for i in s:
        i.cmd('ovs-vsctl set bridge', i, 'protocols=OpenFlow13')


    info('*** Running CLI\n')
    CLI(net)

    link_range = list(range(0,8))

    shuffle(link_range)

    for i in range(0, 8):
        link_e = link_range[i]
        link = Quake_fail[link_e]
        net.configLinkStatus('s' + str(link[0]), 's' + str(link[1]), 'down')
        print('s' + str(link[0]),'s' + str(link[1]),"link down")
        sleep(5)

    info('*** Stopping network')
    #net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    emptyNet()



