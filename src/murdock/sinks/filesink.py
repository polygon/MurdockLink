'''
Created on Feb 27, 2013

@author: jan
'''

from time import sleep

class FileSink(object):
    file = None
    
    def __init__(self, filename):
        self.file = open(filename, 'w')
        
    def writeline(self, packet):
        self.file.write(packet + '\n')
