#!/usr/bin/env python
# coding: utf-8

import roslib; roslib.load_manifest('turtlebot_teleop','rospeex_if')
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64
import datetime
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from rospeex_if import ROSpeexInterface
import sys, termios
import re
from std_srvs.srv import Empty, EmptyResponse

import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler

#parameters for ...
OPERATION_TIME = 500
_operation_count = 0
rule = "none"
point = 1
original = 0
destination = "none"
wheel = "none"
rospeex = None 
turtle_pub = None
_operation_count = 0
_pattern_rule = ""

class NavToPoint:
	def __init__(self):
		rospy.on_shutdown(self.cleanup)
		print '*******NavToPoint initialize Start*******'
		# Subscribe to the move_base action server
		self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
		print "Waiting for move_base action server..."

		# Wait for the action server to become available
		self.move_base.wait_for_server(rospy.Duration(100))
		print "Connected to move base server"

        # A variable to hold the initial pose of the robot to be set by the user in RViz
		initial_pose = PoseWithCovarianceStamped()
		rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose)

		# Get the initial pose from the user
		print "*** Click the 2D Pose Estimate button in RViz to set the robot's initial pose..."
		rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)
		self.last_location = Pose()

		print '***** Waiting for door open *****'
		rospy.Service('door_open', Empty, self.ServiceCallBack)

		# Make sure we have the initial pose
		while initial_pose.header.stamp == "":
			rospy.sleep(1)

		locations = dict()
		quaternion = quaternion_from_euler(0.0, 0.0, 1.5708)
		locations['Departure'] = Pose(Point(5.26, -0.809, 0.00247), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

		self.goal = MoveBaseGoal()
		print "Starting navigation test"

		while not rospy.is_shutdown():
			self.goal.target_pose.header.frame_id = 'map'
			self.goal.target_pose.header.stamp = rospy.Time.now()

			if wheel == "move":
				print "wheel == move"
				rospy.sleep(2)
				if destination == "Departure":
					self.goal.target_pose.pose = locations['Departure']
					self.move_base.send_goal(self.goal)
					waiting = self.move_base.wait_for_result(rospy.Duration(300))
					if waiting == 1:
				  		global wheel
						wheel = "wait"
						rospeex.say('質問をおねがいします。','ja','nict')
						rospy.sleep(5)

	def update_initial_pose(self, initial_pose):
		self.initial_pose = initial_pose
		if original == 0:
			self.origin = self.initial_pose.pose.pose
			global original
			original = 1

	def ServiceCallBack(self, req):
		rospeex.say('ドアが開きました。移動を開始します。', 'ja', 'nict')
		global destination
		destination = "Departure"
		global wheel
		wheel = "move"
		return EmptyResponse()

	def cleanup(self):
		rospy.loginfo("Shutting down navigation	....")
		self.move_base.cancel_goal()
		self.cmd_vel_pub.publish(Twist())
    	
#CallBack__Function for voice recognition
def VoiceCallBack(msg):
	print 'you said : \"%s\"' %msg

	if '中国' in msg and '首都' in msg:
	  rospeex.say('中国の首都は北京です。', 'ja', 'nict')
	  rospy.sleep(2)
	elif '今日' in msg and '曜日' in msg:
	  rospeex.say('今日は水曜日です。', 'ja', 'nict')
	  rospy.sleep(2)

if __name__=="__main__":
	rospy.init_node('speech_recognition')

	#rospeex
	settings = termios.tcgetattr(sys.stdin)
	rospeex = ROSpeexInterface()
	rospeex.init()
	rospeex.register_sr_response(VoiceCallBack)
	rospeex.set_spi_config(language='ja',engine='nict')

try:
	NavToPoint()
	rospy.spin()
		
except:
        pass

