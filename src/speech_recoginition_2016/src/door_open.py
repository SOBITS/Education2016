#!/usr/bin/env python

import rospy
from std_srvs.srv import Empty
from sensor_msgs.msg import LaserScan
import sys

center = 0

def depthcallback(data):
	#rospy.Rate(0.5).sleep()
	global center
	center = data.ranges[320]

if __name__ == '__main__':
	rospy.init_node('DoorOpen')
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
