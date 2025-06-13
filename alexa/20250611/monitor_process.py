import os
import psutil
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
import sys
import platform
from datetime import datetime
import seaborn as sns

sns.set(style="whitegrid")

plt.rcParams.update({
    "font.size": 12,
    "axes.labelsize": 14,
    "axes.titlesize": 16,
    "legend.fontsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
})

def get_top_processes(prev_io, n=5):
    cpu_list, mem_list, io_list = [], [], []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'io_counters']):
        try:
            pid = proc.info['pid']
            name = proc.info['name'] or "unknown"
            cpu = proc.info['cpu_percent']
            mem = proc.info['memory_info'].rss / (1024**3) if proc.info['memory_info'] else 0.0
            io = proc.info['io_counters']
            read_mb = write_mb = 0.0
            if io:
                prev = prev_io.get(pid, (0, 0))
                read_mb = (io.read_bytes - prev[0]) / (1024**2)
                write_mb = (io.write_bytes - prev[1]) / (1024**2)
                prev_io[pid] = (io.read_bytes, io.write_bytes)

            cpu_list.append((pid, name, cpu, mem, read_mb, write_mb))
            mem_list.append((pid, name, cpu, mem, read_mb, write_mb))
            io_list.append((pid, name, cpu, mem, read_mb, write_mb))

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    top_cpu = sorted(cpu_list, key=lambda x: x[2], reverse=True)[:n]
    top_mem = sorted(mem_list, key=lambda x: x[3], reverse=True)[:n]
    top_io = sorted(io_list, key=lambda x: x[4] + x[5], reverse=True)[:n]

    return top_cpu, top_mem, top_io


def get_all_related_processes(name):
    matches = []
    for proc in psutil.process_iter(['name', 'pid']):
        try:
            if proc.info['name'] and name in proc.info['name']:
                matches.append(proc)
                matches.extend(proc.children(recursive=True))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return matches

def log_specific_program(name, logfile):
    processes = get_all_related_processes(name)
    now = int(datetime.now().timestamp())
    with open(logfile, 'a', newline='') as f:
        writer = csv.writer(f)
        for proc in processes:
            try:
                cpu = proc.cpu_percent(interval=0.1)
                mem = proc.memory_info().rss / (1024**3)
                io = proc.io_counters()
                read_mb = io.read_bytes / (1024**2)
                write_mb = io.write_bytes / (1024**2)
                writer.writerow([now, proc.name(), proc.pid, cpu, mem, read_mb, write_mb])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

def log_process_details(cpu_log, mem_log, dio_log, top_cpu, top_mem, top_dio):
    now_str = int(datetime.now().timestamp())
    for logfile, procs in [
        (cpu_log, top_cpu),
        (mem_log, top_mem),
        (dio_log, top_dio)
    ]:
        with open(logfile, 'a', newline='') as f:
            writer = csv.writer(f)
            for proc in procs:
                writer.writerow([now_str] + list(proc))

def real_time_monitor():
    target_programs = ["cmake", "make"]

    log_dir = "dat"
    if not os.path.isdir(log_dir):
        print(f"ERROR: Directory '{log_dir}' does not exist. Please create it before running this script.")
        sys.exit(1)

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_log = os.path.join(log_dir, f"resource_log_{timestamp_str}_full.csv")
    cpu_log  = os.path.join(log_dir, f"resource_log_{timestamp_str}_cpu.csv")
    mem_log  = os.path.join(log_dir, f"resource_log_{timestamp_str}_mem.csv")
    dio_log  = os.path.join(log_dir, f"resource_log_{timestamp_str}_dio.csv")

    program_logs = {
        name: os.path.join(log_dir, f"resource_log_{timestamp_str}_{name}.csv")
        for name in target_programs
    }

    with open(full_log, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "CPU_Total", "Memory_Used_GB", "Disk_Read_MB", "Disk_Write_MB", "Net_Sent_MB", "Net_Recv_MB"])

    header = ["Time", "PID", "Name", "CPU_Total", "Memory_Used_GB", "Disk_Read_MB", "Disk_Write_MB"]
    for log_file in [cpu_log, mem_log, dio_log]:
        with open(log_file, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)

    for file in program_logs.values():
        with open(file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Time", "Name", "PID", "CPU_Total", "Memory_Used_GB", "Disk_Read_MB", "Disk_Write_MB"])

    history_length = 3600  # 1 hour of 1-second samples
    cpu_total, mem_used = [], []
    disk_read, disk_write = [], []
    net_sent, net_recv = [], []

    prev_disk = [psutil.disk_io_counters()]
    prev_net = [psutil.net_io_counters()]
    prev_io = {}  # For per-process disk io tracking

    fig, ax = plt.subplots(4, 1, figsize=(10, 10))
    plt.tight_layout()

    def animate(i):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().used / (1024 ** 3)  # GB

        current_disk = psutil.disk_io_counters()
        current_net = psutil.net_io_counters()

        disk_read_mb = (current_disk.read_bytes - prev_disk[0].read_bytes) / 1024**2
        disk_write_mb = (current_disk.write_bytes - prev_disk[0].write_bytes) / 1024**2
        net_sent_mb = (current_net.bytes_sent - prev_net[0].bytes_sent) / 1024**2
        net_recv_mb = (current_net.bytes_recv - prev_net[0].bytes_recv) / 1024**2

        prev_disk[0] = current_disk
        prev_net[0] = current_net

        cpu_total.append(cpu)
        mem_used.append(mem)
        disk_read.append(disk_read_mb)
        disk_write.append(disk_write_mb)
        net_sent.append(net_sent_mb)
        net_recv.append(net_recv_mb)

        for lst in [cpu_total, mem_used, disk_read, disk_write, net_sent, net_recv]:
            if len(lst) > history_length:
                lst.pop(0)

        top_cpu, top_mem, top_dio = get_top_processes(prev_io)
        now_str = int(datetime.now().timestamp())

        # Write full system stats
        with open(full_log, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([now_str, cpu, mem, disk_read_mb, disk_write_mb, net_sent_mb, net_recv_mb])

        # Write per-process stats
        log_process_details(cpu_log, mem_log, dio_log, top_cpu, top_mem, top_dio)

        # Write specific programs 
        for name, logfile in program_logs.items():
            log_specific_program(name, logfile)

        # Plot CPU
        ax[0].clear()
        ax[0].plot(cpu_total, label="CPU (%)", color='blue')
        ax[0].legend(loc="upper left")
        ax[0].set_ylabel("CPU %")
        ax[0].set_ylim(0, 100)

        # Plot Memory
        ax[1].clear()
        ax[1].plot(mem_used, label="Memory Used (GB)", color='orange')
        ax[1].legend(loc="upper left")
        ax[1].set_ylabel("Memory (GB)")

        # Plot Disk IO (system-wide)
        ax[2].clear()
        ax[2].plot(disk_read, label="Disk Read (MB/s)", color='green')
        ax[2].plot(disk_write, label="Disk Write (MB/s)", color='red')
        ax[2].legend(loc="upper left")
        ax[2].set_ylabel("Disk I/O (MB/s)")

        # Plot Network IO (system-wide)
        ax[3].clear()
        ax[3].plot(net_sent, label="Net Sent (MB/s)", color='purple')
        ax[3].plot(net_recv, label="Net Recv (MB/s)", color='brown')
        ax[3].legend(loc="upper left")
        ax[3].set_ylabel("Network I/O (MB/s)")

    ani = animation.FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)
    plt.show()

def main():
    print("Starting real-time resource monitoring...")
    real_time_monitor()

if __name__ == "__main__":
    main()

