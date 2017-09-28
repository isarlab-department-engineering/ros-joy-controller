#!/usr/bin/env python

#
# This script allows to send strings over the ros_joy_controller topic
#
# script by Andrea Fioroni - andrifiore@gmail.com
# GitHub repo: https://github.com/isarlab-department-engineering/ros-joy-controller
#

import rospy,sys
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy 

twistmessage = Twist()
pub = rospy.Publisher('follow_topic', Twist, queue_size=1) # publish on ros_joy_controller topic

def mainFunction():
    rospy.init_node('ros_joy_controller', anonymous=True) # init a ros_joy_controller node
    rospy.Subscriber("joy",Joy,followFunction)
    rospy.loginfo("Gamepad follower ready")
    rospy.spin()

def followFunction(data):
    direction = data.axes # [0]>0 left, [0]<0 right; [1]>0 front, [1]<0 rear
    if direction[0] == 0.0 and direction[1] == 0.0:
        twistmessage.linear.x = 0
        twistmessage.linear.y = 0
    elif direction[1] > 0.0:
        twistmessage.linear.x = 140
        twistmessage.linear.y = 140
    elif direction[1] < 0.0:
        twistmessage.linear.x = -140
        twistmessage.linear.y = -140
    elif direction[0] > 0.0:
        twistmessage.linear.x = 0
        twistmessage.linear.y = 140
    elif direction[0] < 0.0: 
        twistmessage.linear.x = 140
        twistmessage.linear.y = 0
    print(twistmessage)
    pub.publish(twistmessage) # publish on the topic

if __name__ == '__main__':
    try:
        mainFunction()
    except rospy.ROSInterruptException:
        pass
