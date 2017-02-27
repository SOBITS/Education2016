#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Bool,String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import sys

d_judge = Bool()
command = Twist()

def depthcallback(data):
	if data.ranges[320] > 2:
		global d_judge
		d_judge.data = True
	else:
		global d_judge
		d_judge.data = False		
		

if __name__ == '__main__':
	rospy.init_node('door_open')
	pub = rospy.Publisher('door_open',Bool,queue_size = 10)
	tw_pub = rospy.Publisher('cmd_vel_mux/input/teleop',Twist,queue_size = 5)
	word_pub = rospy.Publisher('speech',String,queue_size = 10)
	try:
		while not rospy.is_shutdown():
			rospy.Subscriber('xtion_scan', LaserScan, depthcallback)

			if d_judge.data == True:
				print "***** DOOR was opened *****"
				print "***** Enter the arena *****"
				
				word = String()
				word.data = "ドアがあきました。"
				word_pub.publish(word)
				word.data = ""

				rospy.sleep(3)

				command.linear.x = 0.2
				for i in range(120000):
					tw_pub.publish(command)#test

				rospy.sleep(2)
				command.linear.x = 0
				tw_pub.publish(command)

				print "***** Publish door_open --> TRUE *****"
				rospy.sleep(5)
				pub.publish(d_judge)
				sys.exit()
			else:
				rospy.sleep(1)
				print "***************************"
				pub.publish(d_judge)

	except rospy.ROSInterruptException:
		pass
