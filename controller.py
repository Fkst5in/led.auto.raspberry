
#!/usr/bin/python3
# _*_ coding: utf-8 _*_

from pid.pid import PID
import hardware.led_pwm.led
import hardware.rc_oscillator.rc

#新建一个PID的子类，用于led的pid调光
class LED_PID(PID):    
    def clear(self):
        self.current_time = time.time()
        self.last_time = self.current_time  
        self.target = 0.0
        self.light = 0.0
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0
        self.int_error = 0.0
        self.output = 0.0
        self.enable = True 

    def reset(self):
        self.current_time = time.time()
        self.last_time = self.current_time  

    def setLight(self,light):
        self.light = light

    def cancel(self):
        self.enable = False

    def led_adjust(self):
        # 初始化pid的时间
        self.reset()
        # 外部硬件的初始化
        led.init(2000) #初始化led
        rc.init()
        # 等待开始
        while self.target == 0.0:
            pass
        try:
            print("- PID自动调节开始")
            while self.enable:
                feedback_value = rc.measure()
                self.setLight = feedback_value
                self.update(feedback_value) 
                # 判断是否
                if -self.output > 1000000:
                    led.change(1000000)
                elif -self.output < 0:
                    led.change(0)
                else:
                    led.change(-int(self.output))
            return '- PID自动调节结束'            
        finally:
            self.clear()
            led.cleanup()
            rc.cleanup()

def get_interval():
    #初始化
    led.init(2000)
    rc.init()
    #led最亮
    led.change(1000000)
    time.sleep(0.1)
    #测量亮度
    max = '{:.05f}'.format(rc.measure())
    print('最大亮度:',max)
    #led最暗
    led.change(0)
    time.sleep(0.1)
    #测量亮度
    min = '{:.05f}'.format(rc.measure())
    print('最大亮度:',min)

    return {"max:":max,"min":min}


    