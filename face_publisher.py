'''
/*
 * Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from faceometer import FaceDetector
from datetime import datetime
import picamera
import random
import json
import sys
import logging
import time
import getopt
import boto3

camera = picamera.PiCamera()
facedetector = FaceDetector()
pics_dir = "/home/pi/laptracker/pics"
# boto3.set_stream_logger(name='botocore')
s3 = boto3.resource('s3')
bucket_name = "msmith-tracking-image-bucket"

# Say Cheese
def say_cheese():
    current_secs = time.time()
    milliseconds = int(round(current_secs * 1000))
    filename = time.strftime("%Y%m%d-%H%M%S",time.gmtime(milliseconds / 1000))
    imagefile = "{pics_dir}/{filename}.jpg".format(filename=filename, pics_dir=pics_dir)
    camera.capture(imagefile)
    detect_dict = facedetector.detect(pics_dir,filename)
    detect_dict['timestamp'] = str(milliseconds)
    return detect_dict

# Usage
usageInfo = """Usage:

Start face detection:
python face_publisher.py -i <seconds to wait between taking pictures> -l <1 or 2 for which pi>

Type "python face_publisher.py -h" for available options.
"""
# Help info
helpInfo = """-i, --interval
	Seconds to wait between taking pictures
    -l, --location
    	"1" or "2", depending on which Pi is the origin
-h, --help
	Help information
"""

# Read in command-line parameters
useWebsocket = False
interval=1
location=random.choice('ab')
topic="facedetection1"
host = "a5026ozfxej17.iot.us-east-1.amazonaws.com"
rootCAPath = "/home/pi/security/root_ca.key"
certificatePath = "/home/pi/security/667_cert.pem"
privateKeyPath = "/home/pi/security/667_private_key.pem"
try:
	opts, args = getopt.getopt(sys.argv[1:], "hi:l:", ["help", "interval=", "location="])
	# if len(opts) == 0:
	# 	raise getopt.GetoptError("No input parameters!")
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print(helpInfo)
			exit(0)
		if opt in ("-i", "--interval"):
			interval = float(arg)
        if opt in ("-l", "--location"):
			location = arg
except getopt.GetoptError:
	print(usageInfo)
	exit(1)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Publish the photo if there are faces detected
loopCount = 0
while True:
    detection_response = say_cheese()
    if detection_response['success']:
        detection_response['success'] = 'true'
        detection_response['location'] = location
        imagefile = "{pics_dir}/{filename}.jpg".format(filename=detection_response['filename'], pics_dir=pics_dir)
        imagedata = open(imagefile, 'rb')
        s3.Bucket(bucket_name).put_object(Key=detection_response['filename'], Body=imagedata, Metadata=detection_response)
	loopCount += 1
	time.sleep(interval)
