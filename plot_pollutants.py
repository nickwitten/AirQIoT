from matplotlib import pyplot as plt
# plt.ion()
import numpy as np
import boto3
from boto3.dynamodb.conditions import Key, Attr
from env import *
import time


fig = plt.figure(figsize=(10, 8))
stations = ['ST102', 'ST105']
plt.xticks([])
plt.yticks([])
plt.xlabel('Time')
plt.ylabel('Concentration')
while True:
    print("Requesting new data")
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_ACCESS_KEY,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                region_name=AWS_REGION)

    table = dynamodb.Table('AirQualityData')

    now=int(time.time())
    timestampold=now-86400
    results = table.scan(
        FilterExpression=Attr('timestamp').gt(timestampold)
    )
    items = results['Items']

    # with open('pollutants.csv') as f:
    #     data = f.readlines()

    # data = [line.replace('\n', '').split(',') for line in data]
    # labels = data[0]
    # data = np.array(data)[1:]

    labels = list(items[0]['data'].keys())
    data = [list(item['data'].values()) for item in items]

    station_col = 5
    pollutant_cols = [1, 2, 3, 4]
    time_col = 7


    data = np.array(data)

    plt.clf()
    axes = []
    for i in range(len(stations)):
        axes.append(fig.add_subplot(len(stations), 1, i+1))
    for ax, station in zip(axes, stations):
        station_data = data[data[:,station_col] == station]
        for col in pollutant_cols:
            ax.plot(station_data[::10,time_col], station_data[::10,col], label=labels[col])
        ax.legend()
        ax.set_title(f'Pollutants Measured by Station {station}')
    plt.pause(5)



