from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
import time

class LinearTopo(Topo):
    def build(self):
        # Add 1 switch
        s1 = self.addSwitch('s1')

        # Add 2 hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        # Connect hosts to switch
        self.addLink(h1, s1)
        self.addLink(h2, s1)

def run():
    setLogLevel('info')
    topo = LinearTopo()
    net = Mininet(topo=topo, controller=RemoteController)
    net.start()

    print("\n=== Topology 1: Linear (1 switch, 2 hosts) ===")

    print("\n--- Ping Test ---")
    net.pingAll()

    h1, h2 = net.get('h1', 'h2')

    print("\n--- iperf Bandwidth Test: h1 to h2 ---")
    h2.cmd('iperf -s &')
    time.sleep(2)
    result = h1.cmd('iperf -c ' + h2.IP() + ' -t 5')
    print(result)

    print("\n--- Flow Table (s1) ---")
    print(net.get('s1').cmd('ovs-ofctl dump-flows s1'))

    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()
