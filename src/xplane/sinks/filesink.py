'''
Created on Dec 30, 2012

@author: jan
'''

class FileSink(object):
    def __init__(self):
        pass
    
    def open(self, filename):
        if self.file is not None:
            self.close()
            
        self.file = open(filename, 'wb')
        
    def close(self):
        if self.file is not None:
            self.file.close()
            self.file = None
            
    def write(self, data):
        self.file.write(data)