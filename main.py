import psutil
import pandas as pd
from datetime import datetime
import time

def bytes_to_mb(bytes_value):
    # 将字节转换为MB并保留两位小数
    mb_value = round(bytes_value / (1024 * 1024), 2)
    return mb_value

def monitor_memory_usage(pid, interval_sec, duration_sec):
    # 创建一个空的DataFrame来存储记录
    data = []

    # 获取开始时间
    start_time = datetime.now()

    # 获取结束时间
    end_time = start_time + pd.Timedelta(seconds=duration_sec)

    # 监控内存使用情况并记录到DataFrame
    while datetime.now() < end_time:
        try:
            # 根据PID获取进程对象
            process = psutil.Process(pid)

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

        # 等待指定的时间间隔
        time.sleep(interval_sec)

    # 创建DataFrame
    df = pd.DataFrame(data)

    # 将DataFrame保存为CSV文件
    df.to_csv('memory_usage.csv', index=False)

# 要监控的应用程序PID
app_pid = 26104

# 监控的时间间隔（秒）
interval = 1

# 监控的持续时间（秒）
duration = 30

monitor_memory_usage(app_pid, interval, duration)
