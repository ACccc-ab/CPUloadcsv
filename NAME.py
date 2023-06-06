import psutil
import pandas as pd
from datetime import datetime
import time
import win32gui
import win32process

def bytes_to_mb(bytes_value):
    # 将字节转换为MB并保留两位小数
    mb_value = round(bytes_value / (1024 * 1024), 2)
    return mb_value

def get_process_name_from_window():
    # 获取当前活动窗口的句柄
    hwnd = win32gui.GetForegroundWindow()

    # 获取窗口的线程ID和进程ID
    tid, pid = win32process.GetWindowThreadProcessId(hwnd)

    # 根据进程ID获取进程对象
    process = psutil.Process(pid)

    # 返回进程的名称
    return process.name()

def monitor_memory_usage(interval_sec, duration_sec):
    # 创建一个空的DataFrame来存储记录
    data = []

    # 获取开始时间
    start_time = datetime.now()

    # 获取结束时间
    end_time = start_time + pd.Timedelta(seconds=duration_sec)

    # 监控内存使用情况并记录到DataFrame
    while datetime.now() < end_time:
        try:
            # 获取当前活动窗口的进程名称
            process_name = get_process_name_from_window()

            # 根据进程名称获取进程对象
            processes = [p for p in psutil.process_iter(attrs=['name']) if p.info['name'] == process_name]
            print(processes)
            #拿到传屏的名字ame='MAXHUBShare.exe'

            # 遍历匹配的进程列表
            for process in processes:
                try:
                    # 获取进程的内存使用情况（以字节为单位）
                    memory_info = process.memory_info()

                    # 获取当前时间戳
                    timestamp = datetime.now()

                    # 将内存使用量转换为MB
                    memory_mb = bytes_to_mb(memory_info.rss)

                    # 添加记录到data列表
                    data.append({'Timestamp': timestamp, 'Memory Usage': memory_mb})

                except psutil.NoSuchProcess:
                    # 如果进程不存在，则结束循环
                    break

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # 如果无法获取进程名称或进程访问被拒绝，则跳过此次循环
            pass

        # 等待指定的时间间隔
        time.sleep(interval_sec)

    # 创建DataFrame
    df = pd.DataFrame(data)

    # 将DataFrame保存为CSV文件
    df.to_csv('memory_usage.csv', index=False)

# 监控的时间间隔（秒）
interval = 5

# 监控的持续时间（秒）
duration = 30

monitor_memory_usage(interval, duration)
