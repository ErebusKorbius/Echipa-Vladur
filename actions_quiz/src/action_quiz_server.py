#!/usr/bin/env python3

import rospy
import actionlib
from std_msgs.msg import Empty
from ardrone_as.msg import ArdroneFeedback, ArdroneResult, ArdroneAction


class ArdroneAS(object):
    _feedback = ArdroneFeedback()
    _result = ArdroneResult()

    def __init__(self):
        # initialize the action server
        self._as = actionlib.SimpleActionServer("ardrone_action_server", ArdroneAction, execute_cb=self.execute_cb, auto_start=False)
        self.toff_pub = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
        self.land_pub = rospy.Publisher('/ardrone/land', Empty, queue_size=1)
        self._as.start()

    def execute_cb(self, goal):
        rate = rospy.Rate(1)
        empty_msg = Empty()
        command = goal.goal.upper()

        feedback_msg = ""
        for i in range(5):  # rulează timp de 5 secunde
            if self._as.is_preempt_requested():
                rospy.loginfo('Preempted')
                self._as.set_preempted()
                return

            if command == "TAKEOFF":
                self.toff_pub.publish(empty_msg)
                feedback_msg = "Taking off"
            elif command == "LAND":
                self.land_pub.publish(empty_msg)
                feedback_msg = "Landing"
            else:
                rospy.logwarn("Unknown command: %s", command)
                self._as.set_aborted()
                return

            self._feedback.feedback = feedback_msg
            self._as.publish_feedback(self._feedback)
            rate.sleep()

        # după 5 secunde considerăm acțiunea reușită
        self._result.result = f"{feedback_msg} completed"
        self._as.set_succeeded(self._result)


if __name__ == '__main__':
    rospy.init_node('ardrone_action_server')
    ArdroneAS()
    rospy.spin()

