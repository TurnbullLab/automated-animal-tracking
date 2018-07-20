# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 13:08:41 2018

@author: notic
"""

def imaging(begin, path1, path3):
    
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    import cv2
    import time
    import os
    
    start_time = time.time()
    
    stopwatch = []
    
#==============================================================================
# Initialize the camera
#==============================================================================
    
    camera=PiCamera()
    camera.resolution = (1648,928)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(1648,928))
    time.sleep(2)                      # Warmup time for camera
    storageind = 0
    filelist = open("/media/pi/TOTO/" + begin + "/Information/Mouse_Name_List.txt" ,'wt')  #Creates File for the specific mouse being imaged. MUST CHANGE NAME MANUALLY!!!
    
#==============================================================================
#  Frame Acquisition
#==============================================================================
    try:    
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            
            
            image = frame.array
            capture_time = time.time()-start_time
            stopwatch.append(capture_time)
            rawCapture.truncate(0) #Clearing the stream in preparation for the next frame
            
            
            cv2.imwrite("/media/pi/TOTO/" + begin + "/Original/image_%d.jpeg" % (storageind), image) #Writes frame and lebels it with a specific filenumber and storage ind
            print("Frame %d saved at --- %d seconds ---" %(storageind, time.time()-start_time))
            cv2.imshow("Image",image)
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord("q"):
                raise KeyboardInterrupt
            
            
            elapsedtime = time.time()-start_time
            elapsedtime = int(elapsedtime/60)
            hours = int(elapsedtime/60)
            minutes = elapsedtime-hours*60
            print("The current imaging time is %s hours and %s minutes" %(hours, minutes))
    
            storageind += 1
            
            
    except KeyboardInterrupt:
        
        finaltime = time.strftime("Date %Y.%m.%d. --- Time %H:%M:%S")
        np.save("/media/pi/TOTO/" + begin + "/Information/Time.npy", stopwatch)
        print("Your acquistion has been completed!")
        print("The program run time was %d hours and %d minutes" %(hours,minutes))
        src_files = os.listdir(path1)
        list = str(src_files)
        filelist.write("Imaging started on: \n" + begin + "\nAnd ended on:\n" + finaltime)
        filelist.write("\nFor the following files:\n")
        filelist.write(list)
        filelist.close
    
    return