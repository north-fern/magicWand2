#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import AnalogSensor, UARTDevice
import utime
import serial, string, math

def readFiles():
     datapoints = []
     
     southwest = open("sw.txt", "r")
     for line in southwest:
          line = line.split(",")
          newthing = [0,0,0,0,0,0]
          for i in range(6):
               newthing[i] = float(line[i])
          datapoints.append((newthing, 0))
     southwest.close()
     wait(500)
     
     southeast = open("se.txt", "r")
     for line in southeast:
          line = line.split(",")
          newthing = [0,0,0,0,0,0]
          for i in range(6):
               newthing[i] = float(line[i])
          datapoints.append((newthing, 1))
     southeast.close()
     wait(500)
     
     northwest = open("nw.txt", "r")
     for line in northwest:
          line = line.split(",")
          newthing = [0,0,0,0,0,0]
          for i in range(6):
               newthing[i] = float(line[i])
          datapoints.append((newthing, 2))
     northwest.close()
     wait(500)
     
     northeast = open("ne.txt", "r")
     for line in northeast:
          line = line.split(",")
          newthing = [0,0,0,0,0,0]
          for i in range(6):
               newthing[i] = float(line[i])
          datapoints.append((newthing, 3))
     northeast.close()
     wait(500)

     return datapoints

def kNN(datapoints, x, k):
     '''
     datapoints is training set, x is value we are comparing, k is number of nearest neighbors
     '''
     dist = []
     for data in datapoints:
          euc = 0
          for val in range(3):
               #print(data[0][val])
               euc += ((x[val] - data[0][val]))**2
          euc = (euc)**(1/2)
          dist.append((euc, data[1]))
     
     dist.sort()
     labelarray = [0,0,0,0]
     for i in range(k):
          label = dist[i][1]
          labelarray[label] += 1
     
     indx = 0
     curmax = 0
     print(labelarray)
     for i, val in enumerate(labelarray):
          if val > curmax:
               curmax = val
               indx = i
     return indx
          
          


# Write your program here
ev3 = EV3Brick()
ev3.speaker.beep()
button = TouchSensor(Port.S1)
filename = "HOLD"
datapoints = readFiles()
#print(datapoints[0])

f = open(filename + ".txt", "w")

s=serial.Serial("/dev/ttyACM0",9600)
#f.write("xaccel, yaccel, zaccel, xgyro, ygyro, zgyro\n")
trialnum = 0
ev3.speaker.say("READY!")
while True:
     justpressed = False
     avgMotion = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
     count = 0
     while button.pressed():
          wait(5)
          data=s.read(s.inWaiting()).decode("utf-8")
          #print('size = %d, buffer = %d' % (len(data),s.inWaiting()))
          data = data.splitlines()
          #print(data)
          wait(50)
          imu = data[-2].split(',')
          #data = float(imu)
          if len(imu) == 6:
               for i in range(6):
                    avgMotion[i] = avgMotion[i] + float(imu[i])
               count += 1
          
          justpressed = True
     
     if justpressed == True:
          for i in range(6):
               avgMotion[i] = (avgMotion[i] / count)
          
               #f.write(str(avgMotion[i]) + ", ")
          #trialnum += 1
          #print(trialnum)
               
          val = kNN(datapoints, avgMotion, 13)
          print(val)
          justpressed = False
          #f.write("\n")
          if val == 0:
               ev3.speaker.play_file('snare.wav')
          if val == 1:
               ev3.speaker.play_file('gong.wav')
          if val == 2:
               ev3.speaker.play_file('laser.wav')
          if val == 3:
               ev3.speaker.play_file('crash.wav')
     

     