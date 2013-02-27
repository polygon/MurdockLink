'''
Created on Feb 14, 2013

@author: jan
'''

from collections import namedtuple

class Entries(object):
    JOYSTICK_CTRLS = 8
    GEAR_BRAKES = 14
    THROTTLE_COMMAND = 25

class PacketBuilder(object):
    pkg = []
    Entry = namedtuple('Entry', ['idx', 'values'])
    
    def __init__(self):
        pass
   
    def newpacket(self):
        self.pkg = []
       
    def addentry(self, entry):
        self.pkg.append(entry)
        
    def getpacket(self):
        return self.pkg
    
    def joystick_ctrls(self, elev=-999, ail=-999., rudd=-999.):
        return self.Entry(Entries.JOYSTICK_CTRLS, [elev, ail, rudd] + 5*[-999.])
    
    def gear_brakes(self, gear=-999., wbrake=-999., rbrake=-999., lbrake=-999.):
        return self.Entry(Entries.GEAR_BRAKES, [gear, wbrake, rbrake, lbrake] + 4*[-999.])
    
    def throttle_command(self, throttle=-999.):
        return self.Entry(Entries.THROTTLE_COMMAND, [throttle] + 7*[-999.])