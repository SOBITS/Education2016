#!/usr/bin/env python
# coding: utf-8

"""
	demo for speech_recognition @ invitation for univ
	coded by yano on 23/01/2016
"""

import roslib; roslib.load_manifest('turtlebot_teleop','rospeex_if')
import rospy
import datetime
from std_msgs.msg import String
from rospeex_if import ROSpeexInterface
import sys, termios
import re

#parameters for ...
OPERATION_TIME = 500
_operation_count = 0
rule = "none"
point = 1
original = 0
rospeex = None 
turtle_pub = None
_operation_count = 0
_pattern_rule = ""

class SpeechDemo:
    def __init__(self):
		print("********START SPEECH DEMO********")
		rospy.sleep(2)
		rospeex.say('我想一個問題', 'zh', 'nict')
		rospy.sleep(1)
    	
#CallBack__Function for voice recognition
def sr_response(msg):
	print 'You Said : \"%s\"' %msg
	rospeex.say(msg, 'zh', 'nict')
	
if __name__=="__main__":	
	rospy.init_node('speech_demo')

	#rospeex 
	settings = termios.tcgetattr(sys.stdin)
	rospeex = ROSpeexInterface()
	rospeex.init()
	rospeex.register_sr_response(sr_response)
	rospeex.set_spi_config(language='ja',engine='nict')

try:
	SpeechDemo()
	rospy.spin()
	
except:
        pass

