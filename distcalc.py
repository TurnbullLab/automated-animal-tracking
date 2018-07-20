# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 10:45:01 2018

@author: notic
"""

#def distcalc():
#    
#    path3 = raw_input("Enter the path of the center location file:\n")
#    
#    file = open(path3 + "/Mouse_Name_Centers.txt").read()
#    centerlocation = [[item.split(",") for item in file.split(';\n')][:-1]]
#    #centerlocation = map(int, centerlocation)
#    
#    print(centerlocation)
##    centerlocation[1,1]
#    return(centerlocation)
#    
#    
#    
#distcalc()



import math
import statistics
import matplotlib.pyplot as plt
import numpy as np
#import seaborn as sns


totaldist = 0
velocity = [0]
pvelocity = [0]
pdista = [0]
dista = [0]
factor = 0.0178546 # Scaling factor for pixels to cm
#physicaldista = []

path = raw_input("Enter the path of the folder you wish to analyze:\n")
path3 = path+ "/Information"
distfile = open( path3 + "/Distance_Stat(mea,med,std,var).txt", 'wt')
distfile2 = open(path3 + "/Distance_per_frame.txt", 'wt')
physicaldistf2 = open(path3 + "/Pixel_dist_per_frame.txt",'wt')
physicaldistf = open(path3 + "/Pixel_dist_stats.txt",'wt')
velfile = open(path3 + "/Velocity_Stat(mea,med,std,var).txt", 'wt')
velfile2 = open(path3 + "/Velocity_per_frame.txt", 'wt')
physicalvelfile = open(path3 + "/Pixel_Velocity_Stat.txt", 'wt')
physicalvelfile2 = open(path3 + "/Pixel_Velocity_per_frame.txt", 'wt')

file = open(path3 + "/Mouse_Name_Centers.txt").read()
centerlocation = [item.split() for item in file.split(';\n')][:-1]

distance = 0
#print(centerlocation)

#z = []
#i = 0
#for x in centerlocation:
#    for y in x:
#        y = int(y)
#        z.append(y) 
#        #print y
        
#        
#clocx = z[::2]
#clocy = z[1::2]
clocx = np.load(path3 + "/Center_X.npy")
clocy = np.load(path3 + "/Center_Y.npy")
stopwatch = np.load(path3 + "/Time.npy")
entrynum = len(clocx)
print(entrynum)

#==============================================================================
# Distance calculation
#==============================================================================
    
for j in range(1, entrynum):

    pdist = math.sqrt((clocx[j] - clocx[j-1])**2 + (clocy[j] - clocy[j-1])**2)
    distfile2.write("%s;\n" %pdist)
    pdista.append(pdist)
    
    physicaldist = pdist * factor          #Conversion from pixel length into physcial length (cm)
    dista.append(physicaldist)    
    physicaldistf2.write("%s\n" %physicaldist)
    
    deltatime = stopwatch[j] - stopwatch[j-1]    
    currentvel = pdist / deltatime
    velfile2.write("%s;\n" %currentvel)
    physicalvelfile2.write("%s;\n" %(currentvel*factor))
    pvelocity.append(currentvel)    #0.5235 SHOULD BE REPLACED WITH ToF File that contains accurate time.
    totaldist = totaldist + pdist
    velocity.append(currentvel*factor)
    
#==============================================================================
# Distance Statistics
#==============================================================================
meandist = statistics.mean(dista)
mediandist = statistics.median(dista)
stddist = statistics.stdev(dista)
variancedist = statistics.variance(dista)
physicaldistf.write("%s\n%s\n%s\n%s" %(meandist,mediandist,stddist,variancedist))


#==============================================================================
# Conversion to physical length
#==============================================================================
pmeandist = meandist*factor
pmediandist = mediandist*factor
pstddist = stddist*factor
pvariancedist = variancedist*factor
distfile.write("%s\n%s\n%s\n%s" %(pmeandist,pmediandist,pstddist,pvariancedist))


#==============================================================================
# Velocity Statistics
#==============================================================================
meanvel = statistics.mean(velocity)
medianvel = statistics.median(velocity)
stdvel = statistics.stdev(velocity)
variancevel = statistics.variance(velocity)
velfile.write("%s\n%s\n%s\n%s" %(meanvel,medianvel,stdvel,variancevel))
physicalvelfile.write("%s\n%s\n%s\n%s" %(meanvel*factor,medianvel*factor,stdvel*factor,variancevel*factor))
#==============================================================================
# NumPy Array File Saving
#==============================================================================
np.save(path3 + "/pixdist.npy", pdista)
np.save(path3 + "/cmdist.npy", dista)

np.save(path3 + "/pixvelocity.npy", pvelocity)
np.save(path3 + "/cmvelocity.npy", velocity)

#plt.plot(range(0, entrynum),pvelocity)
plt.figure(1)
plt.subplot(311)
plt.title("Traveled distance vs time")

plt.plot(stopwatch[0:entrynum],dista)
plt.ylabel("Distance (cm)")
plt.xlabel("Time (s)")

plt.subplot(312)
plt.title("Velocity vs Time")
plt.plot(stopwatch[0:entrynum], velocity)
#plt.plot(stopwatch[1:len(stopwatch)], velocity)
plt.ylabel("Velocity (cm/s)")
plt.xlabel("Time (s)")

plt.subplot(313)
plt.title("Scatter Plot")
plt.scatter(clocx,clocy, c=clocx)
plt.ylim((0,928))
plt.xlim((0,1648))
plt.gca().invert_yaxis()


distfile.close
distfile2.close
physicaldistf.close
physicaldistf2.close
velfile.close
velfile2.close
physicalvelfile.close
physicalvelfile2.close