# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 11:06:32 2018

@author: notic
"""

#def postprocessing():
    
import cv2
import os
import shutil
import time
import imutils
import math
import numpy as np

locationx = []
locationy = []
nomouseind = 0
storageind = 0
contoursa = []
cenY = []
cenX = []
tvalue = 50
#==============================================================================
# Folder path
#==============================================================================
print("Would you like to input the file path or is it a part of TOTO?\n\n")
print("[1] --- Custom path\n[2] --- Documents\n")
case = input("Input a numbers from the options listed above:\n")
if case == 1:
    path = raw_input("Enter the file path (e.g.: /folder/subfolder1/subfolder2/filename\n")

elif case == 2:
    directory = os.listdir("/home/notic/Documents/")
    selector = len(directory)
    print("Enter the number for the folder you wish to analyze from the list below:\n")
    for c in range(0,selector):
        print("["+ str(c) + "]" + directory[c] + "\n")
    filenumber = input("Which folder would you like to select?\n")
    if filenumber >= 0 and filenumber <= selector:
        print("The folder you selected is: " + directory[filenumber] +"!")
        path = "/home/notic/Documents/" + directory[filenumber]
else:
    print("You selected the wrong number! Restart the code!")    

path1 = path + "/Original"
path2 = path + "/Processed"
path3 = path + "/Information"
#==============================================================================
# Information files
#==============================================================================
mousecontours = open(path3 + "/Mouse_Name_Contours.txt" ,'wt')
mousecenters = open(path3 + "/Mouse_Name_Centers.txt", 'wt')
nomouseind = 0
    
   

    
#==============================================================================
# Read first frame and process it
#==============================================================================
bckimage = cv2.imread(path + "/firstframe.jpeg")
bckGray = cv2.cvtColor(bckimage, cv2.COLOR_BGR2GRAY)
bckBlur = cv2.GaussianBlur(bckGray, (91, 91), 0)
avg = bckBlur.copy().astype("float")


start_time = time.time()
for filename in os.listdir(path1):


#==============================================================================
#  Import images# 
#==============================================================================

    rstimage = cv2.imread(path1 + "/" + filename)

#==============================================================================
# Grayscale image
#==============================================================================

    rstGray = cv2.cvtColor(rstimage, cv2.COLOR_BGR2GRAY)

#==============================================================================
# Blurred image
#==============================================================================

    rstBlur = cv2.GaussianBlur(rstGray, (91, 91), 0)

#==============================================================================
#  Subtract
#==============================================================================
    
    cv2.accumulateWeighted(rstBlur, avg, 0.9)
    
#==============================================================================
# Adaptive threshold
#==============================================================================
#    avgpx = sum(sum(avg[827:927,1547:1647]))
#    px = sum(sum(rstBlur[827:927,1547:1647]))
#    diff = avgpx-px
#    if diff < 0 and diff > -20000:
#        tvalue = 40
#    elif diff>0 and diff<20000:
#        tvalue = 60
#    elif diff>20000:
#        tvalue = 60
    
    subBlur = cv2.absdiff(bckBlur, cv2.convertScaleAbs(avg))
    subThresh = cv2.threshold(subBlur, tvalue, 255, cv2.THRESH_BINARY)[1]

#==============================================================================
# Find the Largest Contour
#==============================================================================

    cnts = cv2.findContours(subThresh.copy(), cv2.RETR_EXTERNAL, 
                            cv2.CHAIN_APPROX_SIMPLE) #Function used to find the contours present in the frame/image
    cnts = cnts[0] if imutils.is_cv2() else cnts[1] 

    g = 0;
    mouse = 0;
                        
    for c in cnts: #For loop to find the largest countour present in the image
        f=len(c)
        if f>g:
            g = f
            mouse = c
        else:
            continue
                                
                            
    try:
        
        M = cv2.moments(mouse)
        cX = int(M["m10"] / M["m00"]) #Center location equations for the largest contour.
        cY = int(M["m01"] / M["m00"])
        contoursa.append(mouse)
        mousestr = str(mouse)
        mousecontours.write(mousestr + ';\n' )
        cenY.append(cY)
        cenX.append(cX)
        cXstr = str(cX)
        cYstr = str(cY)
        mousecenters.write(cXstr + " " + cYstr + ";\n")
                            
    except ZeroDivisionError:
        nomouseind += 1
        print('No mouse detected in this frame! Count = %d' %(nomouseind))
            
        continue
        
        #Draw the contour and center of the shape on the image
    cv2.drawContours(rstimage, [mouse], -1, (0, 255, 0), 2)
    cv2.circle(rstimage, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(rstimage, "center", (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
    locationx.append(cX)
    locationy.append(cY)
        
    cv2.imwrite(path2 + "/Processed_" + filename, rstimage)
    if math.fmod(storageind,5) == 0:
        print("Frame %d processed at %d seconds" %(storageind, time.time()-start_time))
    storageind += 1

        
print("The processing lasted %s seconds for %d frames" %((time.time()-start_time), storageind))    
np.save(path3 + "/Contours.npy", contoursa)
np.save(path3 + "/Center_X.npy", cenX)
np.save(path3 + "/Center_Y.npy", cenY)    
mousecontours.close
mousecenters.close        
    #return
    
#postprocessing()