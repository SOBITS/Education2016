#!/usr/bin/env python
# coding: utf-8

"""
set_location(String型)をSubscribeし，その文字列に応じてmap上におけるlocation（座標，向き）を設定するノード

1.mapファイルを指定してRvizを立ち上げる
2.Rviz上でTurtlebotの初期位置を設定する

messageによってロボットの状態（目的地へ行く，止まって待つなど）を管理している

"""
import roslib; roslib.load_manifest('turtlebot_teleop','rospeex_if')#byYANO 'pi_speech_tutorial' extinguish
import rospy

from std_msgs.msg import Float64,String,Bool
from geometry_msgs.msg import Twist
import datetime

import sys, termios
import re

import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler


OPERATION_TIME = 500
_operation_count = 0
rule = "none"
point = 1
original = 0
human_detection = Bool()
detect_counter = 0

message = String()
pre_message = String()
start = 0

command = Twist()

turtle_pub = None
_operation_count = 0

_pattern_rule = ""

class NavToPoint:

	def __init__(self):
		rospy.on_shutdown(self.cleanup)        
	# Publisher to manually control the robot
		self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=10)
	# Subscribe to the move_base action server
		self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
		rospy.loginfo("Waiting for move_base action server...")
        # Wait for the action server to become available
		self.move_base.wait_for_server(rospy.Duration(10))#important
		rospy.loginfo("Connected to move base server")
		rospy.sleep(1)
       

        # A variable to hold the initial pose of the robot to be set by the user in RViz
		initial_pose = PoseWithCovarianceStamped()
		rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose)
	# Get the initial pose from the user
		rospy.loginfo("*** Click the 2D Pose Estimate button in RViz to set the robot's initial pose...")
		rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)
		self.last_location = Pose()
        # Make sure we have the initial pose
		while initial_pose.header.stamp == "":
			rospy.sleep(1)

		locations = dict()

		quaternion = quaternion_from_euler(0.0, 0.0, 1.5708)
		locations['A'] = Pose(Point(-3.55, -4.86, 0.00247), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

		locations['B'] = Pose(Point(-4.6, 1.19, 0.0025), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

		locations['C'] = Pose(Point(-0.131, -0.00497, 0.404), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

		locations['E'] = Pose(Point(-3.84, -7.56, 0.00247), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

		self.goal = MoveBaseGoal()
		rospy.loginfo("Starting navigation test")



		rate = rospy.Rate(10) #10 times per second
		while not rospy.is_shutdown():
			self.goal.target_pose.header.frame_id = 'map'
			self.goal.target_pose.header.stamp = rospy.Time.now()
			d_sub = rospy.Subscriber('location_name',String,set_location)
			hd_sub = rospy.Subscriber('hd_result',Bool,stop_robot)
			print("**********Wait for publish [ location_name ]***********\n")
			if start == 1:
				rospy.sleep(1)

				if message == "WayPoint_1":
					print("**************go to WayPoint_1********************")
					self.goal.target_pose.pose = locations['A']
					self.move_base.send_goal(self.goal)
					waiting = self.move_base.wait_for_result(rospy.Duration(300))
					if waiting == 1:
						print("Robot reached to WayPoint_1")

						word = String()
						word.data = "ウェイポイント１に到着しました。続いて、ウェイポイント2に向かいます。"
						word_pub.publish(word)
						word.data = ""

						rospy.sleep(4)	
						global message
						message = "WayPoint_2"
						waiting = 0

				elif message == "WayPoint_2":
					print("**************go to WayPoint_2********************")
					self.goal.target_pose.pose = locations['B']
					self.move_base.send_goal(self.goal)
					waiting = self.move_base.wait_for_result(rospy.Duration(300))

					global human_detection
					if human_detection == True:
						print("The Robot will stop.")
						global pre_message,message
						pre_message = message

						rospy.sleep(1)
						word = String()
						word.data = "すみません、道を開けていただけませんか。"
						word_pub.publish(word)
						word.data = ""

#						global message
#						message = "Stop"
#						waiting = 0

					if waiting == 1:
						print("Robot reached to WayPoint_2")

						word = String()
						word.data = "ウェイポイント2に到着しました。次はウェイポイント３に向かいます。"
						word_pub.publish(word)
						word.data = ""

						rospy.sleep(4)	
						global message
						message = "WayPoint_3"
						waiting = 0

				elif message == "following":
					rospy.sleep(1)
					print("**************The Robot is following human. ********************")

				elif message == "follow_start":
					print("**************The Robot go back . ********************")
					self.goal.target_pose.pose = locations['C']
					self.move_base.send_goal(self.goal)
					waiting = self.move_base.wait_for_result(rospy.Duration(300))
					if waiting == 1:
						print("Robot reached to WayPoint_3")

						word = String()
						word.data = "ウェイポイント3に戻りました。"
						word_pub.publish(word)
						word.data = ""

						rospy.sleep(4)
						global message
						message = "leave_arena"
						waiting = 0

				elif message == "WayPoint_3":
					print("**************go to WayPoint_3********************")
					self.goal.target_pose.pose = locations['C']
					rospy.sleep(1)
					self.move_base.send_goal(self.goal)
					rospy.sleep(1)
					waiting = self.move_base.wait_for_result(rospy.Duration(400))
					if waiting == 1:
						print("Robot reached to FollowMe start Position.")

						word = String()
						word.data = "追跡対象を検出するので私の前に来て「ついてきて」と言ってください。「戻って」と言われたら戻ります。"
						word_pub.publish(word)
						word.data = ""

						rospy.sleep(4)
						global message
						message = "following"
						waiting = 0

				elif message == "origin":
					rospy.sleep(2)
					print("************go back start_position*****************")
					self.goal.target_pose.pose = self.origin
					self.move_base.send_goal(self.goal)
					waiting = self.move_base.wait_for_result(rospy.Duration(300))
					if waiting == 1:
						print("*********The Robot reached the home*************")
						rospy.sleep(2)
						global start
						start = 0

						waiting = 0
						word = String()
						word.data = "開始位置に戻りました。"
						word_pub.publish(word)
						word.data = ""

						rospy.sleep(4)	
						global message
						message = "leave_arena"
						waiting = 0
				elif message == "Stop":
					rospy.sleep(1)
					print("**************The Robot wait for getting away human.********************")
					self.move_base.cancel_goal()
#					self.cmd_vel_pub.publish(Twist())
					rospy.sleep(2)

					global human_detection	
					if human_detection == True:
						command.linear.x = 0
#						for i in range(100):
						tw_pub.publish(command)#test
					else:
						global message,pre_message
						message = pre_message	#WayPoint_2

				elif message == "leave_arena":
					word = String()
					word.data = "アリーナから退場します。"
					word_pub.publish(word)
					word.data = ""
					rospy.sleep(2)
					print("**************go to end_point********************")
					self.goal.target_pose.pose = locations['E']
					self.move_base.send_goal(self.goal)
					waiting = self.move_base.wait_for_result(rospy.Duration(300))			
					if waiting == 1:
						print("Robot reached to end_point")
						word = String()
						word.data = "ナビゲーションテストを終了します。ありがとうございました。"
						word_pub.publish(word)
						word.data = ""
				else:
					print("***********destination_error*************")
		rate.sleep()

	def update_initial_pose(self, initial_pose):
		self.initial_pose = initial_pose
		if original == 0:
			self.origin = self.initial_pose.pose.pose
			global original
			original = 1

	def cleanup(self):
		rospy.loginfo("Shutting down navigation	....")
		self.move_base.cancel_goal()
		self.cmd_vel_pub.publish(Twist())


def set_location(name):
	global message
	message = ""
	message = name.data
	global start
	start = 1

def stop_robot(result):
	if result.data == True:
#		print("human_detection : True")
		global human_detection
		human_detection = True
	else:
		global human_detection
		human_detection = False

if __name__=="__main__":	
	rospy.init_node('set_location')
	word_pub = rospy.Publisher('speech', String, queue_size = 20)
	tw_pub = rospy.Publisher('cmd_vel_mux/input/teleop',Twist,queue_size = 10)

	try:
		NavToPoint()
		rospy.spin()
	except:
		pass

