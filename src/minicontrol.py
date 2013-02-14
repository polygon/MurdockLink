'''
Created on Feb 14, 2013

@author: jan
'''
# Connects Murdock to xplane and forwards throttle, elev, ail, rudd and gear inputs

from murdock_parser.parser import Parser
from murdock_parser.sources.filesource import FileSource
from functools import partial
from xplanectl.controller import Controller
from xplanectl.packetbuilder import PacketBuilder
from xplanectl.sinks.udpsink import UdpSink

ip = '127.0.0.1'
port = 40000
#infile = '/dev/ttyACM0'          # Linux
#infile = '/dev/cu.usbmodem1'     # OSX
infile = 'example.log'


def forward(packet, controller):
    print packet
    p = PacketBuilder()
    p.newpacket()
    p.addentry(p.joystick_ctrls(packet.elev, packet.ail, packet.rudd))
    p.addentry(p.throttle_command(packet.thr))
    controller.sendDataPacket(p.getpacket())
    
    
def main():
    target = UdpSink(ip, port)
    target.open()
    ctl = Controller(target)
    s = Parser(FileSource(infile), partial(forward, controller=ctl))
    s.run()
    
if __name__=='__main__':
    main()