'''
Created on Feb 27, 2013

@author: jan
'''
class Packet(object):
    _euler = [0., 0., 0.]
    _gyro = [0., 0., 0.]
    _accel = [0., 0., 0.]
    _magheading = 0.
    _pressure = 0.
    _height = 0.
    _airspeed = 0.
    _position = [0., 0.]
    
    def seteuler(self, yaw, pitch, roll):
        self._euler = [yaw, pitch, roll]
    
    def setgyro(self, yawrate, pitchrate, rollrate):
        self._gyro = [yawrate, pitchrate, rollrate]
        
    def setaccel(self, normal, axial, side):
        self._accel = [normal, axial, side]
        
    def setmagheading(self, magheading):
        self._magheading = magheading
        
    def setpressure(self, pressure):
        self._pressure = pressure
        
    def setheight(self, height):
        self._height = height
        
    def setairspeed(self, airspeed):
        self._airspeed = airspeed
        
    def setposition(self, latitude, longitude):
        self._position = [latitude, longitude]
                          
    def makepacket(self):
        out = ''
        out = out + 'yaw:%.4f,pitch:%.4f,roll:%.4f' % (self._euler[0], self._euler[1], self._euler[2])
        out = out + ',gyroyaw:%.4f,gyropitch:%.4f,gyroroll:%.4f' % (self._gyro[0], self._gyro[1], self._gyro[2])
        out = out + ',g_normal:%.4f,g_axial:%.4f,g_side:%.4f' % (self._accel[0], self._accel[1], self._accel[2])
        out = out + ',magheading:%.4f' % (self._magheading)
        out = out + ',pressure:%.4f' % (self._pressure)
        out = out + ',height:%.4f' % (self._height)
        out = out + ',airspeed:%.4f' % (self._airspeed)
        out = out + ',lat:%.4f,lon:%.4f' % (self._position[0], self._position[1])
        return out
    
class Controller(object):
    def __init__(self, sink):
        self.sink = sink
        
    def senddatapacket(self, packet):
        self.sink.writeline(packet.makepacket())