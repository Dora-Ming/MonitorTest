import psutil
import socket
import datetime

# 把字节数转换为GB，保留2位小数
def get_GB(bytes):
    return round(bytes / (1024 * 1024 * 1024), 2)


# 获取CPU信息并写入文件，参数为间隔秒数
def write_cpu(sec, file_log):
    cpu_logical_count = psutil.cpu_count()
    cpu_physical_count = psutil.cpu_count(logical=False)
    cpu_percent = psutil.cpu_percent(interval=sec)
    cpu_time_percent = psutil.cpu_times_percent(interval=sec)

    file_log.write("\n")
    file_log.write("-" * 20 + "CPU 信息" + "-" * 20 + "\n")
    file_log.write("物理CPU个数:" + str(cpu_physical_count) +"\n")
    file_log.write("逻辑CPU个数:" + str(cpu_logical_count) + "\n")
    file_log.write("CPU使用率:" + str(cpu_percent) + "%" + "\n")
    file_log.write("执行用户进程的时间百分比:" + str(cpu_time_percent.user) + "%" + "\n")
    file_log.write("执行内核进程和中断的时间百分比:" + str(cpu_time_percent.system) + "%" + "\n")
    file_log.write("CPU处于空闲状态的时间百分比:" + str(cpu_time_percent.idle) + "%" + "\n")


# 获取内存信息并写入文件
def write_mem(file_log):
    memory = psutil.virtual_memory()
    mem_total = get_GB(memory.total)
    mem_free = get_GB(memory.free)
    mem_used = get_GB(memory.used)

    file_log.write("\n\n")
    file_log.write("-" * 20 + "内存信息" + "-" * 20 + "\n")
    file_log.write("内存总数:" + str(mem_total) + "GB" + "\n")
    file_log.write("内存（使用）:" + str(mem_used) + "GB" + "\n")
    file_log.write("内存（空闲）:" + str(mem_free) + "GB" + "\n")


# 获取磁盘信息并写入文件
def write_disk(file_log):
    file_log.write("\n\n")
    file_log.write("-" * 20 + "磁盘信息" + "-" * 20 + "\n")

    disk_parts = psutil.disk_partitions()
    for disk_part in disk_parts:
        disk_path = disk_part.device

        try:
            disk_usage = psutil.disk_usage(disk_path)
            file_log.write("磁盘路径:" + disk_path + "\n")
            file_log.write("磁盘总大小:" + str(get_GB(disk_usage.total)) + "GB" + "\n")
            file_log.write("磁盘（使用）:" + str(get_GB(disk_usage.used)) + "GB" + "\n")
            file_log.write("磁盘（空闲）:" + str(get_GB(disk_usage.free)) + "GB" + "\n")
            file_log.write("磁盘使用率:" + str(disk_usage.percent) + "%" + "\n")
        except:
            file_log.write("磁盘路径:" + disk_part.device + "\n")
            file_log.write("设备未就绪" + "\n\n")
            continue
        
        file_log.write("\n")

    disk_io = psutil.disk_io_counters()
    disk_read_count = disk_io.read_count
    disk_read_bytes = disk_io.read_bytes
    disk_write_count = disk_io.write_count
    disk_write_bytes = disk_io.write_bytes
    disk_read_time = disk_io.read_time
    disk_write_time = disk_io.write_time

    file_log.write("磁盘读次数:" + str(disk_read_count) + "\n")
    file_log.write("磁盘写次数:" + str(disk_write_count) + "\n")
    file_log.write("磁盘读字节数:" + str(disk_read_bytes) + "\n")
    file_log.write("磁盘写字节数:" + str(disk_write_bytes) + "\n")
    file_log.write("磁盘读时间:" + str(disk_read_time) + "\n")
    file_log.write("磁盘写时间:" + str(disk_write_time) + "\n")


# 获取网络信息并写入文件
def write_net(file_log):
    file_log.write("\n\n")
    file_log.write("-" * 20 + "网络信息" + "-" * 20 + "\n")

    net_io = psutil.net_io_counters()
    net_bytes_recv = net_io.bytes_recv
    net_bytes_sent = net_io.bytes_sent
    net_packets_recv = net_io.packets_recv
    net_packets_sent = net_io.packets_sent

    file_log.write("网络发送字节数:" + str(net_bytes_sent) + "\n")
    file_log.write("网络接收字节数:" + str(net_bytes_recv) + "\n")
    file_log.write("网络发送数据包数:" + str(net_packets_sent) + "\n")
    file_log.write("网络接收数据包数:" + str(net_packets_recv) + "\n")


# 获取系统进程信息并写入文件
def write_proc(file_log):
    file_log.write("\n\n")
    file_log.write("-" * 20 + "系统进程" + "-" * 20 + "\n")

    pids = psutil.pids()

    for pid in pids:
        p = psutil.Process(pid)
        file_log.write("进程名:" + p.name() + "\n")
        file_log.write("进程状态:" + p.status() + "\n")
        file_log.write("进程的cpu时间信息:" + str(p.cpu_times()) + "\n")
        file_log.write("进程的内存利用率:" + str(p.memory_percent()) + "\n")
        file_log.write("进程开启的线程数:" + str(p.num_threads()) + "\n")
        file_log.write("\n")


# 获取其他系统信息并写入文件
def write_oth(file_log):
    file_log.write("\n\n")
    file_log.write("-" * 20 + "其他信息" + "-" * 20 + "\n")

    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    file_log.write("开机时间:" + boot_time + "\n")

    users = psutil.users()
    for user in users:
        user_name = user.name
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        file_log.write("用户名:" + user_name + "\n")
        file_log.write("机器名:" + host_name + "\n")
        file_log.write("IP地址:" + host_ip + "\n")


# 创建文件，记录各个指标的信息
def createfile(filename):
    file_log = open(filename, mode="a")
    return file_log

# 关闭文件
def closefile(file_log):
    file_log.close()


if __name__ == "__main__":
    file_log = createfile("psutil.txt")

    write_cpu(3, file_log)
    write_mem(file_log)
    write_disk(file_log)
    write_net(file_log)
    write_oth(file_log)

    closefile(file_log)