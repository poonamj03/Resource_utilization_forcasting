

#import all the libraries
import os
from os import listdir
from os.path import isfile, join
import re
from dateutil.parser import parse
import pandas as pd
import datetime
from itertools import groupby
import matplotlib.pyplot as plt


#1.System should convert given data into required data model. This stage generates `input-data`.
'''
"{timestamp}:{Memory Allocated}:{Memory Used}:{CPU Allocated}:{CPU_Used}:
# {Network bandwidth utilization}:{Storage space utilization}"
'''

'''
Given the data-set below, following are the expected results from the system,
1. Predictions per Instance (required)
2. Predictions per Group (required)
3. Predictions per Resource (CPU/Memory/Network/Storage) per group or per
instance (optional)
'''

def get_file_names(path):
    arr = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(mypath):
        for file in f:
            if file.endswith(".log"):
                arr.append(os.path.join(r, file))  #array of all file names
    return arr

def input_data(path):
    # Go through the each folder using os and os.path.join in recursive manner
    arr = get_file_names(path)


    '''
    arr_gp1=[]
    arr_gp2=[]
    arr_gp3=[]
    arr_gp4=[]

    for gp in arr:
        #print(gp1[len(mypath)+7:len(mypath)+8])
        if gp[len(mypath)+7:len(mypath)+9] == '1_':
            arr_gp1.append(gp)
        if gp[len(mypath)+7:len(mypath)+9] == '2_':
            arr_gp2.append(gp)
        if gp[len(mypath)+7:len(mypath)+9] == '3_':
            arr_gp3.append(gp)
        if gp[len(mypath)+7:len(mypath)+9] == '4_':
            arr_gp4.append(gp)
    print('Total no of instances in group ',len(arr_gp1))
    '''

    #print(arr[1])
    xxx=[]
    data2 = []   #store each column separately
    data_cpu1=[]
    data_Memory_use1=[]
    for x in [arr[1]]:#[arr_gp1[5]]:#,arr_gp1[6], arr_gp1[7], arr_gp1[8], arr_gp1[9]]:

        print(x)
        ############ 3 create a columns or each feature using the suitable separator
        with open(x,"r") as file:  #read single instance
            data = file.read()
            #print(type(data))
            xx = data.split('\n')

        for xx1 in xx:
            #print(xx1)            #Result : "Tue Jun 23 19:01:44 IST 2020":"65536:65530:6:0.10:0.00:905G"
            xx2 = xx1.split('"')
            #print(xx2)            #Result : ['', 'Tue Jun 23 18:51:15 IST 2020', ':', '65536:65530:6:0.12:0.00:905G', '']
            x_update = [x1 for x1 in xx2 if x1 != ':' and x1 != '']  #parse data using splitter
            #print(x_update)       #Result : ['Tue Jun 23 19:40:57 IST 2020', '65536:65530:6:0.12:0.00:905G']
            if x_update:
                xxx.append(x_update)
                #print(xxx[1])
        for xx1 in xxx:
            timestamp = xx1[0]
            Memory_Allocated, Memory_Used, CPU_Allocated, CPU_Used, Network_bandwidth_utilization, Storage_space_utilization =  xx1[1].split(':')
            week, month, date, time,_,year=timestamp.split()
            oout = parse(timestamp)
            date_time1, _=str(oout).split('+')# datetime.datetime.strptime(year-month-date, '%Y-%m-%d').date()
            #print(Memory_Allocated, Memory_Used, CPU_Allocated, CPU_Used, Network_bandwidth_utilization, Storage_space_utilization)
            groupNo = x[len(mypath)+7:len(mypath)+8]
            groupID = x[len(mypath)+9:len(mypath)+45]
            data2.append([date_time1,groupNo,groupID, Memory_Allocated, Memory_Used, CPU_Allocated, CPU_Used, Network_bandwidth_utilization, Storage_space_utilization])
            data_cpu1.append([date_time1,CPU_Used])
            data_Memory_use1.append([date_time1,Memory_Used])

        ############ 4. Convert it inot the datarame using created columns
        df=pd.DataFrame(data2)
        data_cpu = pd.DataFrame(data_cpu1)
        data_Memory_use = pd.DataFrame(data_Memory_use1)

        df.columns = ['timestamp','groupNo','groupID','Memory_Allocated','Memory_Used', 'CPU_Allocated', 'CPU_Used', 'Network_bandwidth_utilization', 'Storage_space_utilization']
        data_cpu.columns = ['timestamp','CPU_Used']
        data_Memory_use.columns = ['timestamp', 'Memory_Allocated']

        #df.set_index("timestamp", inplace = True)  #will set the timestamp as rows_name
        #data_cpu.set_index("timestamp", inplace = True)  #will set the timestamp as rows_name
        #data_Memory_use.set_index("timestamp", inplace = True)  #will set the timestamp as rows_name

    #print(df)
    return df, data_cpu, data_Memory_use

####################   1.Getting the current work directory (cwd)
mypath = '/home/poonam/Downloads/future_predictions_on_grocessary store/group82_resource_utilization'

df, data_cpu, data_Memory_use = input_data(mypath)
#df.to_csv('group1_ID5_all_data.csv', mode='a', header=False)
#data_cpu.to_csv('group1_ID5_CPU_index.csv', mode='a', header=False)
#data_Memory_use.to_csv('group1_ID5_Memory_index.csv', mode='a', header=False)
#data_cpu['Month']=pd.to_datetime(data_cpu['timestamp'], format='%Y-%m-%d')
#data_cpu.set_index(['timestamp'], inplace=True)

print('\n\n **********   Generated DataFrame  ********** ')
print(df.head())

print('\n\n**********   Data used for the CPU_USage ********** ')
print(data_cpu.head())

print('\n\n ********** Data used for the Memory_USage ********** ')
print(data_Memory_use.head())

#2. System should implement relevant and required data cleaning and data
#transformations techniques in the input data. This stage generates `pre-processed-data`.

def pre_processed_data():
    pass

#3. System should (if required) perform training on pre-processed-data and
#generate machine learning model. This stage will generate a `model`.

def model():
    #return model
    # arima_model2.py
    pass

#4. System should process pre-processed-data and generate prediction
#results. This stage generates `predicted-transactions`.
def predicted_transactions():
    pass

#Steps for data-input
#1.Getting the current work directory (cwd)
#2.go through the each folder using os and os.path.join in recursive manner
#3 create a columns or each feature using the suitable separator
#4. Convert it inot the datarame using created columns

data_cpu['Month']=pd.to_datetime(data_cpu['timestamp'], format='%Y-%m-%d')


fig, ax = plt.subplots()
#plt.plot(data_cpu['CPU_Used'])

ax.plot(data_cpu['Month'].index.values[3000:3500],
           data_cpu['CPU_Used'][3000:3500],
           color='purple')

ax.set(xlabel="Date",
       ylabel="CPU Usage",
       title="CPU Usage\n 2019-2020")
plt.show()


# Plot the data of CPU USED

#df.plot()
plt.ylabel('CPU Used in all the instance')
plt.xlabel('Date')
plt.savefig('Group 1 - CPU Used in all the instance .png')
plt.show()

#plt.plot(df['timestamp'], data_cpu['CPU_Used'])
#plt.show()

# Plot the data of CPU USED
plt.plot(data_cpu['month'], data_cpu['CPU_Used'])
#plt.plot(data['CPU_Used'])
plt.ylabel('Group 1 - Monthly Memory Used by all server')
plt.xlabel('Date')
plt.show()
#plt.savefig('Group 1 - Monthly CPU Used by all server.png')

'''
# Plot the data of CPU USED
#plt.plot(data_Memory_use['Month'], data_Memory_use['Memory_Allocated'])
data_Memory_use.plot()#data['CPU_Used'])
plt.ylabel('Group 1 - Monthly Memory Used by all server')
plt.xlabel('Date')
plt.show()
plt.savefig('Group 1 - Monthly Memory Used by all server.png')
'''
