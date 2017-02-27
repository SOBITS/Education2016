#!/usr/bin/env python
# coding: utf-8
"""
    navi_2.py - enable turtlebot to navigate to predefined location based on voice command

"""

import roslib; roslib.load_manifest('turtlebot_teleop','rospeex_if')#byYANO 'pi_speech_tutorial' extinguish
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64
import datetime#by YANO
from geometry_msgs.msg import Twist#byYANO
from std_msgs.msg import String
from rospeex_if import ROSpeexInterface#byYANO
import sys, termios#byYANO
import re#by YANO broader.py

import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler

from sound_play.libsoundplay import SoundClient

OPERATION_TIME = 500#by YANO
_operation_count = 0#by YANO
rule = "none"#by YANO
point = 1
original = 0
message = "none"
start = 0
rospeex = None#byYANO 
turtle_pub = None#byYANO
_operation_count = 0#byYANO

_pattern_rule = ""#by YANO

class NavToPoint:

    def __init__(self):
        rospy.on_shutdown(self.cleanup)
          
        #self.voice = rospy.get_param("~voice", "voice_don_diphone")
        self.wavepath = rospy.get_param("~wavepath", "")
        
        # Create the sound client object
        self.soundhandle = SoundClient()
        rospy.sleep(1)
        self.soundhandle.stopAll()
        # Subscribe to the recognizer output
        #rospy.Subscriber('/recognizer/output', String, self.identify)
        
	# Publisher to manually control the robot
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=10)

	# Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")
        #rospeex.say('よろしくお願いします。', 'ja', 'nict')
        # Wait for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(10))#important
        rospy.loginfo("Connected to move base server")

        # Announce that we are ready for input
        self.soundhandle.playWave(self.wavepath + "/se_maoudamashii_chime10.wav")
        rospy.sleep(1)
        #self.soundhandle.say("initiated", self.voice)
	rospy.sleep(1)

        # A variable to hold the initial pose of the robot to be set by the user in RViz
        initial_pose = PoseWithCovarianceStamped()
        rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose)
	# Get the initial pose from the user
	#self.soundhandle.say("Where am I", self.voice)
        rospy.loginfo("*** Click the 2D Pose Estimate button in RViz to set the robot's initial pose...")
        rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)
        self.last_location = Pose()
        
        # Make sure we have the initial pose
        while initial_pose.header.stamp == "":
        	rospy.sleep(1)
            
        #self.soundhandle.say("Ready to go", self.voice)
	rospy.sleep(1)


	locations = dict()

	quaternion = quaternion_from_euler(0.0, 0.0, 1.5708)
	#locations['A'] = Pose(Point(0.5, 0.5, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))
	locations['A'] = Pose(Point(4.67, -4.01, 0.408), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

	quaternion = quaternion_from_euler(0.0, 0.0, 3.1412)
	#locations['B'] = Pose(Point(0.5, -0.5, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))byYANO change pose
	locations['B'] = Pose(Point(5.54, 0.58, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))
	
	quaternion = quaternion_from_euler(0.0, 0.0, -1.5708)
	locations['C'] = Pose(Point(7.93, 4.16, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))
	
	quaternion = quaternion_from_euler(0.0, 0.0, -1.5708)
	locations['D'] = Pose(Point(-0.24, 3.52, 0.000), Quaternion(quaternion[0], quaternion[1],  quaternion[2], quaternion[3]))
	
	#quaternion = quaternion_from_euler(0.0, 0.0, 0.0)
	#locations['D'] = Pose(Point(-0.24, 3.52, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3])

	self.goal = MoveBaseGoal()
        rospy.loginfo("Starting navigation test")

	while not rospy.is_shutdown():
	  self.goal.target_pose.header.frame_id = 'map'
	  self.goal.target_pose.header.stamp = rospy.Time.now()
	  if start == 1:
	    #rospy.loginfo("*********near Point *************")
	    rospy.loginfo('%s', message)
	    if message == "point A":
		rospy.sleep(2)
		self.goal.target_pose.pose = locations['A']
		rospy.sleep(2)
		rospy.loginfo('%s', message)
		self.move_base.send_goal(self.goal)
		waiting = self.move_base.wait_for_result(rospy.Duration(300))
		if waiting == 1:
		  #self.soundhandle.say("Reached Argentina", self.voice)
		  rospy.sleep(2)
		  rospy.loginfo("*********Reached Point A*************")
		  rospeex.say('質問をおねがいします。','ja','nict')
		  #rospeex.say('冷蔵庫に到着しました。', 'ja', 'nict')
		  #self.soundhandle.playWave(self.wavepath + "/R2D2a.wav")#byYANO
		  #self.soundhandle.say("Ready for next location", self.voice)
		  rospy.sleep(2)
		  global start
		  start = 0
			
	    if message == "point B":
		# Assume point B is Brazil
		#self.soundhandle.say("Going to Brazil", self.voice)
		rospy.sleep(2)
		rospy.loginfo("************first  ここまで入りました。**************************")
		self.goal.target_pose.pose = locations['B']
		rospy.loginfo("************second  ここまで入りました。**************************")
		self.move_base.send_goal(self.goal)
		rospy.loginfo("************theard  入りました。**************************")
		waiting = self.move_base.wait_for_result(rospy.Duration(300))
		#rospy.loginfo("************four  ここまで入りました。**************************")
		if waiting == 1:
		  #self.soundhandle.say("Reached Brazil", self.voice)
		  rospy.sleep(2)
		  rospy.loginfo("*********Reached Point B*************")
		  rospeex.say('テーブルに到着しました。', 'ja', 'nict')#by YANO
		  #self.soundhandle.playWave(self.wavepath + "/R2D2a.wav")#byYANO
		  #self.soundhandle.say("Ready to go", self.voice)
		  rospy.sleep(2)
		  global start
		  start = 0

	    if message == "point C":
		# Assume point C is China
		#self.soundhandle.say("Going to China", self.voice)
		rospy.sleep(2)
		rospy.loginfo("************ここまで入りました。**************************")
		self.goal.target_pose.pose = locations['C']
		self.move_base.send_goal(self.goal)
		waiting = self.move_base.wait_for_result(rospy.Duration(300))
		if waiting == 1:
		  #self.soundhandle.say("Reached China", self.voice)
		  rospy.sleep(2)
		  rospy.loginfo("*********Reached Point C*************")
		  rospeex.say('洗濯機に到着しました。', 'ja', 'nict')#by YANO
		  #self.soundhandle.say("Ready for next place", self.voice)
		  rospy.sleep(2)
		  global start
		  start = 0

	    if message == "point D":
		# Assume point D is Denmark
		#self.soundhandle.say("Going to Denmark", self.voice)
		rospy.sleep(2)
		rospy.loginfo("************ここまで入りました。**************************")
		#quaternion = quaternion_from_euler(0.0, 0.0, 0.0)
		#locations['D'] = Pose(Point(-0.24, 3.52, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3])
		self.goal.target_pose.pose = locations['D']
		self.move_base.send_goal(self.goal)
		waiting = self.move_base.wait_for_result(rospy.Duration(300))
		if waiting == 1:
		  #self.soundhandle.say("Reached Denmark", self.voice)
		  rospy.sleep(2)
		  rospy.loginfo("*********Reached Point D*************")
		  rospeex.say('布団に到着しました。', 'ja', 'nict')#by YANO
		  #self.soundhandle.say("Where is my next location", self.voice)
		  rospy.sleep(2)
		  global start
		  start = 0

	    if message == "origin":
		#self.soundhandle.say("Going back home", self.voice)
		rospy.sleep(2)
		rospy.loginfo("************戻っています。*****************")
		self.goal.target_pose.pose = self.origin
		self.move_base.send_goal(self.goal)
		waiting = self.move_base.wait_for_result(rospy.Duration(300))
		if waiting == 1:
		  #self.soundhandle.say("Reached home", self.voice)
		  rospy.sleep(2)
		  rospy.loginfo("*********Reached home*************")
		  rospeex.say('ただ今帰りました。', 'ja', 'nict')
		  global start
		  start = 0

		rospy.Rate(3).sleep()

    def update_initial_pose(self, initial_pose):
        self.initial_pose = initial_pose
	if original == 0:
		self.origin = self.initial_pose.pose.pose
		global original
		original = 1

    #def identify(self, msg):
    #def sr_response(message): 
    	#rospy.loginfo("************I HEARD %s************", msg.data)
        # Print the recognized words on the screen
        #if msg.data == 'go to argentina' or msg.data == 'argentina':
        ##if msg.data == 'tea':
		##global message
		##message = "point A"
		##rospy.loginfo(message)
		##global start
		##start = 1
        #elif msg.data == 'go to brazil' or msg.data == 'brazil':
        ##elif msg.data == 'negative':
		##global message
		##message = "point B"
		##rospy.loginfo(message)
		##global start
		##start = 1
	##elif msg.data == 'go to china' or msg.data == 'china':
		##global message
		##message = "point C"
		##rospy.loginfo(message)
		##global start
		##start = 1
	##elif msg.data == 'go to denmark' or msg.data == 'denmark':
		##global message
		##message = "point D"
		##rospy.loginfo(message)
		##global start
		##start = 1
        ##elif msg.data == 'go back to original place' or msg.data == 'go back' or msg.data == 'original' or msg.data == 'go home':
		##global message
		##message = "origin"
		##rospy.loginfo(message)
		##global start
		##start = 1
		
    def cleanup(self):
		rospy.loginfo("Shutting down navigation	....")
		self.move_base.cancel_goal()
		self.cmd_vel_pub.publish(Twist())
    	
def sr_response(msg):
	rospy.loginfo('入りました。')
	print 'you said : \"%s\"' %msg#byYANO
	#elem = '冷蔵庫','テーブル','戻れ'#by OGUSAN
	if 'スタート' in msg:#by YANO
	  rospy.loginfo("************************I'm hungry******************************")#byYANO
	  #rospeex.say('冷蔵庫にいきます。', 'ja', 'nict')
	  global message
	  message = "point A"
	  rospy.loginfo(message)
	  global start
	  start = 1
	  # Assume point A is Argentina
	  #self.soundhandle.say("Going to Argentina", self.voice)
	  rospy.sleep(2)
	elif '山' in msg:
	  rospy.loginfo("*************************let's study******************************")#byYANO
	  rospeex.say('日本一高い山は富士山です。', 'ja', 'nict')
	  global message
	  #message = "point B"
	  rospy.loginfo(message)
	  global start
	  start = 1
	  rospy.sleep(2)
	elif '湖' in msg:
	  rospy.loginfo("*************************sit down******************************")#byYANO
	  rospeex.say('日本一広い湖は琵琶湖です。', 'ja', 'nict')
	  global message
	  #message = "point C"
	  rospy.loginfo(message)
	  global start
	  start = 1
	  rospy.sleep(2)
	elif '川' in msg:
	  rospy.loginfo("*************************good night******************************")#byYANO
	  rospeex.say('日本一長い川は信濃川です。', 'ja', 'nict')
	  global message
	  #message = "point D"
	  rospy.loginfo(message)
	  global start
	  start = 1
	  rospy.sleep(2)
	elif '首都' in msg: 
	  rospy.loginfo("**************************go to home************************************")#by YANO
	  rospeex.say('日本の首都は東京です。', 'ja', 'nict')
	  global message
	  #message = "origin"
	  rospy.loginfo(message)
	  global start
	  start = 1
	elif '一年' in msg: 
	  rospy.loginfo("**************************go to home************************************")#by YANO
	  rospeex.say('一年は365日です。', 'ja', 'nict')
	  global message
	  #message = "origin"
	  rospy.loginfo(message)
	  global start
	  start = 1

class CenterDepth:

	def __init__(self):
		self._scan_sub = rospy.Subscriber('scan',LaserScan,self.depthCallback)

	def depthCallback(self, data):
		#rospy.loginfo("ready ++++++++++++++++++++++++++++++++++++++++++++++ door opened")
		#laser = LaserScan()
		#center = Float64()
		laser = data
		center = laser.ranges[320]
#		rospy.loginfo("human distance:%f",center)
		if center > 2:
			#rospy.loginfo("door opened")
			global message
			#message = "point A"
			rospy.loginfo(message)
			global start
			#start = 1
			# Assume point A is Argentina
			#self.soundhandle.say("Going to Argentina", self.voice)
			rospy.sleep(2)
    
if __name__=="__main__":	
		rospy.init_node('navi_point')#byYANO
		center_depth = CenterDepth()
		settings = termios.tcgetattr(sys.stdin)#byYANO
		rospeex = ROSpeexInterface()
		rospeex.init()
		rospeex.register_sr_response(sr_response)
		rospeex.set_spi_config(language='ja',engine='nict')

try:
		NavToPoint()
		rospy.spin()
		#node.run()
except:
        pass

