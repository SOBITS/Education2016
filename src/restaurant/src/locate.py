#!/usr/bin/env python
# coding: utf-8

"""
	restaurant @RoboCup
	node of guide phase for 
	coded by hirono on 23/01/2016
"""
import rospy
from std_srvs.srv import Empty
import sys

def DestCallBack(msg)
	if 'テーブル' in msg and '一' in msg:
		

if __name__ == '__main__':
	rospy.init_node('restaurant')
	rospy.Subscriber('destination', String, DestCallBack)

	while not rospy.is_shutdown():
