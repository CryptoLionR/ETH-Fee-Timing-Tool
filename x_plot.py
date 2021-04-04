import numpy as np
import urllib.request as rq
import json
from collections import Counter as c
import time

from matplotlib import pyplot as plt

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

#empty inits
fee = []
indexes = []
hours = []
hours_dict = []
counter = 0
threshold = None
#get timezone of local machine
timezone_offset = time.timezone/3600

#calculate and print overall average fee
for elem in dataset:
    fee.append(elem['AVERAGE_FEE'])
fee_avg = np.percentile(fee,50)
print("Hourly Average Transaction Fee over past 5 days: ${:.2f} USD".format(fee_avg))

# for i,elem in enumerate(fee):
#     if fee_avg > elem:
#         indexes.append(i)

for i,element in enumerate(dataset):
    # if indexes[counter] == i:
        hours.append(element['HOUR'])
        # counter+=1
        # if counter >= len(indexes):
        #     break

hour_freq = c(hours)

counter = 0
toprint = []
#calculate the hour average over 5 day period
for key, value in hour_freq.items():
    avg = 0
    c = 0
    if value >= 4:
        #iterate through the dataset to get fee values
        while counter < len(dataset):
            if key not in dataset[counter]['HOUR']:
                break
            else:
                avg+= dataset[counter]['AVERAGE_FEE']
                c+=1
                counter+=1
            
        if avg != 0:
            avg = avg/c

        #translate to local timezone
        if int(key) - timezone_offset < 0: 
            x = int(int(key) + 24 - timezone_offset)
        else:
            x = int(int(key) - timezone_offset)
        toprint.append({'time':x,'price':avg})
        
    else:
        while str(int(key)+1) not in dataset[counter]['HOUR']:
            counter+=1
#sort based on local time
toprint = sorted(toprint,key=lambda hour: hour['time'])

times = []
prices = []

print('Local Hours that have consistent lower fees:')
for elem in toprint:
    print("[{:02d}:00]:~${:.2f} USD".format(int(elem['time']),elem['price']))
    times.append(str(elem['time']))
    prices.append(elem['price'])

plt.bar(times,prices)
plt.title('Average Hourly Prices Under 5 Day Average')
plt.xlabel('Hours (local timezone)')
plt.ylabel('Average Transaction Fee (USD)')
plt.xticks(ha='right',rotation=45)
plt.show()

x = input('Press X to exit')