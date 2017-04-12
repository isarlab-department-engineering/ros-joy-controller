#!/usr/bin/env python

#
# This script allows to send strings over the rospibot_network topic
#
# script by Andrea Fioroni - andrifiore@gmail.com
# GitHub repo: https://github.com/tanicar/rospibot_project
#

import rospy
from std_msgs.msg import String

def talker():                 # TODO: set proper topic name
    pub = rospy.Publisher('rospibot_network', String, queue_size=10) # publish on rospibot_network topic
    rospy.init_node('ros-joy-controller', anonymous=True) # init a rospibot_network_talker node
    rate = rospy.Rate(10) # 10hz

    def_speed = 50

    while not rospy.is_shutdown(): # loop until shutdown
        dir_str = raw_input("Choose direction: ")

        if dir_str == "w" :     # w = move forward
            pub.publish("")
        elif dir_str == "a" :   # a = turn left
            pub.publish("")
        elif dir_str == "s" :   # s = move backward
            pub.publish("")
        elif dir_str == "d" :   # d = turn right
            pub.publish("")
        elif dir_str == "x" :   # x = stop
            pub.publish("")
            
        rospy.loginfo(dir_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
