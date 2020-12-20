#!/usr/bin/python3
# _*_ coding: utf-8 _*_

import pigpio
import time

MONITOR_PIN = 4

pi = pigpio.pi()
start_time = time.time()

def init():
    """
    初始化led
    freq: pwm的频率
    """
    global pi
    pi = pigpio.pi()


def measure():
    """
    to measure the brightness of environment
    """
    pi.set_mode(MONITOR_PIN, pigpio.OUTPUT)
    pi.write(MONITOR_PIN,0)
    time.sleep(0.05)
    start_time = time.time()
    pi.set_mode(MONITOR_PIN, pigpio.INPUT)
    while(pi.read(MONITOR_PIN) == 0):
        pass
    return time.time() - start_time

def cleanup():
    """
    to clear
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