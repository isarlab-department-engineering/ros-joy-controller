#!/usr/bin/env python

#
# This script allows to send strings over the ros_joy_controller topic
#
# script by Andrea Fioroni - andrifiore@gmail.com
# GitHub repo: https://github.com/isarlab-department-engineering/ros-joy-controller
#

import rospy,sys,numpy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy 
from master_node.msg import *
from master_node.srv import *

#impostare il nome del nodo coerente con quello del master
id_node = "joy"

#impostare la risposta positiva coerente con quella del master
positive_answ = 1



twistmessage = Twist()

followmessage = Follow()

followmessage.id = id_node

lock = False

jump = False

max_vel = 200


pub = rospy.Publisher('follow_topic', Follow, queue_size=1) # publish on ros_joy_controller topic
request_lock_service = rospy.ServiceProxy('request_lock',RequestLockService)
release_lock_service = rospy.ServiceProxy('release_lock',ReleaseLockService)

def mainFunction():
    rospy.init_node('ros_joy_controller', anonymous=True) # init a ros_joy_controller node

    #Sottosrizione al topic shared lock
    rospy.Subscriber("lock_shared",Lock,checkMessage)

    #Sottoscrizione al topic joy
    rospy.Subscriber("joy",Joy,requestLock)

    rospy.loginfo("Gamepad follower ready")

    #REALEASE SULLO SHUTDOWN
    rospy.on_shutdown(releaseLock)
    rospy.spin()

 

def requestLock(data):
    global id_node, lock, jump
    if lock:
        followFunction(data)
    elif jump:
        jump = False
    else:

        if numpy.abs(data.axes[0])>0.02 or numpy.abs(data.axes[1])>0.02:
            resp = request_lock_service(id_node)
            print(resp)
            if resp:
                lock = True
                followFunction(data)
            else:
                msg_shared = rospy.wait_for_message("/lock_shared", Lock)
                checkMessage(msg_shared)

def releaseLock():
    global id_node, lock
    resp = release_lock_service(id_node)
    lock = False
    print(resp)




def checkMessage(data):
    global id_node, lock
    if data.id == id_node:
        if data.msg == 1:
            lock = True
        else:
            lock = False
    else:
        msg_shared = rospy.wait_for_message("/lock_shared", Lock)
        checkMessage(msg_shared)



def followFunction(data):
    global jump, max_vel
    #print(data)

    direction = data.axes # [0]>0 left, [0]<0 right; [1]>0 front, [1]<0 rear
    buttons = data.buttons

    if buttons[3] == 1:
        jump = True
        releaseLock()
    else:
        turn = direction[0]
        go = direction[1]

        print (go)

        if turn > 0:
            twistmessage.linear.x = (go*max_vel)/2 + (turn*max_vel)/2
            twistmessage.linear.y = (go*max_vel)
        else:
            twistmessage.linear.x = (go*max_vel)
            twistmessage.linear.y = (go*max_vel)/2 + (turn*max_vel)/2           
    print(twistmessage)
    followmessage.twist = twistmessage
    pub.publish(followmessage) # publish on the topic

if __name__ == '__main__':
    try:
        mainFunction()
    except rospy.ROSInterruptException:
        pass
