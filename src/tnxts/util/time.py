import time
import datetime

def now():
    """返回当前时间，格式: %Y-%m-%d %H:%M:%S"""
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return timestamp