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
from math import radians, copysign, sqrt, pow, pi
from std_srvs.srv import Empty, EmptyResponse

TrainingState = 1

class training:
	def __init__(self):
		rospy.wait_for_service('guide_start')

		self.locate = rospy.Publisher('location', Pose, queue_size=10)
		self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=10)
		self.table = rospy.Publisher('number', String, queue_size=10)

		# Initialize the tf listener
		self.tf_listener = tf.TransformListener()
		self.odom_frame = '/odom'
		self.tf_listener.waitForTransform(self.odom_frame, '/base_footprint', rospy.Time(), rospy.Duration(1.0))
		self.base_frame = '/base_footprint'

		self.num = ""
		self.rotate = ""
		self.current_pose = Pose()
		self.State_change = False
		self.r = rospy.Rate(5);

		self.turn_cmd = Twist()

	def get_odom(self):
		try:
			(trans, rot) = self.tf_listener.lookupTransform(self.odom_frame, self.base_frame, rospy.Time(0))
		except (tf.Exception, tf.ConnectivityException, tf.LookupException):
			rospy.loginfo("TF Exception")
			return
		return (Point(*trans), (Quaternion(*rot)))

def VoiceCallBack(msg):
	print 'you said : \"%s\"' %msg

	if ('ついてきて' in msg):
		rospeex.say('レストランを開始します。', 'ja', 'nict')
		Popen(['roslaunch', 'restaurant', 'mapping.launch'])
		rospy.sleep(5)
		rospeex.say('そのままお待ちください。', 'ja', 'nict')
		rospy.sleep(2)
		tr.turn_cmd.linear.x = 0
		tr.turn_cmd.angular.z = radians(45); #45 deg/s in radians/s
		for x in range(0,53):
			tr.cmd_vel.publish(tr.turn_cmd)
			tr.r.sleep()
		rospeex.say('追跡を開始します。', 'ja', 'nict')
		rospy.sleep(2)
		FollowStartStop(1)

	elif('止まって' in msg):
		rospeex.say('止まります。', 'ja', 'nict')
		rospy.sleep(2)
		FollowStartStop(0)

	elif ('キッチン' in msg):
		tr.State_change = True
		if ('右' in msg):
			rospeex.say('キッチンが右手ですね。', 'ja', 'nict')
			rospy.sleep(1)
			tr.rotate = '右'
		if ('左' in msg):
			rospeex.say('キッチンが左手ですね。', 'ja', 'nict')
			rospy.sleep(1)
			tr.rotate = '左'
		if (tr.rotate == ''):
			rospeex.say('どちらにキッチンがありますか。', 'ja', 'nict')
			rospy.sleep(1)

	elif ('エレーナ' in msg or 'エー' in msg or 'Ａ' in msg or '英霊' in msg or 'テーブルへ' in msg or '経営' in msg or '映画' in msg or 'エレベーター' in msg or '上' in msg or '停電' in msg):
		FollowStartStop(0)
		tr.num = 'A'
		tr.table.publish(tr.num)
		if ('右' in msg):
			rospeex.say('テーブルAが右手ですね。', 'ja', 'nict')
			rospy.sleep(1)
			tr.rotate = '右'
		if ('左' in msg):
			rospeex.say('テーブルAが左手ですね。', 'ja', 'nict')
			rospy.sleep(1)
			tr.rotate = '左'
		if (tr.rotate == ''):
			rospeex.say('どちらにテーブルAがありますか。', 'ja', 'nict')
			rospy.sleep(1)

	elif ('テレビ' in msg or 'エネルギー' in msg or 'テーブルに' in msg):
		FollowStartStop(0)
		tr.num = 'B'
		tr.table.publish(tr.num)
		if ('右' in msg):
			rospeex.say('テーブルBが右手ですね。', 'ja', 'nict')
			rospy.sleep(1)
			tr.rotate = '右'
		if ('左' in msg):
			rospeex.say('テーブルBが左手ですね。', 'ja', 'nict')
			rospy.sleep(1)
			tr.rotate = '左'
		if (tr.rotate == ''):
			rospeex.say('どちらにテーブルBがありますか。', 'ja', 'nict')
			rospy.sleep(1)

	elif ('ヘルシー' in msg or 'Ｃ' in msg or '江頭' in msg or 'しい' in msg):
		FollowStartStop(0)
		tr.num = 'C'
		tr.table.publish(tr.num)
		if ('右' in msg):
			rospeex.say('テーブルCが右手ですね。', 'ja', 'nict')
			rospy.sleep(1)
			tr.rotate = '右'
		if ('左' in msg):
			rospeex.say('テーブルCが左手ですね。', 'ja', 'nict')
			rospy.sleep(1)
			tr.rotate = '左'
		if (tr.rotate == ''):
			rospeex.say('どちらにテーブルCがありますか。', 'ja', 'nict')
			rospy.sleep(1)

	elif ('左' in msg and tr.num != '' and tr.rotate == ""):
		if(tr.State_change == False):
			rospeex.say('テーブル' + str(tr.num) + 'が左ですね。', 'ja', 'nict')
			rospy.sleep(1)
			tr.rotate = '左'
		if(tr.State_change == True):
			rospeex.say('キッチンが左ですね。', 'ja', 'nict')
			rospy.sleep(1)
			tr.rotate = '左'

	elif ('右' in msg and tr.num != '' and tr.rotate == ""):
		if(tr.State_change == False):
			rospeex.say('テーブル' + str(tr.num) + 'が右ですね。', 'ja', 'nict')
			rospy.sleep(1)
			tr.rotate = '右'
		if(tr.State_change == True):
			rospeex.say('キッチンが右ですね。', 'ja', 'nict')
			rospy.sleep(1)
			tr.rotate = '右'

	elif ('そう' in msg or 'はい' in msg):
		if(tr.State_change == False):
			(position, rotation) = tr.get_odom()
			tr.current_pose = Pose(position,rotation)
			if(tr.rotate == '右'):
				tr.current_pose.orientation.z = 0.0 
				tr.current_pose.orientation.z -= 0.7
				tr.current_pose.orientation.w = 1.0
				tr.current_pose.orientation.w -= 0.3
			if(tr.rotate == '左'):
				tr.current_pose.orientation.z = 0.0
				tr.current_pose.orientation.z += 0.7
				tr.current_pose.orientation.w = 1.0
				tr.current_pose.orientation.w -= 0.3
			tr.locate.publish(tr.current_pose)
			rospeex.say('かしこまりました。追跡を再開します。', 'ja', 'nict')
			rospy.sleep(2)
			tr.num = ''
			tr.rotate = ''
			#tr.current_pose = Pose()
			FollowStartStop(1)

		elif(tr.State_change == True):
			tr.num = 'K'
			tr.table.publish(tr.num)
			(position, rotation) = tr.get_odom()
			tr.current_pose = Pose(position,rotation)
			if(tr.rotate == '右'):
				tr.current_pose.orientation.z = 0.0 
				tr.current_pose.orientation.z -= 0.7
				tr.current_pose.orientation.w = 1.0
				tr.current_pose.orientation.w -= 0.3
			if(tr.rotate == '左'):
				tr.current_pose.orientation.z = 0.0
				tr.current_pose.orientation.z += 0.7
				tr.current_pose.orientation.w = 1.0
				tr.current_pose.orientation.w -= 0.3
			tr.locate.publish(tr.current_pose)
			global TrainingState
			TrainingState = 0

	elif ('いいえ' in msg or '違います' in msg):
		tr.num = 0
		tr.rotate = ''
		rospeex.say('もう一度場所を教えてください。', 'ja', 'nict')
		rospy.sleep(1)

	else:
		rospeex.say('もう一度教えてください。', 'ja', 'nict')
		rospy.sleep(1)

def FollowStartStop(x):
	rospy.wait_for_service('/turtlebot_follower/change_state')
	change_state = rospy.ServiceProxy('/turtlebot_follower/change_state', SetFollowState)
	response = change_state(x)

if __name__ == '__main__':
	rospy.init_node('training_phase')
	FollowStartStop(0)

	tr = training()

	settings = termios.tcgetattr(sys.stdin)
	rospeex = ROSpeexInterface()
	rospeex.init()
	rospeex.register_sr_response(VoiceCallBack)
	rospeex.set_spi_config(language='ja',engine='nict')
	rospy.sleep(2)

	rospeex.say('準備が完了しました。', 'ja', 'nict')
	rospy.sleep(2)

	rospeex.say('はじめるときは、ついてきて、と言ってください。', 'ja', 'nict')
	rospy.sleep(1)

	while not rospy.is_shutdown():
		if TrainingState == 0:
			rospeex.say('かしこまりました。', 'ja', 'nict')
			rospy.sleep(1)
			tr.num = 'I'
			tr.table.publish(tr.num)
			#FollowStartStop(0)
			rospy.sleep(1)
			(position, rotation) = tr.get_odom()
			tr.locate.publish(Pose(position,rotation))
			Popen(['rosrun', 'map_server', 'map_saver', '-f', '/home/rg-tb01/catkin_ws/debug'])
			rospy.sleep(3)
			rospeex.say('オーダリングフェーズの準備を行います。', 'ja', 'nict')
			rospy.sleep(1)			
			service = rospy.ServiceProxy('guide_start', Empty)
			response = service()
			rospy.sleep(3)
			Popen(['rosnode', 'kill', 'turtlebot_follower'])
			Popen(['rosnode', 'kill', 'follower_velocity_smoother'])
			Popen(['rosnode', 'kill', 'slam_gmapping'])
			Popen(['rosnode', 'kill', 'navigation_velocity_smoother'])
			Popen(['rosnode', 'kill', 'kobuki_safety_controller'])
			Popen(['rosnode', 'kill', 'move_base'])
			sys.exit()

	rospy.spin()
