#!/usr/bin/env python

#
# This script allows to send strings over the rospibot_network topic
#
# script by Andrea Fioroni - andrifiore@gmail.com
# GitHub repo: https://github.com/tanicar/rospibot_project
#

import rospy
from std_msgs.msg import Int16MultiArray
import numpy as np

def talker():    
    pub = rospy.Publisher('cmd', Int16MultiArray, queue_size=10) # publish on motor_hat's cmd topic
    rospy.init_node('ros-joy-controller', anonymous=True) # init a ros-joy-controller node
    rate = rospy.Rate(10) # 10hz

    m1_speed = -150
    m2_speed = -133

    def send(values):
        values = [-v for v in values]  # hack
        msg = Int16MultiArray()
        msg.data = values
        pub.publish(msg)

    while not rospy.is_shutdown(): # loop until shutdown
        dir_str = raw_input("Choose direction: ")

        if dir_str == "w" :     # w = move forward
	    send([m1_speed,m2_speed,0,0])
	    rospy.loginfo(" - Move Forward")
        elif dir_str == "a" :   # a = turn left
            send([0,m2_speed,0,0])
	    rospy.loginfo(" - Turn Left")
        elif dir_str == "s" :   # s = move backward
            send([-m1_speed,-m2_speed,0,0])
	    rospy.loginfo(" - Move Backward")
        elif dir_str == "d" :   # d = turn right
            send([m1_speed,0,0])
	    rospy.loginfo(" - Turn Right")
        elif dir_str == "x" :   # x = stop
	    send([0,0,0,0])
	    rospy.loginfo(" - Stop")
            
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
