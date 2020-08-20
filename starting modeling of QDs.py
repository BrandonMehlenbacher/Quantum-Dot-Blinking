# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 15:11:59 2018

@author: bmehl
"""
import random
import scipy.integrate as integrate
import math
import time as ti
import matplotlib.pyplot as plt
import numpy as np
from heapq import nsmallest
import xlwt

def determining_on_off(sequence): 
    n = 0 
    t = 0 
    on_list = [] 
    m = 0 
    off_list = [] 
    count = 0 
    for x in sequence: 
        if count == 0: 
            t = x
            if x == 1:
                n += 1
            else:
                n += 1
            count += 1 
        else: 
            if t == x: 
                if t == 1: 
                    n += 1 
                else: 
                    m += 1 
            else: 
                if t == 1: 
                    on_list.append(n) 
                    n = 0
                    t = x
                    m += 1
                else: 
                    off_list.append(m) 
                    m = 0 
                    t = x
                    n += 1
    return on_list,off_list
def threshold_calculation(intensities,threshold):
    my_list = []
    for x in intensities:
        if x > threshold:
            my_list.append(1)
        else:
            my_list.append(0)
    return my_list
def flat_list(array):
    r = []
    while len(array) > 0:
        l = array.pop()
        if hasattr(l, "__iter__"):
            array.extend(l)
        else:
            r.append(l)
    return r[::-1]
import xlwt
def finding_mON_mOFF(histogram_on):
# =============================================================================
#     book = xlwt.Workbook()
#     ws = book.add_sheet(Sheet)
# =============================================================================
    count = 1
    for x in histogram_on:
        if x[1] == 0:
            histogram_on =  np.delete(histogram_on, (int((x[0]-count))),axis=0)
            count += 1
    count = 0
    count1 = 0
    list_times_on = []
    total_on_events = 0
    probability_on = []
    list_average_times = [.1106]
    probability_density = []
    log_times_on = []
    log_probability_density = []
    for y in histogram_on:
        list_times_on.append(.1106*y[0])
    for z in histogram_on:
        total_on_events = total_on_events + z[1]
    for a in histogram_on:
        probability_on.append(a[1]/total_on_events)
    while True:
        if list_times_on[count] == max(list_times_on[0:int(len(list_times_on)-1)]):
            break
        else:
            list_average_times.append((list_times_on[count+2]-list_times_on[count])*.5)
            count += 1
    for d in list_average_times:
        probability_density.append(probability_on[count1]/d)
        count1 += 1
    for b in list_times_on:
        log_times_on.append(np.log10(b))
    log_times_on = np.delete(log_times_on, (len(log_times_on)-1))
    for c in probability_density:
        log_probability_density.append(np.log10(c))
    mON = np.polyfit(log_times_on,log_probability_density,1)
    return (mON[0])
    
def cumulative_data(on_list,off_list):
    on_list.sort()
    off_list.sort()
    time_bin_on = np.delete(np.histogram(on_list,bins=(max(on_list)), range=(1,max(on_list)+1))[1],[int(max(on_list))])
    time_bin_off = np.delete(np.histogram(off_list,bins=(max(off_list)), range=(1,max(off_list)+1))[1],[int(max(off_list))])
    occurences_on = np.histogram(on_list,bins=(max(on_list)), range=(1,max(on_list)+1))[0]
    occurences_off = np.histogram(off_list,bins=(max(off_list)), range=(1,max(off_list)+1))[0]
    histogram_on1 = np.vstack((time_bin_on,occurences_on)).T
    histogram_off1 = np.vstack((time_bin_off,occurences_off)).T
    mON = finding_mON_mOFF(histogram_on1)
    mOFF = finding_mON_mOFF(histogram_off1)
    return mON , mOFF    
# =============================================================================
#     for l, n in enumerate(list_times_on):
#         ws.write(l, 0 , n)
#     for f, w in enumerate(list_average_times):
#         ws.write(f, 1 , w)
#     for m, o in enumerate(probability_on):
#         ws.write(m, 2 , o)
#     for k, p in enumerate(probability_density):
#         ws.write(k, 3 , p)
#     for i, y in enumerate(log_times_on):
#         ws.write(i, 4 , y)
#     for j, z in enumerate(log_probability_density):
#         ws.write(j, 5 , z)
#     book.save(filename+".xls")
# =============================================================================
    return (mON[0])
# =============================================================================
# class trapStates(object):
#     def __init__ (self):
#         self.energy = random.randint(500,610)
#         self.filled = False
#     def getEnergy(self):
#         return self.energy
#     def getFilled(self):
#         return self.filled
#     def changeFilled(self):
#         self.filled  = not self.filled
#     def probabilityChange(self):
#         if random.random() > .4:
#             trapStates.changeFilled(self)
#             
# class quantumDot(object):
#     def __init__ (self,energy,trapstates):
#         self.energy = energy
#         self.intensityOFF  = .01
#         self.intensityON = 1
#         self.trapstates = trapstates
#     def getEnergy(self):
#         return self.energy
#     def getIntensityON(self):
#         return self.intensityON
#     def getIntensityOFF(self):
#         return self.intensityOFF
#     def getPopulation(self):
#         count = 0
#         for x in self.trapstates:
#             if x.getFilled:
#                 count += 1
#             return count
#     def changeIntensityON(self):
#         self.intensityON = (10000/(10000+2000+self.getPopulation()*1000))
#     def changeIntnesityOFF(self):
#         self.intensityOFF = 1000/(1000+10000+self.getPopulation()*1000)
#     def updates(self):
#         for x in self.trapstates:
#             x.probabilityChange()
# =============================================================================
time = range(1,1501)
def generate_weighted_list(time,m,ct):
    weighted_list = []
    A = 1/(integrate.quad(lambda x: x**(-m)*math.exp(-x/ct),.11,math.inf)[0])
    time  = range(time)
    for x in time:
        weighted_list.append((A*((x/(9.09)+.11)**(-m)*(math.exp(-(x/(9.09)+.11)/ct))))*.1106)
    return weighted_list
def generateTime(events,weight):
    for x in range(events):
        val = random.choices(time,weights = weight, k = events)
    return sorted(val)
surfacearea = int(input("whats the surface area of the material?: "))
# =============================================================================
# trapstates = []
# intensityON = []
# for x in range((int(surfacearea/24))*10):
#     trapstates.append(trapStates())
# qd = quantumDot(525,trapstates)
# qd.updates()
# =============================================================================
startTime = ti.clock()
intensity = []
mON = 1.60
mOFF = 1.60
weightON = generate_weighted_list(1500,mON,math.inf)
weightOFF = generate_weighted_list(1500,mOFF,math.inf)
eventsON = random.randint(1000,1500)
eventsOFF = random.randint(1000,1500)
timeON  = generateTime(eventsON,weightON)
timeOFF = generateTime(eventsOFF,weightOFF)
# =============================================================================
# timeONintensity = []
# timeOFFintensity = []
# =============================================================================
# =============================================================================
# trapstates = []
# intensityON = []
# =============================================================================
# =============================================================================
# for x in range((int(surfacearea/24))*10):
#     trapstates.append(trapStates())
# qd = quantumDot(525,trapstates)
# for x in timeON:
#     intensityONfill = []
#     for y in range(x):
#         qd.updates()
#         qd.changeIntensityON()
#         intensityONfill.append(qd.getIntensityON())
#     intensityON.append(intensityONfill)
# print(intensityON)
# =============================================================================
timestart = ti.clock()
mON = 1.60
mOFF = 1.60
intensitylist = []
intensityweight = []
mONlist = []
mOFFlist = []
avgOFF = []
avgON = []
trapeffect = .1
weightON = generate_weighted_list(1500,mON,math.inf)
weightOFF = generate_weighted_list(1500,mOFF,math.inf)
for x in range((int(surfacearea/24))*10):
    intensitylist.append(x*trapeffect)
    if x <= int(surfacearea/24)*5:
        intensityweight.append(x/(int(surfacearea/24))*10)
    else:
        intensityweight.append(((int(surfacearea/24))*10-x)/(int(surfacearea/24))*10)
for y in range(1):
    intensity = []
    eventsON = random.randint(1400,1500)
    eventsOFF = random.randint(1400,1500)
    timeON  = generateTime(eventsON,weightON)
    timeOFF = generateTime(eventsOFF,weightOFF)
    for x in range(len(timeON)+len(timeOFF)):
        if random.randint(0,1) == 1:
            if timeON == []:
                value = random.choices(timeOFF)
                for x in range(value[0]):
                    intensityOFF = random.choices(intensitylist, weights = intensityweight, k = 1)
                    qy = 1/(1+10+intensityOFF[0])
                    intensity.append(qy)
                timeOFF.remove(value[0])
            else:
                value = random.choices(timeON)
                for x in range(value[0]):
                    intensityON = random.choices(intensitylist, weights = intensityweight, k = 1)
                    qy = 10/(10+1+intensityON[0])
                    intensity.append(qy)
                timeON.remove(value[0])
        else:
            if timeOFF == []:
                value = random.choices(timeON)
                for x in range(value[0]):
                    intensityON = random.choices(intensitylist, weights = intensityweight, k = 1)
                    qy = 10/(10+1+intensityON[0])
                    intensity.append(qy)
                timeON.remove(value[0])
            else:
                value = random.choices(timeOFF)
                for x in range(value[0]):
                    intensityOFF = random.choices(intensitylist, weights = intensityweight, k = 1)
                    qy = 1/(1+10+intensityOFF[0])
                    intensity.append(qy)
                timeOFF.remove(value[0])
    count = 0
    count1 = 0
    x = range(0,len(intensity))
# =============================================================================
#     plt.figure(figsize=(20,5))
#     plt.plot(x,intensity)
#     plt.axis([0, 50000, 0, 1])
#     ax = plt.axes()
#     ax.xaxis.set_major_locator(plt.MaxNLocator(40))
#     plt.show()
# =============================================================================
    #x = int(input("where does off start: "))
   # y = int(input("where does off end: "))
    avgOFFint = np.average(nsmallest(26000,intensity))
    stdOFFint = np.std(nsmallest(26000,intensity),dtype = np.float64)
  #  avgOFFint1 = np.average(intensity[x:y])
   # stdOFFint1 = np.std(intensity[x:y],dtype = np.float64)
    intvalue = avgOFFint+4*stdOFFint
    #intvalue1 = avgOFFint1+3*stdOFFint1
    for x in intensity:
        if x > intvalue:
            count += 1
        else:
            count1 += 1
    avgON.append(count/(count1+count))
    avgOFF.append(count1/(count+count1))
    intensitythres = threshold_calculation(intensity,intvalue)
    mylist = determining_on_off(intensitythres)
    mON_cum = cumulative_data(mylist[0],mylist[1])[0]
    mOFF_cum = cumulative_data(mylist[0],mylist[1])[1]
    mONlist.append(mON_cum)
    mOFFlist.append(mOFF_cum)
print(np.average(mONlist))
print(np.std(mONlist))
print(np.average(mOFFlist))
print(np.std(mOFFlist))
print(np.average(avgON))
print(np.std(avgON))
print(np.average(avgOFF))
print(np.std(avgOFF))
timeend = ti.clock()
print(timeend-timestart)


book = xlwt.Workbook()
ws = book.add_sheet(Sheet1)




for l, n in enumerate(list_times_on):
    ws.write(l, 0 , n)
for f, w in enumerate(list_average_times):
    ws.write(f, 1 , w)
for m, o in enumerate(probability_on):
    ws.write(m, 2 , o)
for k, p in enumerate(probability_density):
    ws.write(k, 3 , p)
for i, y in enumerate(log_times_on):
    ws.write(i, 4 , y)
for j, z in enumerate(log_probability_density):
    ws.write(j, 5 , z)
book.save(finalresult+".xls")





