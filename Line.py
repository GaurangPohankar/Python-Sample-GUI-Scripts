import matplotlib.pyplot as plt
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
          

x = [1000,  15000, 28000, 70000, 850000]
y = [10000, 20000, 30000, 10000, 50000]

x_plot = range(len(y))

plt.plot(x_plot, y)

plt.xticks(x_plot, x)

plt.show()
