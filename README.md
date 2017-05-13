# ros-joy-controller
ROS package that interfaces the robot with a joystick and send commands to the motor controller node.

ROS Nodes:

- talker.py:
runs on the remote computer, allowing the user to input "wasd" encoded Stings through a Arduino Esplora controller

- rospibot_network.py
runs on the robot, and it puts together informations from all other ROS Nodes running, finally communicating with the motor_hat Node in order to move the robot
