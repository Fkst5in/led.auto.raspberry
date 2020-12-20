#!/usr/bin/python3
# _*_ coding: utf-8 _*_

import pigpio
import time

PWM_LED_PIN = 18
PWM_FREQ = 800
MONITOR_PIN = 4

pi = pigpio.pi()
start_time = time.time()

#获取可调节的亮度范围
def get_interval(pi):
    #led最亮
    pi.hardware_PWM(PWM_LED_PIN,PWM_FREQ,100 *10000)
    time.sleep(0.1)
    #测量亮度
    print('最大亮度{:.05f}'.format(measure(pi)))
    #led最暗
    pi.hardware_PWM(PWM_LED_PIN,PWM_FREQ,0 *10000)
    time.sleep(0.1)
    #测量亮度
    print('最小亮度{:.05f}'.format(measure(pi)))

def measure(pi):
    """
    to measure the brightness of environment
    """
    pi.set_mode(MONITOR_PIN, pigpio.OUTPUT)
    pi.write(MONITOR_PIN,0)
    start_time = time.time()
    time.sleep(0.05)
    pi.set_mode(MONITOR_PIN, pigpio.INPUT)
    while(pi.read(MONITOR_PIN) == 0):
        pass
    return time.time() - start_time

try:
    get_interval(pi)


except KeyboardInterrupt:
    print('關閉程式')
finally:
    pi.set_mode(PWM_LED_PIN,pigpio.INPUT)