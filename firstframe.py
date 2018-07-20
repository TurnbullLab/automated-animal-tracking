# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 12:52:50 2018

@author: notic
"""

#==============================================================================
#First Frame Acquisition 
#==============================================================================

def firstframe(begin):
    
    import cv2
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    import time
    
#==============================================================================
# Initialize the camera
#==============================================================================
    camera=PiCamera()
    camera.resolution = (1648,928)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(1648,928))
    time.sleep(2)  #Warmup time for camera
    
#==============================================================================
# First Frame Acquisition 
#==============================================================================

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        
        image = frame.array
        rawCapture.truncate(0) #Clearing the stream in preparation for the next frame
        
        
        cv2.imwrite("/media/pi/TOTO/" + begin + "/firstframe.jpeg" , image) #Writes frame and lebels it with a specific filenumber and storage ind
        print("First frame has been acquired!") 
        break

    camera.close
    return