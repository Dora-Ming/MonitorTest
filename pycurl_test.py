# -*- coding: utf-8 -*-
import pycurl
import certifi
import time

# web地址监控类
class UrlMonitor(object):
    curl = pycurl.Curl()    # pucurl对象
    content_file = None     # 存放html响应头和内容的文件
    url = ""                # 要监控的Url地址
    interval = 0            # 监控间隔，单位秒
    timeout = 0             # 请求超时时间，单位秒
    status_code = ""        # 返回的HTTP状态码
    dns_time = 0            # DNS解析时间，单位毫秒
    connect_time = 0        # 建立连接时间，单位毫秒
    pre_transfer_time = 0   # 从建立连接到准备传输所消耗的时间，单位毫秒
    start_transfer_time = 0 # 从建立连接到传输开始消耗的时间，单位毫秒
    total_time = 0          # 传输总时间，单位毫秒
    header_size = 0         # HTTP头大小
    size_download = 0       # 下载的数据包大小，单位字节
    speed_download = 0      # 平均下载速度

    # 初始化UrlMonitor对象，默认连接间隔为10秒，超时时间为5秒
    def __init__(self, url, interval = 10, timeout = 5):
        self.url = url
        self.content_file = open("content.txt", "wb")
        self.interval = interval
        self.timeout = timeout
        self.setopt()
        
    # 设置pycurl对象的url和timeout值
    def setopt(self):
        self.curl.setopt(pycurl.URL, self.url)
        self.curl.setopt(pycurl.TIMEOUT, self.timeout)
        self.curl.setopt(pycurl.CAINFO, certifi.where())
        self.curl.setopt(pycurl.NOPROGRESS, 1)   # 屏蔽下载进度条
        self.curl.setopt(pycurl.FORBID_REUSE, 1)  # 完成交互后强制断开连接，不重用
        self.curl.setopt(pycurl.WRITEHEADER, self.content_file)   # 将html头写入文件
        self.curl.setopt(pycurl.WRITEDATA, self.content_file)    # 将html体写入文件
    
    # 执行perform方法，获取请求返回的状态码和其他信息
    def perfrom(self):
        try:
            self.curl.perform()

            self.status_code = self.curl.getinfo(self.curl.HTTP_CODE)
            self.dns_time = self.curl.getinfo(self.curl.NAMELOOKUP_TIME)
            self.connect_time = self.curl.getinfo(self.curl.CONNECT_TIME)
            self.pre_transfer_time = self.curl.getinfo(self.curl.PRETRANSFER_TIME)
            self.start_transfer_time = self.curl.getinfo(self.curl.STARTTRANSFER_TIME)
            self.total_time = self.curl.getinfo(self.curl.TOTAL_TIME)
            self.header_size = self.curl.getinfo(self.curl.HEADER_SIZE)
            self.size_download = self.curl.getinfo(self.curl.SIZE_DOWNLOAD)
            self.speed_download = self.curl.getinfo(self.curl.SPEED_DOWNLOAD)

            print("监控URL: %s" % self.url)
            print("HTTP状态码: %s" % self.status_code)
            print("DNS解析时间: %.2f ms" % (self.dns_time * 1000))
            print("建立连接时间: %.2f ms" % (self.connect_time * 1000))
            print("准备传输时间: %.2f ms" % (self.pre_transfer_time * 1000))
            print("传输开始时间: %.2f ms" % (self.start_transfer_time * 1000))
            print("传输总时间: %.2f ms" % (self.total_time * 1000))
            print("HTTP头部大小: %d bytes" % (self.header_size))
            print("下载数据包大小: %d bytes" % (self.size_download))
            print("平均下载速度: %d bytes/s" % (self.speed_download))
            print("")

        except Exception as e:
            print("连接错误:" + str(e))

    # 关闭文件对象和pycurl对象，释放内存及回收
    def close(self):
        self.content_file.close()
        self.curl.close()

if __name__ == "__main__":
    url = "https://www.jd.com"
    m = UrlMonitor(url)

    for i in range(3):
        m.perfrom()
        time.sleep(m.interval)
    
    m.close()


    



