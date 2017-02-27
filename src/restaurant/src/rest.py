#!/usr/bin/env python
# coding: utf-8

import roslib; roslib.load_manifest('rospeex_if','turtlebot_follower')
import rospy
from std_msgs.msg import String

import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from rospeex_if import ROSpeexInterface 
import sys, termios, re, tf

point = 1
original = 0
message = "none"
start = 0

class NavToPoint:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)

	# Publisher to manually control the robot
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)

	# Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        
        # Wait for the action server to become available
        rospy.loginfo("Waiting for move_base action server...")
        self.move_base.wait_for_server(rospy.Duration(10))
        rospy.loginfo("Connected to move base server")


		pose = rospy.Publisher('initialpose', PoseWithCovarianceStamped, self.update_initial_pose)
        
        initial_pose = PoseWithCovarianceStamped()
		initial_pose.header.stamp=rospy.Time.now()
        initial_pose.header.frame_id="map"
        initial_pose.pose.pose.position.x = 5.0
        initial_pose.pose.pose.position.y = 5.0
        initial_pose.pose.pose.orientation.z = 1.0
        initial_pose.pose.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891945200942]
        pose.publish(initial_pose)
    
        self.last_location = Pose()
        
        # Make sure we have the initial pose
        while initial_pose.header.stamp == "":
        	rospy.sleep(1)
                 
        # define dictionary for location
	locations = dict()
	quaternion = quaternion_from_euler(0.0, 0.0, 1.5708)
	locations['A'] = Pose(Point(0.5, 0.5, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

	self.goal = MoveBaseGoal()
        rospy.loginfo("Starting navigation test")

	while not rospy.is_shutdown():
	  self.goal.target_pose.header.frame_id = 'map'
	  self.goal.target_pose.header.stamp = rospy.Time.now()
	  if start == 1:
		if message == "point A":
	 	  rospeex.say('テーブルにいきます', 'ja', 'nict')
		  rospy.sleep(2)
		  self.goal.target_pose.pose = locations['table']
	  	  self.move_base.send_goal(self.goal)
		  waiting = self.move_base.wait_for_result(rospy.Duration(300))
		  if waiting == 1:
	 	    rospeex.say('テーブルに到着しました', 'ja', 'nict')
		    rospy.sleep(2)
		    global start
		    start = 0

		rospy.Rate(3).sleep()

    def update_initial_pose(self, initial_pose):
        self.initial_pose = initial_pose
	if original == 0:
		self.origin = self.initial_pose.pose.pose
		global original
		original = 1
	
	def FollowStartStop(x):
      rospy.wait_for_service('/turtlebot_follower/change_state')
      try:
        change_state = rospy.ServiceProxy('/turtlebot_follower/change_state', SetFollowState)
        response=change_state(x)
      except rospy.ServiceException, e:
        pass

    def sr_response(msg):
		print 'you said : \"%s\"' %msg
		if 'ガイド開始' in msg:
	  		FollowStartStop(1)
	  
		elif 'テーブル' in msg:
			global message
			message = "point A"
			rospy.loginfo(message)
			#listen to actual Pose()
			quaternion = quaternion_from_euler(0.0, 0.0, 1.5708)
			locations['table'] = Pose(Point(0.5, 0.5, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))
			global start
			start = 1
		elif 'ガイド終了' in msg:
			FollowStartStop(0)

    def cleanup(self):
        rospy.loginfo("Shutting down navigation	....")
	self.move_base.cancel_goal()
        self.cmd_vel_pub.publish(Twist())

if __name__=="__main__":
    rospy.init_node('navi_point')
    settings = termios.tcgetattr(sys.stdin)
    rospeex = ROSpeexInterface()
    rospeex.init()
    rospeex.register_sr_response(sr_response)
    rospeex.set_spi_config(language='ja',engine='nict')

    try:
        NavToPoint()
        rospy.spin()
    except:
        pass

