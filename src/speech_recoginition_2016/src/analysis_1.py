#!/usr/bin/env python
# coding: utf-8

"""
	demo for speech_recognition @ TurtleBot lecture
	coded by hirono on 23/01/2016
"""

import roslib; roslib.load_manifest('rospeex_if')
import rospy
import datetime
from std_msgs.msg import String
from rospeex_if import ROSpeexInterface
import sys, termios
import re

def textcallback(msg):

	if('テスト' in msg):
		rospeex.say('マイクテスト。', 'ja', 'nict')
		rospy.sleep(1)

if __name__=="__main__":	
	rospy.init_node('speech_demo')
	
	rospy.Subscriber('voice', String, textcallback)
	rospy.spin()
