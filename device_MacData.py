import datetime
import os
import subprocess
import time
import pandas as pd
from wsgiref.validate import validator
from subprocess import Popen, PIPE
#from OperateFile import OperatePickle
import re
#from OperateFile import OperatePickle
from consoleLog import Logger
from datetime import datetime, date, time
import logging
from openpyxl import load_workbook
from openpyxl.chart import LineChart, Reference
from openpyxl import Workbook
import shlex
import ctypes
desktop_path = os.path.join(os.path.expanduser("~/Desktop"), "console_log.log")
print(desktop_path)
log_path = desktop_path
logger =Logger(logging.DEBUG, log_path)
import queue
def now_time():
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    nowTime="{}:{}:{}".format(hour, minute, second)
    return nowTime

def get_cpu(devices,package_string):
    try:
        output = subprocess.check_output(['adb', '-s',devices, 'shell', 'top', '-n', '1'],
                                         universal_newlines=True)
        output_str = output.strip()
        lines = output_str.split('\n')
        package_string1 = package_string.split('.')
        pattern = re.compile(f".*{package_string1[1]}.+")
        match = pattern.search(output_str)
        cpu_title_pattern = re.compile(r'.*CPU.*[%\]]?')
        for line in lines:
            if "PID" in line:  # 判断这一行是否是列标题行
                columns = line.strip().split()  # 提取出所有列标题
                print(columns)
                # 找到第一个符合条件的 CPU 列标题，记录其索引位置
                for index, column in enumerate(columns):
                    print("for2")
                    if cpu_title_pattern.match(column):
                        cpu_title_index = index
                        print(cpu_title_index)
                        # 使用正则表达式匹配包含指定包名的行
                        if match:
                            # 如果找到匹配的行，按空格分割字符串，获取 CPU 使用率和内存情况
                            cpu_info = match.group().split()[cpu_title_index]
                            logger.info(f"CPU 占用：{cpu_info}")
                            # queue.put(cpu_info)
                            # 输出 CPU 占用情况
                            return cpu_info
                        else:
                            # print(f"Application {package_string} not found")
                            return False
        # output_str.split("\n")
        # # print(output_str)
        #
        # # 使用正则表达式匹配包含指定包名的行
        # pattern = re.compile(f".*dianshijia.*")
        # match = pattern.search(output_str)
        #
        # if match:
        #     # 如果找到匹配的行，按空格分割字符串，获取 CPU 使用率和内存情况
        #     cpu_info = match.group().split()[8]
        #     # queue.put(cpu_info)
        #     # 输出 CPU 占用情况
        #     print(cpu_info)
        #     return cpu_info
        # else:
        #     # print(f"Application {package_string} not found")
        #     return False
    except subprocess.CalledProcessError as e:
        # print("Error:", e)
        return False


def get_men(pkg_name, devices):
    try:
        cmd = ["adb", "-s", devices, "shell", "dumpsys", "meminfo", pkg_name]
        logger.info(cmd)
        output = subprocess.check_output(cmd).split()
        print(output)
        s_men = ".".join([x.decode() for x in output])  # 转换为string
        logger.info(s_men)
        men2 = int(re.findall(r"TOTAL.(\d+)*", s_men, re.S)[0])
        print(men2)
        return men2
    except subprocess.CalledProcessError as e:
        logger.error("获取应用 %s 的内存占用信息失败：%s" % (pkg_name, e))
        men2 = 0
        return men2


def get_cpu_info(package_name):
    # 获取应用程序的CPU信息，输出格式为：User Time   System Time
    cmd = f"adb shell dumpsys cpuinfo | findstr '{package_name}'"
    logger.info(cmd)
    output = subprocess.check_output(cmd, shell=True).decode().strip()#使用strip()方法去除字符串两端的空格和换行符
    user_time = output.split()[2][:-1]
    sys_time = output.split()[4][:-1]
    return user_time, sys_time

def get_fps(pkg_name, devices):
    _adb = "adb -s " + devices + " shell dumpsys gfxinfo %s" % pkg_name
    logger.info(_adb)
    # results = os.popen(_adb).read().strip()
    results, b = Popen(_adb, stdout=PIPE, stderr=PIPE).communicate()
    frames = [x for x in results.decode("utf-8").split('\n') if validator(x)]
    frame_count = len(frames)
    jank_count = 0
    vsync_overtime = 0
    render_time = 0
    for frame in frames:
        time_block = re.split(r'\s+', frame.strip())
        if len(time_block) == 3:
            try:
                render_time = float(time_block[0]) + float(time_block[1]) + float(time_block[2])
            except Exception as e:
                render_time = 0


#获取pid
def get_pid(pkg_name, devices):
    cmd = "adb -s " + devices + " shell ps | findstr " + pkg_name
    logger.info("----get_pid-------")
    logger.info(cmd)
    pid = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE).stdout.readlines()
    for item in pid:
        if item.split()[8].decode() == pkg_name:
            return item.split()[1].decode()

def get_flow(pid, type, devices):
    # pid = get_pid(pkg_name)
    upflow = downflow = 0
    if pid is not None:
        cmd = "adb -s " + devices + " shell cat /proc/" + pid + "/net/dev"
        logger.info(cmd)
        _flow = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE).stdout.readlines()
        for item in _flow:
            if type == "wifi" and item.split()[0].decode() == "wlan0:":  # wifi
                # 0 上传流量，1 下载流量
                upflow = int(item.split()[1].decode())
                downflow = int(item.split()[9].decode())
                logger.info("------flow---------")
                logger.info(upflow)
                break
            if type == "gprs" and item.split()[0].decode() == "rmnet0:":  # gprs
                logger.info("-----flow---------")
                upflow = int(item.split()[1].decode())
                downflow = int(item.split()[9].decode())
                logger.info(upflow)
                break

    OperatePickle().writeFlowInfo(upflow, downflow, PATH("./info/" + devices + "_flow.pickle"))


 #手机分辨率
def get_app_pix(devices):
    cmd = "adb -s " + devices + " shell wm size"
    logger.info(cmd)
    return subprocess.check_output(cmd).split()[2].decode()

if __name__ == '__main__':
    get_cpu("XPL4C19C11001295","dianshi")
    #get_men("com.dianshijia.tvlive","XPL4C19C11001295")