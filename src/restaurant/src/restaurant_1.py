#!/usr/bin/env python
# coding: utf-8

"""
	restaurant @RoboCup
	coded by hirono on 23/01/2016
"""

import roslib; roslib.load_manifest('turtlebot_follower','rospeex_if')
import rospy
from std_msgs.msg import String
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from rospeex_if import ROSpeexInterface 
import sys, termios, re, tf
from subprocess import *
from turtlebot_msgs.srv import SetFollowState
#from rbx1_nav.transform_utils import quat_to_angle, normalize_angle
from math import radians, copysign, sqrt, pow, pi

TrainingState = 1
OrderingState = 0
follow = 0

class training:
	def __init__(self):
		#self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
		print '****** Waiting for move_base ******'
		#self.move_base.wait_for_server(rospy.Duration(100))

		# for getting the present location at training phase
		rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose)
		
		locations = dict()

		self.goal = MoveBaseGoal()

		# Initialize the tf listener
		self.tf_listener = tf.TransformListener()
		rospy.sleep(2)
		self.odom_frame = '/odom'
		self.tf_listener.waitForTransform(self.odom_frame, '/base_footprint', rospy.Time(), rospy.Duration(1.0))
		self.base_frame = '/base_footprint'
		# Initialize the position variable as a Point type
		position = Point()
		(position, rotation) = self.get_odom()
		x_start = position.x
		y_start = position.y


	def update_initial_pose(self, initial_pose):
		self.initial_pose = initial_pose
		if original == 0:
			self.origin = self.initial_pose.pose.pose
			global original
			original = 1

	def get_odom(self):
		try:
			(trans, rot) = self.tf_listener.lookupTransform(self.odom_frame, self.base_frame, rospy.Time(0))
		except (tf.Exception, tf.ConnectivityException, tf.LookupException):
			rospy.loginfo("TF Exception")
			return

		return (Point(*trans), (Quaternion(*rot)))

class guide:
	def __init__(self):
		print "guide phase start"

def kill_node(nodename):
	p2 = Popen(['rosnode', 'list'], stdout =PIPE)
	p2.wait()
	nodelist = p2.communicate()
	nd = nodelist[0]
	nd = nd.split("\n")
	for i in range(len(nd)):
		tmp = nd[i]
		ind = tmp.find(nodename)
		if ind == 1:
			call(['rosnode', 'kill', nd[i]])
			break

def FollowStartStop(x):
	rospy.wait_for_service('/turtlebot_follower/change_state')
	change_state = rospy.ServiceProxy('/turtlebot_follower/change_state', SetFollowState)
	response = change_state(x)

def VoiceCallBack(msg):
	print 'you said : \"%s\"' %msg

	if '開始' in msg:
		rospeex.say('ガイドフェーズを開始します。', 'ja', 'nict')
		Popen(['roslaunch', 'restaurant', 'mapping.launch'])
		rospy.sleep(10)
		rospeex.say('追跡を開始します。', 'ja', 'nict')
		rospy.sleep(2)
		FollowStartStop(1)

	elif '終了' in msg:
		rospeex.say('追跡を終了します。', 'ja', 'nict')
		FollowStartStop(0)
		rospy.sleep(1)
		follow = 0
		rospy.sleep(1)
		# save map
		p = Popen(['rosrun', 'map_server', 'map_saver', '-f', '/home/rg-tb01/catkin_ws/training'])
		#rospy.sleep(5)
		kill_node('slam_gmapping')
		p = Popen(['roslaunch', 'turtlebot_navigation', 'amcl_demo.launch', 'map_file:=/home/rg-tb01/catkin_ws/training.yaml'])
		rospy.sleep(5)
		#p = Popen(['rosrun', 'amcl', 'amcl'])
		# publish initial pose
		#initial_pose = PoseWithCovarianceStamped()
		#initial_pose.header.stamp=rospy.Time.now()
		#initial_pose.header.frame_id="map"
		#initial_pose.pose.pose.position.x = 5.0
		#initial_pose.pose.pose.position.y = 5.0
		#initial_pose.pose.pose.orientation.z = 1.0
		#initial_pose.pose.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891945200942]
		#pose.publish(initial_pose)

		#last_location = Pose()
		# terminate guide phase 
		global TrainingState
		TrainingState = 0

	elif 'テーブル' in msg:
		if TrainingState == 1 and OrderingState == 0:
			FollowStartStop(0)
			rospeex.say('A地点を記憶します。', 'ja', 'nict')
			rospy.sleep(2)
			(position, rotation) = get_odom()
			locations['A'] = (position, rotation)
			rospeex.say('追跡を再開します。', 'ja', 'nict')
			rospy.sleep(2)
			FollowStartStop(1)
		elif TrainingState == 0 and OrderingState == 1:
			# go to table
			self.goal.target_pose.pose = locations['A']
			self.move_base.send_goal(self.goal)
			rospy.sleep(1)

	elif 'ポテト' in msg and OrderingState == 1:
		# register order and location
		# orders['A'] =  
		rospy.sleep(1)

if __name__ == '__main__':
	rospy.init_node('restaurant')
	training()
	settings = termios.tcgetattr(sys.stdin)
	rospeex = ROSpeexInterface()
	rospeex.init()
	rospeex.register_sr_response(VoiceCallBack)
	rospeex.set_spi_config(language='ja',engine='nict')
	FollowStartStop(0)

	rospy.spin()
	#while not rospy.is_shutdown():
		#if TrainingState == 0:
			#print "*** Training Phase finished ***"
			#guide()

		#if follow == 0:
			#kill_node('gmapping_demo.launch')
