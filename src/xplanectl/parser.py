'''
Created on Feb 24, 2013

@author: jan
'''
'''
Created on Feb 14, 2013
'''

from collections import namedtuple
import threading
import struct

class Parser(object):

    thread = None
    lock = threading.Lock()
    stopping = False
    packet = None
    callback = None
    source = None
    
    
    def __init__(self, source, callback=None):
        self.source = source
        self.callback = callback
        
    def parsepacket(self, line):
        # Make sure this is a data package
        if line[:5] != "DATA@":
            return None
        
        # Calculate amount of Entries
        assert (len(line)-5) % 36 == 0, 'Invalid x-plane data packet'
        n_entries = (len(line) - 5) / 36
        data = struct.unpack('Iffffffff'*n_entries, line[5:])
        packet = {}
        for i in range(n_entries):
            packet[data[9*i]] = data[9*i+1:9*(i+1)]
        return packet
    
    def run(self):
        while self.stopping is False:
            data = self.source.read()
            packet = self.parsepacket(data)
            if packet is not None:
                with self.lock:
                    self.packet = packet
                if self.callback is not None:
                    self.callback(packet)

    def start(self):
        if self.thread is None:
            self.stopping = False
            self.thread = threading.Thread(target=self.run, name='XplaneParser')
            self.thread.start()
            
    def stop(self):
        if self.thread is not None:
            self.stopping = True
            self.thread.join()
            
    def packet(self):
        with self.lock:
            packet = self.packet
        return packet
