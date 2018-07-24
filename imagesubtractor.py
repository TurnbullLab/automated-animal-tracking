# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 12:13:17 2018

@author: notic
"""
import cv2
import os
import shutil
import time
import imutils

from firstframe import firstframe
from imaging import imaging

#==============================================================================
#File Creation 
#==============================================================================

begin = time.strftime("Date %Y_%m_%d_ --- Time %H_%M_%S")


path = ("/media/pi/TOTO/"+ begin)
os.mkdir(path)
path1 = ("/media/pi/TOTO/" + begin + "/Original")
path12 = ("/media/pi/TOTO/" + begin + "/Original2")
path13 = ("/media/pi/TOTO/" + begin + "/Original3")
path14 = ("/media/pi/TOTO/" + begin + "/Original4")
path15 = ("/media/pi/TOTO/" + begin + "/Original5")
path2 = ("/media/pi/TOTO/" + begin + "/Processed")
path3 = ("/media/pi/TOTO/" + begin + "/Information")

if os.path.exists(path1): #Checks to see if path already exists
    shutil.rmtree(path1)  #delete path if it exists
    os.mkdir(path1)  #Make Directory function (path, mode)
else:
    os.mkdir(path1)  #If the path does not exist a new one is created
    os.mkdir(path12)
    os.mkdir(path13)
    os.mkdir(path14)
    os.mkdir(path15)
    
if os.path.exists(path2): 
    shutil.rmtree(path2)
    os.mkdir(path2)
else:
    os.mkdir(path2)
    
if os.path.exists(path3): 
    shutil.rmtree(path3)
    os.mkdir(path3)
else:
    os.mkdir(path3)
    
#==============================================================================
# Call first frame and imaging functions
#==============================================================================

firstframe(begin)
answer = raw_input("Would you like to continue to the imaging program? (Yes/No)\n")
if answer == "Yes" or answer == "yes" or answer == "YES":
    print("The frame acquisition will now begin!")
    time.sleep(1)
    imaging(begin)
elif answer == "No" or answer == "NO" or answer == "no":  
    print("The program will close now!")
    quit()
    
quit()