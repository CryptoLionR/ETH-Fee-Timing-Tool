import numpy as np
import urllib.request as rq
import json
import pandas as pd
import time

#based on the flipcoin api data
url = 'https://api.flipsidecrypto.com/api/v2/queries/a8f048e1-e99e-49b1-a659-cb4608b2a818/data/latest'
try:
    dataset = rq.urlopen(url)
    dataset = dataset.read()
    dataset = json.loads(dataset)
except Exception as e:
    print('Unable to get data from flipsidecrypto API. Check the URL below: \n{}'.format(url))

#simplify hour values *note HOURS in UTC
for i,item in enumerate(dataset):
    dataset[i]['HOUR'] = item['HOUR'].split('T')[1].rsplit(':')[0]
#sort ascending hours
dataset = sorted(dataset,key=lambda hour: hour['HOUR'])

#get pandas df
dataset = pd.DataFrame(dataset)
hourly_avgs = []

#get timezone of local machine
timezone_offset = time.timezone/3600

#calculate and print overall average fee
fee_avg = np.percentile(dataset['AVERAGE_FEE'],50)
print("Hourly Average Transaction Fee over past 5 days: ${:.2f} USD".format(fee_avg))

start_slice = 0
counter = 1

while counter < len(dataset):
    if dataset['HOUR'][counter] == dataset['HOUR'][counter-1]:
        None
    else:
        hourly_avgs.append({
            'HOUR' : dataset['HOUR'][counter-1], 
            'AVERAGE_FEE' : np.average(dataset['AVERAGE_FEE'][start_slice:counter])
            })
        start_slice = counter
    counter+=1

hourly_avgs.append({
            'HOUR' : dataset['HOUR'][counter-1], 
            'AVERAGE_FEE' : np.average(dataset['AVERAGE_FEE'][start_slice:counter])
            })

del dataset,start_slice,counter

counter = 0
while counter < len(hourly_avgs):
    if int(hourly_avgs[counter]['HOUR']) - timezone_offset < 0:
        hourly_avgs[counter]['HOUR'] = int(hourly_avgs[counter]['HOUR']) + 24 - timezone_offset
    else:
        hourly_avgs[counter]['HOUR'] = int(hourly_avgs[counter]['HOUR']) - timezone_offset
    counter+=1
hourly_avgs = sorted(hourly_avgs,key=lambda hour: hour['HOUR'])

for elem in hourly_avgs:
    if elem['AVERAGE_FEE'] < fee_avg:
        print("[{:02d}:00]:~${:.2f} USD".format(int(elem['HOUR']),elem['AVERAGE_FEE']))
print('NOTE: Hours are in Local Time ({})\n'.format(time.tzname[0]))
x = input('Press X to exit')