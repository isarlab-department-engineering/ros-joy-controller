#!/usr/bin/env python

#
# This script allows to send strings over the ros_joy_controller topic
#
# script by Andrea Fioroni - andrifiore@gmail.com
# GitHub repo: https://github.com/isarlab-department-engineering/ros-joy-controller
#

import rospy,sys
from geometry_msgs.msg import Twist

twistmessage = Twist()
twistmessage.linear.x=0
twistmessage.linear.y=0
twistmessage.linear.z=0
twistmessage.angular.x=0
twistmessage.angular.y=0
twistmessage.angular.z=0

def talker():
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1) # publish on ros_joy_controller topic
    rospy.init_node('ros_joy_controller', anonymous=True) # init a ros_joy_controller node
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown(): # loop until shutdown
        dir_str = raw_input("Choose direction: ")
        rospy.loginfo(dir_str)
	if dir_str == 'w':
		twistmessage.linear.x=140
		twistmessage.linear.y=140
		twistmessage.linear.z=0
		twistmessage.angular.x=0
		twistmessage.angular.y=0
		twistmessage.angular.z=0
	elif dir_str == 's':
                twistmessage.linear.x=-140
                twistmessage.linear.y=-140
                twistmessage.linear.z=0
                twistmessage.angular.x=0
                twistmessage.angular.y=0
                twistmessage.angular.z=0
	elif dir_str == 'd':
                twistmessage.linear.x=100
                twistmessage.linear.y=0
                twistmessage.linear.z=0
                twistmessage.angular.x=0
                twistmessage.angular.y=0
                twistmessage.angular.z=0
	elif dir_str == 'a':
                twistmessage.linear.x=0
                twistmessage.linear.y=100
                twistmessage.linear.z=0
                twistmessage.angular.x=0
                twistmessage.angular.y=0
                twistmessage.angular.z=0
	elif dir_str == 'x':
                twistmessage.linear.x=0
                twistmessage.linear.y=0
                twistmessage.linear.z=0
                twistmessage.angular.x=0
                twistmessage.angular.y=0
                twistmessage.angular.z=0
       	pub.publish(twistmessage) # publish on the topic
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
