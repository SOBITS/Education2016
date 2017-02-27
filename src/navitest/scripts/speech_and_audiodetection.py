#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
	import roslib; roslib.load_manifest('rospeex_if','turtlebot_follower')
except:
	pass

import rospy
import re


from std_msgs.msg import String,Bool,Float64

from rospeex_if import ROSpeexInterface
from turtlebot_msgs.srv import SetFollowState

rospeex = None
sig = Bool()
destination = String()

class Rospeex(object):
	def __init__(self):
		self._interface = ROSpeexInterface()
		FollowStartStop(0)
		
	def sr_response(self, message):
		print 'you said : \"%s\"' %message

		if 'テスト' in message:
			self._interface.say('マイクテスト、チェック、ワンツー', 'ja', 'nict')
		elif 'ついてきて' in message:
			self._interface.say('わかりました、ついていきます。', 'ja', 'nict')

			destination.data = "follow"
			d_pub.publish(destination)
			destination.data = ""
			rospy.sleep(1)

			FollowStartStop(1)

		elif '戻って' in message:
			self._interface.say('わかりました、もどります。', 'ja', 'nict')
			print("Robot will go back the position started.")

			destination.data = "follow_start"
			d_pub.publish(destination)
			destination.data = ""
			rospy.sleep(1)

			FollowStartStop(0)

		elif '退場' in message:
			self._interface.say('わかりました、アリーナから退場します。', 'ja', 'nict')
			print("Robot will go back initial position.")

			destination.data = "leave_arena"
			d_pub.publish(destination)
			destination.data = ""
			rospy.sleep(1)
		else:
			self._interface.say('もう一度おねがいします。', 'ja', 'nict')		

	def run(self):
        # initialize rospeex
		self._interface.init()
		self._interface.register_sr_response(self.sr_response)
		self._interface.set_spi_config(language='ja', engine='nict')
		
		word_sub = rospy.Subscriber('speech',String,self.speech)
		rospy.spin()

	def speech(self,word):
		print("*******Speech*******")
		self.words = String()
		self.words.data = word.data
		self._interface.say( self.words.data ,'ja','nict')
		rospy.sleep(2)
		self.words = ""#clear

def FollowStartStop(x):
	rospy.wait_for_service('/turtlebot_follower/change_state')
	change_state = rospy.ServiceProxy('turtlebot_follower/change_state',SetFollowState)
	response = change_state(x)


if __name__ == '__main__':
	rospy.init_node('speech_and_audiodetection')
	d_pub = rospy.Publisher('location_name',String,queue_size = 10)

	try:
		rp = Rospeex()
		rp.run()

	except rospy.ROSInterruptException:
		pass
