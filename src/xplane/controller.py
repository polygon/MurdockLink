'''
Created on Dec 30, 2012

@author: jan
'''

import struct

class Controller(object):
    def __init__(self, sink):
        self.sink = sink
        
    def sendDataPacket(self, packet):
        msg = 'DATA@'
        for entry in packet:
            msg += struct.pack('I', entry.idx)
            msg += struct.pack('ffffffff', *entry.values)
        self.sink.write(msg)
        
    def disableAll(self):
        msg = 'USEL@'
        msg += struct.pack('I'*132, *range(132))
        self.sink.write(msg)
        
    def enable(self, idxs):
        msg = 'DSEL@'
        msg += struct.pack('I'*len(idxs), *idxs)
        self.sink.write(msg)