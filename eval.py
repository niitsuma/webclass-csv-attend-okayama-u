#coding: UTF-8

import csv
import commands
import os
import codecs
import ast
import glob
import dateutil.parser
from collections import defaultdict
import datetime


default_day=-1
default_id=-1
root_dict=defaultdict(lambda : default_id)
name_dict=defaultdict(lambda : default_id)
day_set=set([])

starttime_dict=defaultdict(int)

def update_name_dic(id,name,num,dic):
    if dic[id] == default_id :
        dic[id]= {'name' : name , 'num':num}
    else :
        if dic[id]['name'] <> name :
            print id, name
        if dic[id]['num'] <> num :
            print id, num
    return dic


def update_day_time_dict(dt,dic):
    d=dt.date()
    day_set.add(d)
    if dic[d] == default_day :
        dic[d]=dt
    elif dic[d] > dt :
        dic[d]=dt

    return dic

def update_id_dict(dt,id,dic):
    if dic[id] == default_id :
        tmp_day_dict = defaultdict(lambda : default_day)
        dic[id]= update_day_time_dict(dt,tmp_day_dict )
    else :
        dic[id]= update_day_time_dict(dt,dic[id])   
    return dic

if __name__ == "__main__":
    files = glob.glob('all-utf/*.csv*')
    for file in files:
    #     print file
    #file="出席者12020858.csv"
        csv_reader = csv.reader(open(file, 'rb'), dialect="excel")
        csv_list=list(csv_reader)
        for n in range(1,len(csv_list)):
            id= csv_list[n][0]
            
            dt=dateutil.parser.parse(csv_list[n][5])
            update_id_dict(dt,id,root_dict)
            name= csv_list[n][1]
            num= csv_list[n][2]
            update_name_dic(id,name,num,name_dict)

    print day_set
    day_list=list(day_set)
    day_list=sorted(day_list)
    print day_list
    
        
    starttime_dict={d:min([root_dict[id][d] for id in root_dict if root_dict[id][d] <> default_day])
                        for 
                        d in day_list}
        
    ff = open('attend-flag.csv', 'ab')
    ft = open('attend-time.csv', 'ab')
    csvWriter_t = csv.writer(ft)
    csvWriter_f = csv.writer(ff)

    lis_f=[-1]
    for d in day_list :
        dstr=("%s" % d)
        lis_f.append(dstr)
    print lis_f
    csvWriter_f.writerow(lis_f)        

    for id in root_dict:
        lis=[]
        lis_t=[]
        lis_f=[]
        lis_t.append(id)
        lis_f.append(id)

        for d in day_list :
            if root_dict[id][d] == default_day :
                lis_t.append(root_dict[id][d])
                lis_f.append(root_dict[id][d])
            else :
                dt=root_dict[id][d]
                t=dt.time()
                dtstr=("%s" % root_dict[id][d])
                lis_t.append(dtstr)
                t1=datetime.datetime(2000, 10, 10, 9, 0 , 0).time() ##edit your lecture start time
                t1b=starttime_dict[d].time()
                t2=datetime.datetime(2000, 10, 10, 9, 50, 0).time() ##edit your lecture late limit time
                if t > t2 :
                    lis_f.append(-1)
                elif t > t1 and t > t1b:
                    lis_f.append(0)
                else :
                    lis_f.append(1)
                
                
                
        lis_t.append(name_dict[id]['num'])
        lis_f.append(name_dict[id]['num'])
        lis_t.append(name_dict[id]['name'])
        lis_f.append(name_dict[id]['name'])

        csvWriter_t.writerow(lis_t)
        csvWriter_f.writerow(lis_f)    
    ff.close()
    ft.close()                  

   
