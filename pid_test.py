#!/usr/bin/python3
# _*_ coding: utf-8 _*_

import pid as PID
import led
import light
import time




#获取可调节的亮度范围
def get_interval():
    #led最亮
    led.change(1000000)
    time.sleep(0.1)
    #测量亮度
    print('最大亮度{:.05f}'.format(light.measure()))
    #led最暗
    led.change(0)
    time.sleep(0.1)
    #测量亮度
    print('最小亮度{:.05f}'.format(light.measure()))


if __name__ == '__main__':
    try:
        led.init(1000) #led初始化
        get_interval() #获取亮度范围
        target = float(input("输入一个介于最大亮度和最小亮度间的亮度：\n> "))

        pid = PID.PID(10000,20000,100)
        pid.setTarget(target * 500)
        pid.setSampleTime(0.01)

        while True:
            print("当前的亮度输出是：",-int(pid.output))
            feedback_value = light.measure()
            print("当前的亮度是：",feedback_value)
            pid.update(feedback_value * 500)
            if -pid.output > 1000000:
                led.change(1000000)
                print("超过最大调节上限")
            elif -pid.output < 0:
                led.change(0)
                print("超过最大调节下限")
            else:
                led.change(-int(pid.output))

            
                
    except KeyboardInterrupt:
        print("程序退出")
    finally:
        led.cleanup()
        light.cleanup()
