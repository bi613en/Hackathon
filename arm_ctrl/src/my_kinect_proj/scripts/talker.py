#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic



#rosrun my_kinect_proj talker.py cmd_vel:=/turtle1/cmd_vel


import struct

file = open( "/dev/input/mice", "rb" );
import roslib
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from random import random



def getMouseEvent():
  buf = file.read(3);
  button = ord( buf[0] );
  bLeft = button & 0x1;
  bMiddle = ( button & 0x4 ) > 0;
  bRight = ( button & 0x2 ) > 0;
  x,y = struct.unpack( "bb", buf[1:] );
  print ("L:%d, M: %d, R: %d, x: %d, y: %d\n" % (bLeft,bMiddle,bRight, x, y) );
  return (x,y, bLeft, bMiddle)



def talker():
    mouse_pos = [0,0];    
    pub = rospy.Publisher('cmd_vel', Twist)
    rospy.init_node('talker', anonymous=True)
    r = rospy.Rate(50) # 10hz
    while not rospy.is_shutdown():
	diff = getMouseEvent();
	x = 0
	z = 0
	if (diff[2]):
		x = x+2;
		z = z+2;
	if (diff[3]):
		x = x+2;
		z = z-2;
	
	twist = Twist()
	twist.linear.x = x                 # our forward speed
	twist.linear.y = 0; 
	twist.linear.z = 0;     # we can't use these!        
	twist.angular.x = 0; 
	twist.angular.y = 0;   #          or these!
 	twist.angular.z = z;  
	
	pub.publish(twist)
	#diff = getMouseEvent();
	#mouse_pos[0] = mouse_pos[0] + diff[0];
	#mouse_pos[1] = mouse_pos[1] + diff[1];
        #str = '[2.0, 0.0, 0.0]' '[0.0, 0.0, 1.8]'
        #rospy.loginfo(str)
        #pub.publish(str)
        r.sleep()
        
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
