import pandas as pd
from collections import Counter as c

from matplotlib import pyplot as plt
import x
a = pd.DataFrame(x.hourly_avgs)
b = []
for index,row in a.iterrows():
    if row['AVERAGE_FEE'] < x.fee_avg:
        b.append({
            'HOUR': str(a['HOUR'][index]),
            'AVG': a['AVERAGE_FEE'][index]
        })
b = pd.DataFrame(b)
plt.bar(b['HOUR'],b['AVG'])
plt.title('Average Hourly Prices Under 5 Day Average')
plt.xlabel('Hours (local timezone)')
plt.ylabel('Average Transaction Fee (USD)')
plt.show()