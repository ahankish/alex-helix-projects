import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import psutil

filename = sys.argv[1]
fullname = "stresstests/" + filename


# data using psutil
load_avg = psutil.getloadavg() # average system load of processes in a runnable state
mem_usage = psutil.virtual_memory()
disk_partitions = psutil.disk_partitions()
sens_temp = psutil.sensors_temperatures()
sens_fans = psutil.sensors_fans()
# cputimes = psutils.cpu_times()
# cpustats = psutils.cpu_stats()

#df_headers = pd.read_csv(fullname, )
#print(df.to_string())

#with open(fullname) as test_file:
    #for entry in test_file: 
        # remember the first entry contains headers

df_time = pd.read_csv(fullname, usecols=["Time"])

df_tempedge = pd.read_csv(fullname, usecols=["Temp:Edge,0"])
#df_temptctl = pd.read_csv(fullname, usecols=["Temp:Tctl,0"])

df_core0 = pd.read_csv(fullname, usecols=["Frequency:Core 0"])
df_core1 = pd.read_csv(fullname, usecols=["Frequency:Core 1"])
df_core2 = pd.read_csv(fullname, usecols=["Frequency:Core 2"])
df_core3 = pd.read_csv(fullname, usecols=["Frequency:Core 3"])
df_core4 = pd.read_csv(fullname, usecols=["Frequency:Core 4"])
df_core5 = pd.read_csv(fullname, usecols=["Frequency:Core 5"])
df_core6 = pd.read_csv(fullname, usecols=["Frequency:Core 6"])
df_core7 = pd.read_csv(fullname, usecols=["Frequency:Core 7"])
df_core8 = pd.read_csv(fullname, usecols=["Frequency:Core 8"])
df_core9 = pd.read_csv(fullname, usecols=["Frequency:Core 9"])
df_core10 = pd.read_csv(fullname, usecols=["Frequency:Core 10"])
df_core11 = pd.read_csv(fullname, usecols=["Frequency:Core 11"])

# graphing the core frequencies vs time

#size = time_arr.size
time = np.zeros(df_time.to_numpy().size)
core0 = np.zeros(df_core0.to_numpy().size)
core1 = np.zeros(df_core1.to_numpy().size)
core2 = np.zeros(df_core2.to_numpy().size)
core3 = np.zeros(df_core3.to_numpy().size)
core4 = np.zeros(df_core4.to_numpy().size)
core5 = np.zeros(df_core5.to_numpy().size)
core6 = np.zeros(df_core6.to_numpy().size)
core7 = np.zeros(df_core7.to_numpy().size)
core8 = np.zeros(df_core8.to_numpy().size)
core9 = np.zeros(df_core9.to_numpy().size)
core10 = np.zeros(df_core10.to_numpy().size)
core11 = np.zeros(df_core11.to_numpy().size)

for i, entry in enumerate(df_time.to_numpy()):
    if i < 4:
        time[i] = float(entry[0][-1])
    elif i > 26: 
        time[i] = time[i-1] + 2

    else:
        time[i] = float(entry[0][-2] + entry[0][-1]) # add strings together

for i, entry in enumerate(df_core0.to_numpy()):
    core0[i] = float(entry[0])

for i, entry in enumerate(df_core1.to_numpy()):
    core1[i] = float(entry[0])

for i, entry in enumerate(df_core2.to_numpy()):
    core2[i] = float(entry[0])

for i, entry in enumerate(df_core3.to_numpy()):
    core3[i] = float(entry[0])

for i, entry in enumerate(df_core4.to_numpy()):
    core4[i] = float(entry[0])

for i, entry in enumerate(df_core5.to_numpy()):
    core5[i] = float(entry[0])

for i, entry in enumerate(df_core6.to_numpy()):
    core6[i] = float(entry[0])

for i, entry in enumerate(df_core7.to_numpy()):
    core7[i] = float(entry[0])

for i, entry in enumerate(df_core8.to_numpy()):
    core8[i] = float(entry[0])

for i, entry in enumerate(df_core9.to_numpy()):
    core9[i] = float(entry[0])

for i, entry in enumerate(df_core10.to_numpy()):
    core10[i] = float(entry[0])

for i, entry in enumerate(df_core11.to_numpy()):
    core11[i] = float(entry[0])


#plt.subplots(nrows=2, ncols=1)
plt.plot(time, core0, 'r', label="core 0") # 'r' for red plot
plt.plot(time, core1, 'orange', label="core 1")
plt.plot(time, core2, 'y', label="core 2")
plt.plot(time, core3, 'g', label="core 3")
plt.plot(time, core4, 'b', label="core 4")
plt.plot(time, core5, 'indigo', label="core 5")
plt.plot(time, core6, 'violet', label="core 6")
plt.plot(time, core7, 'deeppink', label="core 7")
plt.plot(time, core8, 'crimson', label="core 8")
plt.plot(time, core9, 'tomato', label="core 9")
plt.plot(time, core10, 'sienna', label="core 10")
plt.plot(time, core11, 'goldenrod', label="core 11")
plt.title("Core Frequency vs. Time")
plt.legend(loc="upper left")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
#plt.show()
plt.savefig(sys.argv[2]) # saving the plot to a png - name given as 2nd argument

# graphing the time vs temperature

tempedge = np.zeros(df_tempedge.to_numpy().size)

for i, entry in enumerate(df_tempedge.to_numpy()):
    tempedge[i] = float(entry[0])

#plt.subplot(1, 2, 2)
plt.plot(time, tempedge, 'indigo')
plt.title("Edge Tempertature vs. Time")
plt.xlabel("Time (s)")
plt.ylabel("Temperature (Fahrenheight??)")

#plt.show()
plt.savefig(sys.argv[3]) # saves the plot to a png - name given as 3rd argument

