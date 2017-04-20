#!/usr/bin/env python

#
# This script allows to send strings over the ros_joy_controller topic
#
# script by Andrea Fioroni - andrifiore@gmail.com
# GitHub repo: https://github.com/tanicar/rospibot_project
#

import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('ros_joy_controller', String, queue_size=10) # publish on ros_joy_controller topic
    rospy.init_node('ros_joy_controller', anonymous=True) # init a ros_joy_controller node
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown(): # loop until shutdown
        dir_str = raw_input("Choose direction: ")
        rospy.loginfo(dir_str)
        pub.publish(dir_str) # publish on the topic
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
