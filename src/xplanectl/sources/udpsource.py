'''
Created on Feb 24, 2013

@author: jan
'''

import socket

class UdpSource(object):
    sock = None
    
    def __init__(self, port = 49003):
        self.port = port
        
    def open(self):
        if self.sock is not None:
            self.close()
            
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', self.port))
        
    def close(self):
        if self.sock is not None:
            self.sock.close()
            self.sock = None
            
    def read(self):
        return self.sock.recv(32768)