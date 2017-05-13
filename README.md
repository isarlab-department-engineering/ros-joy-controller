# ros-joy-controller
ROS package that interfaces the robot with a joystick and sends commands to the motor controller node.



ROS Nodes:

- talker.py:
runs on the remote computer, allowing the user to input "wasd" encoded Stings through a Arduino Esplora controller

- rospibot_network.py
runs on the robot, and it puts together informations from all other ROS Nodes running, finally communicating with the motor_hat Node in order to move the robot



Arduino scripts:

- ROSpiBot_wasdx.ino:
uses Arduino Esplora libraries to allow the joystick to send Strings through the keyboard. 



Encoded Strings:
- w = move forward
- a = turn left
- d = turn right
- s = move backward
- x = stop
