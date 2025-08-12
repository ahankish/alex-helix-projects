#!/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 
import sys

# CLI: .csv file to be graphed 
filename = sys.argv[1]

# Open the file and turn into a dataframe 
df = pd.read_csv(filename)

time = df["Time"].to_numpy() # In Minutes
mother_temp = df["Motherboard"].to_numpy() # In Celsius
cpu_temp = df["Motherboard CPU"].to_numpy() # In Celsius
fan_speed = df["Fan"].to_numpy() # In RPM (???)

fig, (axfan, axmother, axcpu) = plt.subplots(3, sharex=True)
fig.suptitle('Sensors Run Analysis')
plt.tight_layout()

axfan.plot(time, fan_speed)
#axfan.set_title('Fan Speed vs. Time')
axfan.set(xlabel='Time (Minutes)', ylabel='Fan Speed (RPM)')

axmother.plot(time, mother_temp, color='r')
#axmother.set_title('Motherboard Temp. vs. Time')
axmother.set(xlabel='Time (Minutes)', ylabel='Motherboard Temp. (C)')

axcpu.plot(time, cpu_temp, color='g')
#axcpu.set_title('CPU Temp. vs. Time')
axcpu.set(xlabel='Time (Minutes)', ylabel='CPU Temp (C)')

axfan.label_outer()
axmother.label_outer()
axcpu.label_outer()

#plt.subplots_adjust(
plt.savefig("test-graph.png", bbox_inches='tight')
plt.show()
