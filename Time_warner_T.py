from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from time import sleep

'''
Nodes=[7, 16, 21, 25, 26, 27, 29, 30, 33, 40, 46, 48, 58]

print(len(Nodes))
Links=[[7,58],[7,33],
        [25, 26],[25, 27],
        [25, 30], [30, 40], [30,26],
       [30, 33], [27, 40],
       [27, 21],[16, 33],[29,30],[29,33],
       [16, 21],[21,26], [27, 48], [40, 46], [40, 33],
       [46, 58], [46,33],[58, 33]]
print(len(Links))

Links=[[1, 2], [1, 3], [3, 4], [3, 5], [6, 7], [6, 8], [4, 9], [10, 9], [10, 11], [5, 12], [5, 7], [5, 11],
       [5, 9], [5, 13], [9, 14], [9, 15], [9, 16], [9, 17], [15, 18], [19, 20], [19, 21], [19, 22], [23, 24],
       [23, 25], [25, 26], [25, 20], [25, 27], [28, 29], [28, 30], [29, 31], [29, 32], [29, 33], [29, 30],
       [29, 34], [35, 36], [35, 37], [37, 38], [37, 30], [38, 39], [39, 25], [25, 30], [30, 40], [30, 26],
       [30, 33], [30, 41], [30, 42], [30, 43], [30, 44], [45, 46], [45, 47], [45, 41], [45, 44], [27, 40],
       [27, 20], [27, 48], [27, 21], [48, 49], [48, 50], [32, 26], [41, 47], [16, 33], [16, 51], [16, 52],
       [16, 21], [49, 40], [22, 20], [53, 24], [53, 54], [24, 26], [43, 40], [31, 54], [42, 40], [40, 46],
       [40, 33], [40, 50], [55, 56], [55, 21], [34, 33], [51, 57], [51, 21], [56, 33], [21, 57], [21, 26],
       [21, 33], [21, 20], [54, 26], [36, 46], [7, 33], [7, 58], [12, 52], [12, 8], [13, 17], [46, 33],
       [46, 59], [46, 58], [59, 58], [58, 33], [33, 60], [33, 8], [8, 61], [8, 2], [52, 14], [52, 18],
       [52, 62], [62, 14], [14, 18], [60, 61]]
'''
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
    '''
    h = []
    for i in Nodes:
        host = 'h' + str(i)
        
        h.append(net.addHost(host))
    print("hhhhh", h[0])

    info('*** Adding Hosts Address\n')
    '''
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

    info('*** Starting network\n')
    net.start()
    for i in s:
        i.cmd('ovs-vsctl set bridge', i, 'protocols=OpenFlow13')

    info('*** Running CLI\n')
    CLI(net)
    # sleep(2)
    # net.pingAll()

    info('*** Stopping network')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    emptyNet()

