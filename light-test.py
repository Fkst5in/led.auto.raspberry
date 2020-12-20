#!/usr/bin/python3
# _*_ coding: utf-8 _*_

import RPi.GPIO as GPIO
import time

MONITOR_PIN = 4

GPIO.setmode(GPIO.BCM)

try:
    print('按下 Ctrl-C 可停止程式')
    while True:
        GPIO.setup(MONITOR_PIN, GPIO.OUT)
        GPIO.output(MONITOR_PIN, GPIO.LOW)
        time.sleep(0.1)

        count = 0
        start_time = time.time()
        GPIO.setup(MONITOR_PIN, GPIO.IN)
        while (GPIO.input(MONITOR_PIN) == GPIO.LOW):
            pass
            # count += 1
        end_time = time.time()

        print('count={}, time={:.05f}'.format(1, end_time-start_time))
except KeyboardInterrupt:
    print('關閉程式')
finally:
    GPIO.cleanup()