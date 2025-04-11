#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

def callback(data):
	move = Twist()
	front = data.ranges[180]
	left = data.ranges[359]
	right = data.ranges[0]

	if front > 1.0:
		move.linear.x=0.5
		move.angular.z=0.0
	else:
		move.linear.x=0.0
		move.angular.z=0.5
	if right < 1.0:
		move.linear.x=0.0
		move.angular.z=0.5
	if left < 1.0:
		move.linear.x=0.0
		move.angular.z=-0.5
	pub.publish(move)

rospy.init_node('Evita_obst')

sub = rospy.Subscriber('/scan', LaserScan, callback)

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)


rospy.spin()
