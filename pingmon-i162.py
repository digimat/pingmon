import pingmon

pmon=pingmon.PingMon('/var/log/pingmon.py')

pmon.addHost('192.168.139.1')
pmon.addHost('192.168.143.200')
pmon.addHost('192.168.143.220')
pmon.addHost('192.168.143.221')
pmon.addHost('192.168.143.222')

pmon.run()
