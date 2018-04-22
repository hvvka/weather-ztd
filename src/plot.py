import csv

import matplotlib.pyplot as plt

x = []
y = []

with open('src/output/output.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(str(row[0]))
        y.append(float(row[1]))

plt.plot(x, y, label='BART')
plt.xlabel('time')
plt.ylabel('ZTD')
plt.title('ZTD Average')
plt.legend()
plt.show()
