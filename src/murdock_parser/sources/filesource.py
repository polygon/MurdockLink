'''
Created on Feb 14, 2013

@author: jan
'''

from time import sleep

class FileSourceSink(object):
    delay = 0.5
    file = None
    
    def __init__(self, filename, delay=0.5):
        self.delay = delay
        self.file = open(filename)
        
    def readline(self):
        sleep(self.delay)
        return self.file.readline()