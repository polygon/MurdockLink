'''
Created on Feb 14, 2013

@author: jan
'''
# Connects Murdock to xplane and forwards throttle, elev, ail, rudd and gear inputs

from murdock.parser import Parser as MurdockParser
from murdock.sources.filesource import FileSource
from murdock.sinks.filesink import FileSink
from murdock.controller import Controller as MurdockController
from murdock.controller import Packet as MurdockPacket
from functools import partial
from xplane.controller import Controller as XplaneController
from xplane.packetbuilder import PacketBuilder
from xplane.sinks.udpsink import UdpSink
from xplane.sources.udpsource import UdpSource
from xplane.parser import Parser as XplaneParser

xplaneip = '10.0.0.234'
xplanetxport = 49000

xplanerxport = 49003

#infile = '/dev/ttyACM0'          # Linux
#infile = '/dev/cu.usbmodem1'     # OSX
infile = 'example.log'
delay = 0.0

outfile = 'rx.log'
#outfile = '/dev/ttyACM0'          # Linux
#outfile = '/dev/cu.usbmodem1'     # OSX



def murdock_to_xplane(mpacket, controller):
    print mpacket
    p = PacketBuilder()
    p.newpacket()
    p.addentry(p.joystick_ctrls(mpacket.elev, mpacket.ail, mpacket.rudd))
    p.addentry(p.throttle_command(mpacket.thr))
    controller.sendDataPacket(p.getpacket())
    
def xplane_to_murdock(xpacket, murdockctl, xplanectl):
    # Verify packet
    if set([3,4,7,16,17,20]).issubset(xpacket.keys()) is False:
        # Configure xplane outputs
        xplanectl.enable([3, 4, 7, 16, 17, 20])
        return
        
    # Build packet for Murdock
    p = MurdockPacket()
    p.setairspeed(xpacket[3][2])
    p.setaccel(xpacket[4][4], xpacket[4][5], xpacket[4][6])
    p.setpressure(xpacket[7][0])
    p.setgyro(xpacket[16][2], xpacket[16][0], xpacket[16][1])
    p.setmagheading(xpacket[17][3])
    p.seteuler(xpacket[17][2], xpacket[17][0], xpacket[17][1])
    p.setheight(xpacket[20][3])
    p.setposition(xpacket[20][0], xpacket[20][1])
    print p.makepacket()
    murdockctl.senddatapacket(p)
    
    
def main():
    # Initialize link from murdock to xplane
    xplanesink = UdpSink(xplaneip, xplanetxport)
    xplanesink.open()
    xctl = XplaneController(xplanesink)
    mp = MurdockParser(FileSource(infile, delay), partial(murdock_to_xplane, controller=xctl))
    mp.start()
    print "Setup of Murdock to Xplane link"
    
    # Initialize the link from xplane to murdock
    xplanesrc = UdpSource(xplanerxport)
    xplanesrc.open()
    mctl = MurdockController(FileSink(outfile))
    xp = XplaneParser(xplanesrc, partial(xplane_to_murdock, murdockctl=mctl, xplanectl=xctl))
    xp.start()
    print "Setup of Xplane to Murdock link"
    
    print "Press Ctrl+C to abort"
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
    
    
if __name__=='__main__':
    main()
