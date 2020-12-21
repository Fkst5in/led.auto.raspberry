#!/usr/bin/python3
# _*_ coding: utf-8 _*_

import pigpio
import time


MONITOR_PIN = 4
pi = pigpio.pi()

def init():
    """
    连接pigpio
    """
    global pi
    # 判断是否已连接
    if not pi.connected:
        pi = pigpio.pi()

def measure():
    """
    测量亮度
    返回测量电路震荡单次震荡时长
    """
    pi.set_mode(MONITOR_PIN, pigpio.OUTPUT)
    pi.write(MONITOR_PIN,0)
    time.sleep(0.05)
    start_time = time.time()
    pi.set_mode(MONITOR_PIN, pigpio.INPUT)
    while(pi.read(MONITOR_PIN) == 0):
        pass
    return (time.time() - start_time) * 500
def cleanup():
    """
    断开连接
    """
    pi.stop()

if __name__ == '__main__':
    try:
        while True:
            time.sleep(0.5)
            print('当前亮度{:.05f}'.format(measure()))
    except KeyboardInterrupt:
        print('關閉程式')
    finally:
        cleanup()