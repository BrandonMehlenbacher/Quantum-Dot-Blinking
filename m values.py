# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 22:21:54 2018

@author: bmehl
"""
import numpy as np
import xlrd
import xlwt
def bringing_in_data_cum(name,sheet,m):
    book = xlrd.open_workbook(name+'.xls')
    sheet = book.sheet_by_name(sheet)
    data = [sheet.cell_value(r, m) for r in range(0,3000)]
    return data
#determines whether a value is above or below a threshold and builds a list of true and false statements
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
def building_cum_set(spreadsheet,worksheet,Sheet,filename):
    book = xlwt.Workbook()
    ws = book.add_sheet(Sheet)
    on_list_total = []
    off_list_total = []
    columns = int(input("Please specify number of columns:"))
    for x in range(columns):
        my_data = bringing_in_data_cum(spreadsheet,worksheet,(x))
        threshold  = float(input("Please input threshold value:"))
        my_list1 = threshold_calculation(my_data,threshold)
        on_list = determining_on_off(my_list1)
        on_list_total.append(on_list[0])
        off_list_total.append(on_list[1])
    on_list_total_flat = flat_list(on_list_total)
    off_list_total_flat = flat_list(off_list_total)
    for i, y in enumerate(on_list_total_flat):
        ws.write(i, 0 , y)
    for j, z in enumerate(off_list_total_flat):
        ws.write(j, 1 , z)
    book.save(filename+".xls")
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
def finding_mON_mOFF(Sheet,filename,histogram_on):
    book = xlwt.Workbook()
    ws = book.add_sheet(Sheet)
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
    book.save(filename+".xls")
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
    mON = finding_mON_mOFF('ON','ON_result',histogram_on1)
    mOFF = finding_mON_mOFF('OFF','OFF_result',histogram_off1)
    return mON , mOFF
#def mONmOFFvalues(result1,sheet1):
on_data1 = bringing_in_data(result1,sheet1,0)
on_data2 = []
for x in on_data1:
    if x == '':
        pass
    else:
        on_data2.append(int(x))
        off_data1 = bringing_in_data(result1,sheet1,1)
        off_data2 = []
    for y in off_data1:
        if y == '':
            pass
        else:
            off_data2.append(int(y))
mON_cum = cumulative_data(on_data2,off_data2)[0]
mOFF_cum = cumulative_data(on_data2,off_data2)[1]
print(mON_cum)
print(mOFF_cum)
    