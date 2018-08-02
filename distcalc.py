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
import pylab
#import seaborn as sns


totaldist = [0]
velocity = [0]
pvelocity = [0]
pdista = [0]
dista = [0]
factorx = 0.019256 # Scaling factor for pixels to cm
factory = 0.019256
area = np.zeros(6)
percentarea = np.zeros(6)
#physicaldista = []
#timetemp = 0.5305
#deltatime = timetemp

path = raw_input("Enter the path of the folder you wish to analyze:\n")
path3 = path+ "/Information"

distfile = open(path3 + "/Total_Distance.txt", 'wt')
distfile2 = open(path3 + "/Distance_per_frame.txt", 'wt')
physicaldistf2 = open(path3 + "/Pixel_dist_per_frame.txt",'wt')
physicaldistf = open(path3 + "/Pixel_dist_stats.txt",'wt')
velfile = open(path3 + "/Velocity_Stat.txt", 'wt')
velfile2 = open(path3 + "/Velocity_per_frame.txt", 'wt')
#physicalvelfile = open(path3 + "/Pixel_Velocity_Stat.txt", 'wt')
#physicalvelfile2 = open(path3 + "/Pixel_Velocity_per_frame.txt", 'wt')

#centerlocation = [item.split() for item in file.split(';\n')][:-1]

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
#entrynum = 20992
print(entrynum)
area = np.zeros(6)


#==============================================================================
# Distance calculation
#==============================================================================
    
for j in range(1, entrynum):
    
#==============================================================================
#     Area histogram
#==============================================================================
    if clocy[j] <= 464:
        if clocx[j] <= 549:
            area[0] += 1
        elif clocx[j] >549 and clocx[j] <=1099:
            area[1] += 1
        else:
            area[2] += 1
    elif clocy[j] > 464:
        if clocx[j] <= 549:
            area[5] += 1
        elif clocx[j] >549 and clocx[j] <=1099:
            area[4] += 1
        else:
            area[3] += 1
#==============================================================================
# Calculating Pixel Distance
#==============================================================================
    pdist = math.sqrt((clocx[j] - clocx[j-1])**2 + (clocy[j] - clocy[j-1])**2)
    distfile2.write("%s;\n" %pdist)
    pdista.append(pdist)
    
#==============================================================================
# Calculating Physical Distance
#==============================================================================
    physicaldist = math.sqrt(((clocx[j] - clocx[j-1])*factorx)**2 + ((clocy[j] - clocy[j-1])*factory)**2)       #Conversion from pixel length into physcial length (cm)
    
    td = int(totaldist[j-1] + (physicaldist))
    totaldist.append(td)
    
    #Distance inbetween frames
    dista.append(physicaldist)    
    physicaldistf2.write("%s\n" %physicaldist)
    
    deltatime = stopwatch[j] - stopwatch[j-1]
    pixelcurrentvel = pdist/deltatime
    pvelocity.append(pixelcurrentvel)    
    currentvel = physicaldist / deltatime
    velfile2.write("%s;\n" %currentvel)
#    physicalvelfile2.write("%s;\n" %(currentvel))
#    pvelocity.append(currentvel)    #0.5235 SHOULD BE REPLACED WITH ToF File that contains accurate time.
    #totaldist = totaldist + pdist
    velocity.append(currentvel)
    
#==============================================================================
# Physical Distance Statistics
#==============================================================================
meandist = statistics.mean(dista)
mediandist = statistics.median(dista)
stddist = statistics.stdev(dista)
variancedist = statistics.variance(dista)
physicaldistf.write("%s; %s; %s; %s" %(meandist,mediandist,stddist,variancedist))

areasum = sum(area)
for i in range(0,6):
    percentarea[i] = area[i]/areasum*100

#==============================================================================
# Pixel Distance Statistics
#==============================================================================
pmeandist = statistics.mean(pdista)
pmediandist = statistics.median(pdista)
pstddist = statistics.stdev(pdista)
pvariancedist = statistics.variance(pdista)
distfile.write("%s" %td)


#==============================================================================
# Velocity Statistics
#==============================================================================
meanvel = statistics.mean(velocity)
medianvel = statistics.median(velocity)
stdvel = statistics.stdev(velocity)
variancevel = statistics.variance(velocity)

velfile.write("%s; %s; %s; %s" %(meanvel,medianvel,stdvel,variancevel))
#physicalvelfile.write("%s; %s; %s; %s" %(meanvel,medianvel,stdvel,variancevel))
#==============================================================================
# NumPy Array File Saving
#==============================================================================
np.save(path3 + "/pixdist.npy", pdista)
np.save(path3 + "/cmdist.npy", dista)

np.save(path3 + "/pixvelocity.npy", pvelocity)
np.save(path3 + "/cmvelocity.npy", velocity)

#plt.plot(range(0, entrynum),pvelocity)
plt.figure(4)
plt.title("Traveled distance vs time")
plt.plot(stopwatch[0:entrynum],totaldist)
#plt.plot(range(0,entrynum),totaldist)
plt.ylabel("Distance")
plt.xlabel("Time (s)")
#plt.xlabel("Frames")
plt.savefig(path3 + "/Distance_over_time.jpeg")

plt.figure(1)
plt.figure(figsize=(15,10))
plt.title("Position vs Time")
plt.plot(stopwatch[0:entrynum], velocity)
#plt.plot(range(0,entrynum), velocity)
plt.ylabel("Distance (cm)")
plt.xlabel("Time (s)")
#plt.xlabel("Frames")
plt.savefig(path3 + "/Pos_v_Time.jpeg")


plt.figure(2)
#plt.title("Scatter Plot")
#plt.scatter(clocx,clocy, c=clocx)
#plt.ylim((0,928))
#plt.xlim((0,1648))
#plt.gca().invert_yaxis()
plt.figure(figsize=(15,10))
x = np.arange(6)
plt.bar(x, percentarea, color ="red")
plt.xticks(x+.5, ["TL", "TM", "TR", "BR", "BM", "BL"])
plt.ylabel("Percent of time spent in area")
plt.xlabel("Area")
plt.axis(ymin=0, ymax=100)
plt.savefig(path3 + "/Area_Histogram.jpeg")


plt.figure(3)
plt.figure(figsize=(15,10))
plt.title("Scatter Plot")
colors = np.linspace(0,entrynum*0.5,entrynum) #assuming 2fps
im=plt.imread(path + "/firstframe.jpeg")
plt.imshow(im, zorder=1)
plt.scatter(clocx,clocy, c=colors, cmap=pylab.cm.viridis, zorder=2)
plt.colorbar()
plt.ylim((0,928))
plt.xlim((0,1648))
plt.gca().invert_yaxis()
plt.savefig(path3 + "/Scatterplot.jpeg")
plt.show()

distfile.close
distfile2.close
physicaldistf.close
physicaldistf2.close
velfile.close
velfile2.close
#physicalvelfile.close
#physicalvelfile2.close
