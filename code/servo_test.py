from adafruit_servokit import ServoKit
from board import SDA, SCL
import busio
from adafruit_pca9685 import PCA9685
from time import sleep


# i2c = busio.i2c(SCL, SDA)

# pca = PCA9685(i2c)

# pca.frequency = 60

kit = ServoKit(channels=16)

# kit.servo[0].actuation_range = 360
kit.servo[0].set_pulse_width_range(500,2500)
kit.servo[1].set_pulse_width_range(500,2500)
kit.servo[2].set_pulse_width_range(500,2500)
kit.servo[3].set_pulse_width_range(500,2500)
# kit.servo[0].angle = 180
# kit.continuous_servo[0].throttle = 1

# kit.continuous_servo[0].throttle = -1
# sleep(2)
# kit.continuous_servo[0].throttle = 0

# kit.servo[0].angle = 0

def resetPattern():
    kit.servo[0].angle = 135
    kit.servo[4].angle = 135
    kit.servo[8].angle = 135
    kit.servo[12].angle = 135
    
def goDownPattern():
    kit.servo[0].angle = 155
    kit.servo[4].angle = 155
    kit.servo[8].angle = 155
    kit.servo[12].angle = 155
    
def pattern1():
    kit.servo[0].angle = 155
    kit.servo[4].angle = 142
    kit.servo[8].angle = 115
    kit.servo[12].angle = 140
    
def pattern2():
    kit.servo[0].angle = 142
    kit.servo[4].angle = 115
    kit.servo[8].angle = 128
    kit.servo[12].angle = 155
    
    
def pattern4():
    kit.servo[8].angle = 155
    kit.servo[0].angle = 115
    kit.servo[4].angle = 135
    kit.servo[12].angle = 145


while True:
    a0 = input("Enter 0: ")
    kit.servo[0].angle = int(a0)
    a1 = input("Enter 1: ")
    kit.servo[1].angle = int(a1)
    a2 = input("Enter 2: ")
    kit.servo[2].angle = int(a2)
    a3 = input("Enter 3: ")
    kit.servo[3].angle = int(a3)
    
    
    
    #tilt -y:
    # 0: down  most (increase ansgle) + 10
    # 1: up half (decrease angle) -5
    # 2: up most (decrease angle) -10
    # 3: down half (increase angle) + 5

# resetPattern()
# sleep(2)
# kit.servo[4].angle = 125
# kit.servo[8].angle = 125
# sleep(.05)  
# kit.servo[4].angle = 115
# sleep(.05)
# kit.servo[12].angle = 145
# kit.servo[0].angle = 145
# kit.servo[12].angle = 155
# sleep(2)


# count12 = 0
# count0=0
# count4=0
# count8=0
# while True:
#     if (count12 < 30):
#         kit.servo[12].angle = 155-count12
#         count12+=1
#         
#         
#     if (count0 < 10):
#         kit.servo[0].angle = 145+count0
#         count0+=1
#         
#     if (count4 < 30):
#         kit.servo[4].angle = 115+count4
#         count4+=1
#         
#     if (count8 < 10):
#         kit.servo[8].angle = 125-count8
#         count8+=1
#     
#     if count4>=30:
#         break

#pattern1()
# sleep(2)
# resetPattern()
# sleep(0.5)
#pattern2()
# goDownPattern()
# sleep(2)
# resetPattern()

