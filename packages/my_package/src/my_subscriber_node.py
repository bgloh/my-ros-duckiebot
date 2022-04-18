#!/usr/bin/env python3
"""
OpenCV feature detectors with ros CompressedImage Topics in python.
This example subscribes to a ros topic containing sensor_msgs CompressedImage. 
It converts the CompressedImage into a numpy.ndarray, then detects and marks features in that image.>
and publishes the new image - again as CompressedImage topic.
"""

import os,sys,time
import rospy
import cv2
import numpy as np
from duckietown.dtros import DTROS, NodeType, TopicType, DTParam, ParamType
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import CameraInfo

class MySubscriberNode(DTROS):

    def __init__(self, node_name):
        # initialize the DTROS parent class
        super(MySubscriberNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
        # construct publisher
        self.image_pub = rospy.Publisher("output/image_raw/compressed", CompressedImage,queue_size = 2)

        # construct subscriber
        self.subscriber = rospy.Subscriber("/duckieIronMan/camera_node/image/compressed",CompressedImage, self.callback,  queue_size = 1)


    def callback(self, data):
        # direct conversion to cv2
        np_arr = np.frombuffer(data.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        rospy.loginfo("I heard %s", np_arr)
        # feature detectors using cv2
        #method = "GridFAST"
        feat_det = cv2.xfeatures2d.SIFT_create(500) #cv2.FeatureDetector_create(method)
        time1 = time.time()
        # convert np image to grayscale
        featPoints = feat_det.detect(cv2.cvtColor(image_np,cv2.COLOR_BGR2GRAY))
        time2 = time.time()
        # draw a circle near objects 
        for featpoint in featPoints:
             x,y = featpoint.pt
             # Draw a circle with  line borders of thickness of 1 px
             image=image_np
             center_coordinates=(int(x),int(y));radius=10;color=(255,0,0);thickness=1
             image = cv2.circle(image, center_coordinates, radius, color, thickness) 
             # cv2.imshow('cv_img',image_np)
             # cv2.waitKey(2)
             # show image

        ### Create CompressedImage  ####
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np.array(cv2.imencode('.jpg',image_np)[1]).tostring()
        # publish new image
        self.image_pub.publish(msg)

if __name__ == '__main__':
    # create the node
    node = MySubscriberNode(node_name='my_subscriber_node')
    # keep spinning
    rospy.spin()


