import psutil
import socket
import datetime

# 把字节数转换为GB，保留2位小数
def get_GB(bytes):
    return round(bytes / (1024 * 1024 * 1024), 2)


# 获取并打印CPU信息，参数为间隔秒数
def print_CPU(sec):
    cpu_logical_count = psutil.cpu_count()
    cpu_physical_count = psutil.cpu_count(logical=False)
    cpu_percent = psutil.cpu_percent(interval=sec)
    cpu_time_percent = psutil.cpu_times_percent(interval=sec)

    print("\n")
    print('-'*20 + "CPU 信息" + '-'*20)
    print("物理CPU个数:" + str(cpu_physical_count))
    print("逻辑CPU个数:" + str(cpu_logical_count))
    print("CPU使用率:" + str(cpu_percent) + "%")
    print("执行用户进程的时间百分比:" + str(cpu_time_percent.user) + "%")
    print("执行内核进程和中断的时间百分比:" + str(cpu_time_percent.system) + "%")
    print("CPU处于空闲状态的时间百分比:" + str(cpu_time_percent.idle) + "%")


# 获取并打印内存信息
def print_mem():
    memory = psutil.virtual_memory()
    mem_total = get_GB(memory.total)
    mem_free = get_GB(memory.free)
    mem_used = get_GB(memory.used)

    print("\n")
    print('-'*20 + "内存信息" + '-'*20)
    print("内存总数:" + str(mem_total) + "GB")
    print("内存（使用）:" + str(mem_used) + "GB")
    print("内存（空闲）:" + str(mem_free) + "GB")


# 获取并打印磁盘信息
def print_disk():
    print("\n")
    print('-'*20 + "磁盘信息" + '-'*20)

    disk_parts = psutil.disk_partitions()
    for disk_part in disk_parts:
        disk_path = disk_part.device

        try:
            disk_usage = psutil.disk_usage(disk_path)
            print("磁盘路径:" + disk_path)
            print("磁盘总大小:" + str(get_GB(disk_usage.total)) + "GB")
            print("磁盘（使用）:" + str(get_GB(disk_usage.used)) + "GB")
            print("磁盘（空闲）:" + str(get_GB(disk_usage.free)) + "GB")
            print("磁盘使用率:" + str(disk_usage.percent) + "%")
        except:
            print("磁盘路径:" + disk_part.device)
            print("设备未就绪")
            continue

        print("")

    disk_io = psutil.disk_io_counters()
    disk_read_count = disk_io.read_count
    disk_read_bytes = disk_io.read_bytes
    disk_write_count = disk_io.write_count
    disk_write_bytes = disk_io.write_bytes
    disk_read_time = disk_io.read_time
    disk_write_time = disk_io.write_time

    print("")
    print("磁盘读次数:" + str(disk_read_count))
    print("磁盘写次数:" + str(disk_write_count))
    print("磁盘读字节数:" + str(disk_read_bytes))
    print("磁盘写字节数:" + str(disk_write_bytes))
    print("磁盘读时间:" + str(disk_read_time))
    print("磁盘写时间:" + str(disk_write_time))


# 获取并打印网络信息
def print_net():
    print("\n")
    print('-'*20 + "网络信息" + '-'*20)

    net_io = psutil.net_io_counters()
    net_bytes_recv = net_io.bytes_recv
    net_bytes_sent = net_io.bytes_sent
    net_packets_recv = net_io.packets_recv
    net_packets_sent = net_io.packets_sent
    print("网络发送字节数:" + str(net_bytes_sent))
    print("网络接收字节数:" + str(net_bytes_recv))
    print("网络发送数据包数:" + str(net_packets_sent))
    print("网络接收数据包数:" + str(net_packets_recv))


# 获取系统进程信息
def print_proc():
    print("\n")
    print('-'*20 + '系统进程' + '-'*20)

    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        print('进程名:' + p.name())
        print('进程状态:' + p.status())
        print('进程的cpu时间信息:' + str(p.cpu_times()))
        print('进程的内存利用率:' + str(p.memory_percent()))
        print('进程开启的线程数:' + str(p.num_threads()))
        print('')


# 获取并打印其他系统信息
def print_oth():
    print('\n')
    print('-'*20 + "其他信息" + '-'*20)
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    print("开机时间:" + boot_time)

    users = psutil.users()
    for user in users:
        user_name = user.name
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print("用户名:" + user_name)
        print("机器名:" + host_name)
        print("IP地址:" + host_ip)


if __name__ == '__main__':
    print_CPU(3)
    print_mem()
    print_disk()
    print_net()
    print_oth()