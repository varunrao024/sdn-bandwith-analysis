from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
import time

class TreeTopo(Topo):
    def build(self):
        # Add 3 switches
        s1 = self.addSwitch('s1')  # root switch
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Connect switches
        self.addLink(s1, s2)
        self.addLink(s1, s3)

        # Add 2 hosts per leaf switch
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        # Connect hosts to leaf switches
        self.addLink(h1, s2)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s3)

def run():
    setLogLevel('info')
    topo = TreeTopo()
    net = Mininet(topo=topo, controller=RemoteController)
    net.start()

    print("\n=== Topology 2: Tree (3 switches, 4 hosts) ===")

    print("\n--- Ping Test ---")
    net.pingAll()

    h1, h4 = net.get('h1', 'h4')

    print("\n--- iperf Bandwidth Test: h1 to h4 ---")
    h4.cmd('iperf -s &')
    time.sleep(2)
    result = h1.cmd('iperf -c ' + h4.IP() + ' -t 5')
    print(result)

    print("\n--- Flow Tables ---")
    for s in ['s1', 's2', 's3']:
        print(f"\nSwitch {s}:")
        print(net.get(s).cmd(f'ovs-ofctl dump-flows {s}'))

    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()
