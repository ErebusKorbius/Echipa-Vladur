#!/usr/bin/env python
import rospy
from services_quiz.srv import CustomSquare, CustomServMessResponse
from geometry_msgs.msg import Twist

def my_callback(request):
    rospy.loginfo("Service move")
    
    move_straight = Twist()
    move_straight.linear.x = 0.2
    move_straight.angular.z = 0.0

    turn_left = Twist()
    turn_left.linear.x = 0.0
    turn_left.angular.z = 0.5  

    rate = rospy.Rate(10)  
    seconds_straight = request.duration  
    seconds_turn = int(90 / (turn_left.angular.z * 180 / 3.14))  

    for _ in range(4):
        for _ in range(seconds_straight * 10):
            my_pub.publish(move_straight)
            rate.sleep()
y
      
        stop = Twist()
        my_pub.publish(stop)
        rospy.sleep(0.5)

     
        for _ in range(15): 
            my_pub.publish(turn_left)
            rate.sleep()

        my_pub.publish(stop)
        rospy.sleep(0.5)

  
    return CustomServMessResponse(success=True)


rospy.init_node('service_move_jackal_custom_server')
my_pub = rospy.Publisher('/jackal_velocity_controller/cmd_vel', Twist, queue_size=1)
my_service = rospy.Service('/move_jackal_custom', CustomServMess, my_callback)
rospy.loginfo("Service /move_jackal_custom Ready")
rospy.spin()

