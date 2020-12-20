#!/usr/bin/python3
# _*_ coding: utf-8 _*_

import pigpio

PWM_LED_PIN = 18
PWM_FREQ = 800

pi = pigpio.pi()

def init(freq):
    """
    初始化led
    freq: pwm的频率
    """
    global pi
    pi = pigpio.pi()
    PWM_FREQ = freq

def change(duty):
    """
    改变led的亮度
    duty: 百分比 x 1,000,000
    """
    pi.hardware_PWM(PWM_LED_PIN,PWM_FREQ,duty)
    

def cleanup():
    """
    清除硬件pwm设置
    """
    pi.set_mode(PWM_LED_PIN,pigpio.INPUT)
    pi.stop()


if __name__ == '__main__':
    try:
        init(2000)
        change(1000000)
        while True:
            pass

    except KeyboardInterrupt:
        print('關閉程式')
    finally:
        cleanup()
