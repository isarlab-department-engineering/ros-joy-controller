#!/usr/bin/env python

#
# This script allows control over a raspberry pi based robot
# reads strings from rospibot_network topic and decodes it
# to control the motors using Adafruit libraries and the 
# motor_hat ROS Node (which takes a Int16MultiArray as input)
#
# script by Andrea Fioroni - andrifiore@gmail.com
# GitHub repo: https://github.com/isarlab-department-engineering/ros-joy-controller
#

import rospy,sys,time,atexit
from std_msgs.msg import String
from std_msgs.msg import Int16MultiArray

class rospibot_network:

    def __init__(self):

	# semaphore variable
	self.semaphore = 0
	
	# motor speed variables
	self.m1_speed = -150
	self.m2_speed = -133
    
	self.controlPub = rospy.Publisher("cmd", Int16MultiArray, queue_size=10) # publish on motor_hat's cmd topic
	self.controlInfoPub = rospy.Publisher("cmdinfo", String, queue_size=10) # publish info about control 

	rospy.Subscriber("line_detection_topic", Int16MultiArray, self.callback2)
	rospy.Subscriber("ros_joy_controller", String, self.callback1) # subscribe to ros_joy_controller topic
        rospy.Subscriber("traffic_light_detection", String, self.callback0) # subscribe to traffic_light_detection topic
	rospy.loginfo("Listening on two different topics")

    def callback0(self,data): # runs whenever any data is published on the traffic_light_detection topic
        rospy.loginfo(rospy.get_caller_id() + " Getting Traffic Light Info: %s", data.data)
        input = data.data # input received (will always be a string)

	def send(values):
            values = [-v for v in values]
            msg = Int16MultiArray()
            msg.data = values
            self.controlPub.publish(msg)

	if input == "GGG":
	    self.semaphore = 0
	elif input == "RRR":
	    self.semaphore = 1
	    send([0,0,0,0])

    def callback1(self,data): # runs whenever any data is published on the ros_joy_controller topic
        rospy.loginfo(rospy.get_caller_id() + " Getting User Input Info: %s", data.data)
        dir_str = data.data # input received (will always be a string)

	return 

	def send(values):
            values = [-v for v in values]
            msg = Int16MultiArray()
            msg.data = values
            self.controlPub.publish(msg)

	if(self.semaphore == 1):
            # red semaphore => stop the robot
            send([0,0,0,0])
        else:
            if dir_str == "w" :     # w = move forward
    	        send([self.m1_speed,self.m2_speed,0,0])
    	        rospy.loginfo(" - Move Forward")
		self.controlInfoPub.publish("forward")
            elif dir_str == "a" :   # a = turn left
                send([0,self.m2_speed,0,0])
    	        rospy.loginfo(" - Turn Left")
		self.controlInfoPub.publish("left")
            elif dir_str == "s" :   # s = move backward
                send([-self.m1_speed,-self.m2_speed,0,0])
    	        rospy.loginfo(" - Move Backward")
		self.controlInfoPub.publish("backward")
            elif dir_str == "d" :   # d = turn right
                send([self.m1_speed,0,0,0])
    	        rospy.loginfo(" - Turn Right")
		self.controlInfoPub.publish("right")
            elif dir_str == "x" :   # x = stop
    	        send([0,0,0,0])
    	        rospy.loginfo(" - Stop")
		self.controlInfoPub.publish("stop")

    def callback2(self,data):
	if self.semaphore == 0 :
	    self.controlPub.publish(data)


def main(args):
    rospi_net = rospibot_network()
    rospy.init_node('rospibot_network', anonymous=True) # create a rospibot_network node
    rospy.loginfo("started")
    try:
	rospy.spin() # loop until shutdown
    except KeyboardInterrupt:
	print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)
