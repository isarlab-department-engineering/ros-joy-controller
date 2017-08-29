#!/usr/bin/env python

#
# This script allows control over a raspberry pi based robot
# reads Twist messages from the controller topic and decodes it
# to move the motors using Adafruit libraries
#
# script by Andrea Fioroni - andrifiore@gmail.com
# GitHub repo: https://github.com/isarlab-department-engineering/ros-joy-controller/tree/master
#

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import atexit
import time

class motor_driver:

    def __init__(self):

        # motor HAT setup
        self.mh = Adafruit_MotorHAT(addr=0x60) # setup Adafruit Motor HAT on 0x60 address

        # at exit code, to auto-disable motor on shutdown
        def turnOffMotors():
            self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
            self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	    atexit.register(turnOffMotors)

        # setup 2 motors
        self.mLeft = self.mh.getMotor(1) # left motor
        self.mRight = self.mh.getMotor(2) # right motor

        # speed vars
        self.leftSpeed = 0
        self.rightSpeed = 0
        # dir vars (1 = move forward, -1 = move backward)
        self.leftDir = 1
        self.rightDir = 1


        # distance between the two wheels of the robot (cm)
        self.WHEEL_DIST = 10 #TODO misure this param

        # wheel radius, not needed right now
        # but could be useful for a more accurate control
        # WHEEL_RADIUS = 2.5

        rospy.Subscriber("cmd_vel", Twist, self.callback) # subscribe to cmd_vel topic

    def callback(self,data):
        rospy.loginfo(rospy.get_caller_id() + " Incoming Twist Message")

        #msg = data.data # wrong, data already represents the whole twist message
        msg = data

        # converts angular + linear values from cmd_vel
        # to 2 speed values for the motors
        #
        # we only need two of the six available values
        # so input Twist message will always be:
        # [ L X X ] [ X X A ]
        # with L representing the linear x-axis velocity
        # A representing the angular z-axis velocity
        # and X are values we don't need here
        #
        # good kown values are L = 150 and A = 10 -> 30 ( +/- )
        # (-10 = turn left, 0 = go straight, 10 = turn right)
        # angular 30 and linear 150 will make the robot turn with
        # only one wheel, while the other motor will be at 0 speed

        # change this to change the curve arc
        # modelling the difference on the two speeds
        diffParam = 2.0

        velDiff = (self.WHEEL_DIST * msg.angular.z) / diffParam;
        if(msg.linear.x < 0): # moving backward
            velDiff = -velDiff # reverse the curve arc
        self.leftSpeed = (msg.linear.x + velDiff) #/ WHEEL_RADIUS
        self.rightSpeed = (msg.linear.x - velDiff) #/ WHEEL_RADIUS

        speedControl()

        setMotorSpeed()

    def speedControl():
        # check if l and r speed are in the -255 - 255 range
        # and set the direction vars, since Adafruit libraries
        # only allow us to set a positive speed value and then
        # to move the motors backward/forward

        if(self.leftSpeed >= 0):
            self.leftDir = 1
            if(self.leftSpeed > 255):
                self.leftSpeed = 255
        else:
            self.leftDir = -1
            self.leftSpeed = -self.leftSpeed
            if(self.leftSpeed > 255):
                self.leftSpeed = 255

        if(self.rightSpeed >= 0):
            self.rightDir = 1
            if(self.rightSpeed > 255):
                self.rightSpeed = 255
        else:
            self.rightDir = -1
            self.rightSpeed = -self.rightSpeed
            if(self.rightSpeed > 255):
                self.rightSpeed = 255


    def setMotorSpeed():
        self.mLeft.setSpeed(self.leftSpeed)
        self.mRight.setSpeed(self.rightSpeed)

        if(self.leftDir == 1): # move left motor forward
            self.mLeft.run(Adafruit_MotorHAT.FORWARD)
        else: # move left motor backward
            self.mLeft.run(Adafruit_MotorHAT.BACKWARD)

        if(self.rightDir == 1): # move right motor forward
            self.mRight.run(Adafruit_MotorHAT.FORWARD)
        else: # move right motor backward
            self.mRight.run(Adafruit_MotorHAT.BACKWARD)

def main(args):
    m_driver = motor_driver()
    rospy.init_node('ros_motor_driver', anonymous=True) # create a ros_motor_driver node

    try:
	    rospy.spin() # loop until shutdown
    except KeyboardInterrupt:
	    print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)

