#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
	import roslib; roslib.load_manifest('rospeex_if')
except:
	pass

import rospy

from std_msgs.msg import String,Bool,Float64

move_permission = 0
destination = String()

def door_open(result):
	if result.data == True :
		print("Door was opened --> Navigation Test  START")
		rospy.sleep(1)
		print("publish first location_name")

		word = String()
		word.data = "アリーナに入りました。"
		word_pub.publish(word)
		word.data = ""
		
		rospy.sleep(2)

		global destination#test
		destination.data = "WayPoint_1"
		d_pub.publish(destination)
		destination.data = ""

	else:
		print("Robot is waiting for the door to open.")

if __name__ == '__main__':
	try:
		rospy.init_node('navitest_2016')
		d_pub = rospy.Publisher('location_name',String,queue_size = 10)
		word_pub = rospy.Publisher('speech',String,queue_size = 10)

		sub = rospy.Subscriber('door_open',Bool,door_open)
		print("navitest_2016 is ready")
		rospy.spin()

	except rospy.ROSInterruptException:
		pass
