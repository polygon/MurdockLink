'''
Created on Feb 14, 2013

@author: jan
'''
'''
Created on Feb 14, 2013

@author: jan
'''

from collections import namedtuple
import re
import threading

class Parser(object):
    Packet = namedtuple('Packet', ['time', 'thr', 'ail', 'elev', 'rudd', 'gear'])
    thread = None
    lock = threading.Lock()
    stopping = False
    packet = None
    callback = None
    source = None
    
    
    def __init__(self, source, callback=None):
        self.source = source
        self.callback = callback
        
    def parseline(self, line):
        res = re.search('\[\s*([0-9]+.[0-9]+)\] thr:([0-9-.]+) ail:([0-9-.]+) elev:([0-9-.]+) rudd:([0-9-.]+) gear:([0-9-.]+)', line)
        if res is None:
            return None
        else:
            return self.Packet(*map(float, res.groups())) 
    
    def run(self):
        while self.stopping is False:
            line = self.source.readline()
            if line is not None:
                packet = self.parseline(line)
                if packet is not None:
                    with self.lock:
                        self.packet = packet
                    if self.callback is not None:
                        self.callback(packet)
                    
    def start(self):
        if self.thread is None:
            self.stopping = False
            self.thread = threading.Thread(target=self.run, name='MurdockParser')
            self.thread.start()
            
    def stop(self):
        if self.thread is not None:
            self.stopping = True
            self.thread.join()
            
    def packet(self):
        with self.lock:
            packet = self.packet
        return packet