#!/usr/bin/env python
# coding: utf-8

"""
	restaurant @RoboCup
	coded by hirono on 23/01/2016
"""

import roslib; roslib.load_manifest('turtlebot_teleop','rospeex_if')
import rospy
from std_msgs.msg import String,Int16
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from rospeex_if import ROSpeexInterface 
import sys, termios, re, tf
from subprocess import *
from std_srvs.srv import Empty, EmptyResponse

ChangeState = False
get_order = False
cnt = 0
drink = ''
food_order = ''
drink_order = ''

class guide:
	def __init__(self):
		rospy.Service('guide_start', Empty, self.ServiceCallBack)

		rospy.Subscriber('location', Pose, self.LocateCallBack)
		rospy.Subscriber('number', String, self.NumCallBack)

		self.pose = rospy.Publisher('initialpose', PoseWithCovarianceStamped, queue_size=10)
		self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=10)
		self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
		self.move_base.wait_for_server(rospy.Duration(100))

		self.destination = []
		self.drink = []
		self.food = []
		self.position = []
		self.rotate = []
		self.table = ''
		self.tmp = ''

		self.goal = MoveBaseGoal()
		self.initial_pose = PoseWithCovarianceStamped()
		self.tf_listener = tf.TransformListener()
		rospy.sleep(2)
		self.odom_frame = '/odom'
		self.tf_listener.waitForTransform(self.odom_frame, '/base_footprint', rospy.Time(), rospy.Duration(1.0))
		self.base_frame = '/base_footprint'
		
		self.r = rospy.Rate(5)
		self.turn_cmd = Twist()

		self.locations = dict()

	def ServiceCallBack(self, req):
		global ChangeState
		ChangeState = True
		return EmptyResponse()

	def NumCallBack(self, num):
		self.table = num.data

	def LocateCallBack(self, location):
		self.destination.append(location)
		#self.locations[self.table] = location

def VoiceCallBack(msg):
	print 'you said : \"%s\"' %msg

	if ('エレーナ' in msg or 'エー' in msg or 'Ａ' in msg or '英霊' in msg or 'テーブルへ' in msg or '経営' in msg or '映画' in msg or 'エレベーター' in msg or '上' in msg):
		rospeex.say('テーブル' + gd.table + 'から注文を取りに行きます。', 'ja', 'nict')
		rospy.sleep(2)
		gd.goal.target_pose.header.frame_id = 'map'
		gd.goal.target_pose.pose = gd.destination[0]
		#gd.goal.target_pose.pose = gd.locations['A']
		gd.move_base.send_goal(gd.goal)
		rospy.sleep(1)
		waiting = gd.move_base.wait_for_result(rospy.Duration(300))
		if waiting == 1:
			rospeex.say('テーブルAに到着しました。', 'ja', 'nict')
			rospy.sleep(2)
			gd.tmp = 'テーブルA'
			rospeex.say('頂いた注文を復唱しますので、よろしければ、はい、そうです、と言ってください。間違っていれば、いいえ、違います、と言ってください。それでは注文をどうぞ。', 'ja', 'nict')
			rospy.sleep(2)
			gd.position.append('テーブルA')

	elif ('テレビ' in msg or 'エネルギー' in msg or 'Ｂ' in msg):
		rospeex.say('テーブルBから注文を取りに行きます。', 'ja', 'nict')
		rospy.sleep(2)
		gd.goal.target_pose.header.frame_id = 'map'
		gd.goal.target_pose.pose = gd.destination[1]
		#gd.goal.target_pose.pose = gd.locations['B']
		gd.move_base.send_goal(gd.goal)
		rospy.sleep(1)
		waiting = gd.move_base.wait_for_result(rospy.Duration(300))
		if waiting == 1:
			rospeex.say('テーブルBに到着しました。', 'ja', 'nict')
			rospy.sleep(2)
			gd.tmp = 'テーブルB'
			rospeex.say('頂いた注文を復唱しますので、よろしければ、はい、そうです、と言ってください。間違っていれば、いいえ、違います、と言ってください。それでは注文をどうぞ。', 'ja', 'nict')
			rospy.sleep(2)
			gd.position.append('テーブルB')

	elif ('ヘルシー' in msg or 'Ｃ' in msg or '江頭' in msg or 'しい' in msg or 'シー' in msg):
		rospeex.say('テーブルCから注文を取りに行きます。', 'ja', 'nict')
		rospy.sleep(2)
		gd.goal.target_pose.header.frame_id = 'map'
		gd.goal.target_pose.pose = gd.destination[2]
		#gd.goal.target_pose.pose = gd.locations['C']
		gd.move_base.send_goal(gd.goal)
		rospy.sleep(1)
		waiting = gd.move_base.wait_for_result(rospy.Duration(300))
		if waiting == 1:
			rospeex.say('テーブルCに到着しました。', 'ja', 'nict')
			rospy.sleep(2)
			gd.tmp = 'テーブルC'
			rospeex.say('頂いた注文を復唱しますので、よろしければ、はい、そうです、と言ってください。間違っていれば、いいえ、違います、と言ってください。それでは注文をどうぞ。', 'ja', 'nict')
			rospy.sleep(2)
			gd.position.append('テーブルC')

	if ('ポテトチップス' in msg or '一日です' in msg or '土地' in msg):
		gd.food.append('ポテトチップス')
		global get_order
		get_order = True
		global food_order
		food_order = gd.tmp
	if ('駅' in msg or 'ピッチ' in msg or 'クッキー' in msg):
		gd.food.append('クッキー')
		global get_order
		get_order = True
		global food_order
		food_order = gd.tmp
	if ('していく' in msg or 'ポテトスティック' in msg or '一個' in msg):
		gd.food.append('ポテトスティック')
		global get_order
		get_order = True
		global food_order
		food_order = gd.tmp
	if ('ポタージュスープ' in msg):
		gd.food.append('ポタージュスープ')
		global get_order
		get_order = True
		global food_order
		food_order = gd.tmp
	if ('Ｘ' in msg or '駅です' in msg or 'エックス' in msg):
		gd.food.append('エッグスープ')
		global get_order
		get_order = True
		global drink_order
		drink_order = gd.tmp
	if ('オレンジ' in msg and not 'ジュース' in msg):
		gd.food.append('オレンジ')
		global get_order
		get_order = True
		global drink_order
		drink_order = gd.tmp
	if ('Ａｐｐｌｅ' in msg or 'アップル' in msg):
		gd.food.append('アップル')
		global get_order
		get_order = True
		global drink_order
		drink_order = gd.tmp
	if ('グリーンティ' in msg or 'グリーンピース' in msg):
		gd.drink.append('グリーンティー')
		global get_order
		get_order = True
		global drink_order
		drink_order = gd.tmp
	if ('カフェオレ' in msg or '英語で' in msg):
		gd.drink.append('カフェオレ')
		global get_order
		get_order = True
		global drink_order
		drink_order = gd.tmp
	if ('アイスティ' in msg or '愛して' in msg):
		gd.drink.append('アイスティー')
		global get_order
		get_order = True
		global drink_order
		drink_order = gd.tmp
	if ('オレンジジュース' in msg):
		gd.drink.append('オレンジジュース')
		global get_order
		get_order = True
		global drink_order
		drink_order = gd.tmp
	if ('ストロベリー' in msg):
		gd.drink.append('ストロベリージュース')
		global get_order
		get_order = True
		global drink_order
		drink_order = gd.tmp

	elif ('そう' in msg or 'はい' in msg):
		rospeex.say('かしこまりました。キッチンに戻ります。')
		rospy.sleep(2)
		gd.goal.target_pose.header.frame_id = 'map'
		gd.goal.target_pose.pose = gd.origin
		gd.move_base.send_goal(gd.goal)
		rospy.sleep(1)
		waiting = gd.move_base.wait_for_result(rospy.Duration(300))
		if waiting == 1:
			rospeex.say('キッチンに到着しました。', 'ja', 'nict')
			rospy.sleep(2)
			global cnt
			cnt += 1

	elif ('いいえ' in msg or '違います' in msg):
		rospeex.say('もう一度注文を教えてください。', 'ja', 'nict')
		rospy.sleep(1)
		if(len(gd.food) != None):
			for i in range(0, len(gd.food)):
				gd.food.pop()
				i += 1

		if(len(gd.drink) != None):
			for l in range(0, len(gd.drink)):
				gd.drink.pop()
				l += 1
	else:
		rospeex.say('もう一度教えてください。', 'ja', 'nict')
		rospy.sleep(1)
		
if __name__ == '__main__':
	rospy.init_node('restaurant')
	gd = guide()
	drink == ''

	while not rospy.is_shutdown():
		if ChangeState == True:

			settings = termios.tcgetattr(sys.stdin)
			rospeex = ROSpeexInterface()
			rospeex.init()
			rospeex.register_sr_response(VoiceCallBack)
			rospeex.set_spi_config(language='ja',engine='nict')

			rospy.sleep(7)
			p = Popen(['roslaunch', 'restaurant', 'amcl.launch', 'map_file:=/home/rg-tb01/catkin_ws/debug.yaml'])
			rospy.sleep(7)

			gd.initial_pose.header.frame_id = "map"
			gd.initial_pose.pose.pose = gd.destination[4]
			#gd.initial_pose.pose.pose = gd.locations['I']
			gd.pose.publish(gd.initial_pose)
			rospy.sleep(2)
			gd.origin = gd.destination[3]
			#gd.origin = gd.locations['K']
			rospeex.say('準備が完了しました。どこのテーブルから注文をとりますか。', 'ja', 'nict')
			rospy.sleep(2)
		
			global ChangeState
			ChangeState = False

		if (get_order == True):
			if (len(gd.drink) != 0):
				for i in range(0, len(gd.drink)):
					rospeex.say(gd.drink[i] , 'ja', 'nict')
					rospy.sleep(1)

			if (len(gd.food) != 0):
				for l in range(0,len(gd.food)):
					rospeex.say(gd.food[l] , 'ja', 'nict')
					rospy.sleep(3)

			rospeex.say('以上でよろしいでしょうか。', 'ja', 'nict')
			rospy.sleep(1)
			global get_order
			get_order = False

		if (cnt == 1):
			rospeex.say('どこのテーブルから注文をとりますか。', 'ja', 'nict')
			rospy.sleep(1)
			if(len(gd.drink) != 0):
				drink = gd.drink[0]
				gd.drink.pop()
			global cnt
			cnt += 1

		if (cnt == 3):
			rospeex.say('頂いた注文です。', 'ja', 'nict')
			rospy.sleep(1)
			if(len(gd.drink) != 0):
				drink = gd.drink[0]
				gd.drink.pop()

			if(drink != None):
				#rospeex.say(gd.position[0] + 'に' + drink + 'の注文がありました。', 'ja', 'nict')
				rospeex.say(drink_order + 'に' + drink + 'の注文がありました。', 'ja', 'nict')
				rospy.sleep(1)

			if(len(gd.food) != 0):
				rospeex.say(food_order + 'に' + gd.food[0] + 'と' + gd.food[1] + 'の注文がありました。', 'ja', 'nict')
				rospy.sleep(1)

			global cnt
			cnt = 0
