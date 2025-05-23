#!/usr/bin/env python3

import rospy
import actionlib
from ardrone_as.msg import ArdroneAction, ArdroneGoal

def feedback_cb(feedback):
    rospy.loginfo(f"[Feedback] {feedback.feedback}")

def main():
    rospy.init_node('ardrone_action_client')

    client = actionlib.SimpleActionClient('ardrone_action_server', ArdroneAction)


    command = input("TAKEOFF / LAND): ").strip().upper()
   

    goal = ArdroneGoal()
    goal.goal = command

   
    client.send_goal(goal, feedback_cb=feedback_cb)

    client.wait_for_result()
    result = client.get_result()

  

if __name__ == '__main__':
    main()

