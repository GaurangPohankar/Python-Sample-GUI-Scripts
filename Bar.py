import matplotlib.pyplot as plt
import numpy as np


import csv
csv_file=open("raw.csv", "r")
reader = csv.reader(csv_file)

positive = 0
neutral = 0
negative = 0

for row in reader:
     if(str(row[2]) == 'positive'):
          positive += 1
     if(str(row[2]) == 'neutral'):
          neutral += 1
     if(str(row[2]) == 'negative'):
          negative += 1
          
city=['positive','negative','neutral']
pos = np.arange(len(city))
Happiness_Index=[int(positive),int(negative),int(neutral)]
 
plt.bar(pos,Happiness_Index,color='blue',edgecolor='black')
plt.xticks(pos, city)
plt.xlabel('City', fontsize=16)
plt.ylabel('Happiness_Index', fontsize=16)
plt.title('Barchart - Happiness index across cities',fontsize=20)
plt.show()
