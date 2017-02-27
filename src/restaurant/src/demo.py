#!/usr/bin/env python
# coding: utf-8

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
from std_srvs.srv import Empty, EmptyResponse

def FollowStartStop(x):
	rospy.wait_for_service('/turtlebot_follower/change_state')
	change_state = rospy.ServiceProxy('/turtlebot_follower/change_state', SetFollowState)
	response = change_state(x)

def VoiceCallBack(msg):
	print 'you said : \"%s\"' %msg

	if('ついてきて' in msg):
		rospeex.say('ついていくよー。', 'ja', 'nict')
		rospy.sleep(2)
		FollowStartStop(1)
	elif('止まって' in msg):
		rospeex.say('止まるよ。', 'ja', 'nict')
		rospy.sleep(2)
		FollowStartStop(0)

if __name__ == '__main__':
	rospy.init_node('follow_demo')
	FollowStartStop(0)

	settings = termios.tcgetattr(sys.stdin)
	rospeex = ROSpeexInterface()
	rospeex.init()
	rospeex.register_sr_response(VoiceCallBack)
	rospeex.set_spi_config(language='ja',engine='nict')
	rospy.sleep(2)

	rospeex.say('命令をどうぞ。', 'ja', 'nict')
	rospy.sleep(2)
	
	rospy.spin()
