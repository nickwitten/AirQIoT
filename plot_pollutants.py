from matplotlib import pyplot as plt
import numpy as np


with open('pollutants.csv') as f:
    data = f.readlines()
data = [line.replace('\n', '').split(',') for line in data]
station_col = 5
pollutant_cols = [1, 2, 3, 4]
time_col = 7

labels = data[0]
data = np.array(data)[1:]

stations = ['ST102', 'ST105']
data = np.array(data)

fig = plt.figure()
for i, station in enumerate(stations):
    ax = fig.add_subplot(len(stations), 1, i+1)
    station_data = data[data[:,station_col] == station]
    for col in pollutant_cols:
        ax.plot(station_data[::10,time_col], station_data[::10,col], label=labels[col])
    ax.legend()
    plt.title(f'Pollutants Measured by Station {station}')
    plt.xticks([])
    plt.yticks([])
    plt.xlabel('Time')
    plt.ylabel('Concentration')
plt.show()



