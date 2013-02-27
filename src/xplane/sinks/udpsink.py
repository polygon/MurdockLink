'''
Created on Dec 30, 2012

@author: jan
'''

import socket

class UdpSink(object):
    sock = None
    
    def __init__(self, ip, port = 49001):
        self.ip = ip
        self.port = port
        
    def open(self):
        if self.sock is not None:
            self.close()
            
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((self.ip, self.port))
        
    def close(self):
        if self.sock is not None:
            self.sock.close()
            self.sock = None
            
    def write(self, data):
        self.sock.send(data)