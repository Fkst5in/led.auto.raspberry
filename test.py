#!/usr/bin/python3
# _*_ coding: utf-8 _*_

import pigpio
import time

MONITOR_PIN = 4
pi = pigpio.pi()

try:
    print('按下 Ctrl-C 可停止程式')
    # while True:
    pi.set_mode(MONITOR_PIN, pigpio.OUTPUT)
    pi.write(MONITOR_PIN,0)
    time.sleep(0.1)
    
    start_time = time.time()
    pi.set_mode(MONITOR_PIN, pigpio.INPUT)
    while(pi.read(MONITOR_PIN) == 0):
        pass
    end_time = time.time()
    print('count={}, time={:.05f}'.format(1, time.time()-start_time))
except KeyboardInterrupt:
    print('關閉程式')
finally:
    pass