# tello_binom base library extention for feedback 
# for Tello EDU KIT

import os
import serial.tools.list_ports
import time
# ports list
ports = list(serial.tools.list_ports.comports())

for p in ports: 
    if "Serial" in str(p):
        port_name = str(p)[:4] 
# port definition
ser = serial.Serial(port_name)
ser.baudrate = 115200

# DIOD1
def L1_red():
    '''Turns the lamp 1 red light on'''
    L1_off()
    ser.write(bytes('L1=1', 'utf-8'))
    
def L1_green():
    '''Turns the lamp 1 green light on'''
    L1_off()
    ser.write(bytes('L2=1', 'utf-8'))
    
def L1_yellow():
    '''Turns the lamp 1 yellow (red+green) light on'''
    ser.write(bytes('L1=1', 'utf-8'))
    ser.write(bytes('L2=1', 'utf-8'))
    
def L1_off():
    '''Turns the lamp 1 light off'''
    ser.write(bytes('L1=0', 'utf-8'))
    ser.write(bytes('L2=0', 'utf-8'))
    
# DIOD2
def L2_red():
    '''Turns the lamp 2 red light on'''
    L2_off()
    ser.write(bytes('L4=1', 'utf-8'))
    
def L2_green():
    '''Turns the lamp 2 green light on'''
    L2_off()
    ser.write(bytes('L3=1', 'utf-8'))
    
def L2_yellow():
    '''Turns the lamp 2 yellow (red+green) light on'''
    ser.write(bytes('L3=1', 'utf-8'))
    ser.write(bytes('L4=1', 'utf-8'))
    
def L2_off():
    '''Turns the lamp 2 light off'''
    ser.write(bytes('L3=0', 'utf-8'))
    ser.write(bytes('L4=0', 'utf-8'))    
    
# DIOD3
def L3_red():
    '''Turns the lamp 3 red light on'''
    L3_off()
    ser.write(bytes('L6=1', 'utf-8'))
    
def L3_green():
    '''Turns the lamp 3 green light on'''
    L3_off()
    ser.write(bytes('L5=1', 'utf-8'))
    
def L3_yellow():
    '''Turns the lamp 3 yellow (red+green) light on'''
    ser.write(bytes('L5=1', 'utf-8'))
    ser.write(bytes('L6=1', 'utf-8'))
    
def L3_off():
    '''Turns the lamp 3 light off'''
    ser.write(bytes('L5=0', 'utf-8'))
    ser.write(bytes('L6=0', 'utf-8'))    

# DIOD4
def L4_red():
    '''Turns the lamp 4 red light on'''
    L4_off()
    ser.write(bytes('L7=1', 'utf-8'))

def L4_green():
    '''Turns the lamp 4 green light on'''
    L4_off()
    ser.write(bytes('L8=1', 'utf-8'))

def L4_yellow():
    '''Turns the lamp 4 yellow (red+green) light on'''
    ser.write(bytes('L7=1', 'utf-8'))
    ser.write(bytes('L8=1', 'utf-8'))
    
def L4_off():
    '''Turns the lamp 4 light off'''
    ser.write(bytes('L7=0', 'utf-8'))
    ser.write(bytes('L8=0', 'utf-8')) 

# DIOD5
def L5_red():
    '''Turns the lamp 5 red light on'''
    L5_off()
    ser.write(bytes('L9=1', 'utf-8'))

def L5_green():
    '''Turns the lamp 5 green light on'''
    L5_off()
    ser.write(bytes('L0=1', 'utf-8'))

def L5_yellow():
    '''Turns the lamp 5 yellow (red+green) light on'''
    ser.write(bytes('L9=1', 'utf-8'))
    ser.write(bytes('L0=1', 'utf-8'))
    
def L5_off():
    '''Turns the lamp 5 light off'''
    ser.write(bytes('L9=0', 'utf-8'))
    ser.write(bytes('L0=0', 'utf-8')) 

# laser pointer
def laser_on():
    '''Turns the laser pointer on'''
    ser.write(bytes('LL=1', 'utf-8'))

def laser_off():
    '''Turns the laser pointer off'''
    ser.write(bytes('LL=0', 'utf-8'))

# beeper    
def beep_on():
    '''Turns the beeper on'''
    ser.write(bytes('BP=1', 'utf-8'))

def beep_off():
    '''Turns the laser pointer off'''
    ser.write(bytes('BP=0', 'utf-8'))
    
def reset_all():
    '''Turns all the feedback off'''
    L1_off()
    L2_off()
    L3_off()
    L4_off()
    L5_off()    
    laser_off()
    beep_off()
    