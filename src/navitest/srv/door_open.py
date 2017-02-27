#!/usr/bin/env python

import rospy
from navitest.srv import DoorOpen
from navitest.srv import DoorOpenResponse

from sensor_msgs.msg import LaserScan
import sys		

center = 0

def depthcallback(data):
	#rospy.Rate(0.5).sleep()
	global center
	center = data.ranges[320]

def check(req):
	result = False

	if center > 2 :
		result = True
	else:
		result = False

	return DoorOpenResponse(success=result)

def DoorOpenServer():
	rospy.init_node('door_open')
	s = rospy.Service('door_open',DoorOpen,check)

if __name__ == '__main__':
	rospy.init_node('door_open')
	try:
		rospy.wait_for_service('door_open')
		rospy.Subscriber('scan', LaserScan, depthcallback)
		print "*****Get Depth******"
		while not rospy.is_shutdown():
			if center > 2:
				print '***** DOOR OPEN *****'
				service = rospy.ServiceProxy('door_open', Empty)
				response = service()
				rospy.sleep(1)
				sys.exit()

	except rospy.ROSInterruptException:
		pass
