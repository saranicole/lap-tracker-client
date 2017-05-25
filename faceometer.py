import numpy as np
import urllib
import json
import cv2
import getopt
import sys

class FaceDetector(object):
    """A face detector utility
    """

    def __init__(self):
        self.cascade_path = "{base_path}/haarcascades/haarcascade_frontalface_default.xml".format(
        	base_path='/home/pi/laptracker/opencv-3.1.0/data')

    def detect(self, filepath, filename):
    	# initialize the data dictionary to be returned by the request
    	data = {"success": False}
        imagefile = "{filepath}/{filename}.jpg".format(filepath=filepath, filename=filename)
    	# load the image and convert
    	image = cv2.imread(imagefile)

        # convert the image to grayscale, load the face cascade detector,
        # and detect faces in the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detector = cv2.CascadeClassifier(self.cascade_path)
        rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,
        	minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        # construct a list of bounding boxes from the detection
        #rects = [(int(x), int(y), int(x + w), int(y + h)) for (x, y, w, h) in rects]

        rects = [ '{x},{y},{a},{b}'.format(x=x,y=y,a=str(int(x + w)),b=int(y + h)) for (x, y, w, h) in rects]
        faces = ';'.join(rects)

        # update the data dictionary with the faces detected
        data.update({"num_faces": str(len(rects)), "faces": faces, "success": True, "filename": filename, "filepath": filepath})

        return data
