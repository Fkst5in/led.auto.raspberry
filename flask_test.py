#!/usr/bin/python3
# _*_ coding: utf-8 _*_

from flask import Flask, request, render_template
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.server import WSGIServer
from geventwebsocket.websocket import WebSocket
from gevent import monkey
from concurrent.futures import ThreadPoolExecutor

import pid as PID
import led
import light
import time

monkey.patch_all()
pid = PID.PID(10000,20000,100)
pid.setSampleTime(0.01)
executor = ThreadPoolExecutor(2)

def adjust_light():
    # 等待开始信号
    while pid.SetPoint == 0.0:
        pass
    try:
        #初始化led及测量电路
        led.init(2000)
        light.init()
        pid.reset()
        while pid.enable:
            print("当前的LED输出是：",-int(pid.output))
            feedback_value = light.measure()
            pid.setLight(feedback_value)
            print("当前的亮度是：",feedback_value)
            print("目标亮度是:",pid.SetPoint / 500)
            pid.update(feedback_value * 500)
            if -pid.output > 1000000:
                led.change(1000000)
                print("超过最大调节上限")
            elif -pid.output < 0:
                led.change(0)
                print("超过最大调节下限")
            else:
                led.change(-int(pid.output))
        return 'over'
            
    except concurrent.futures.CancelledError:
        print("任务中断")
        pid.clear()
        led.cleanup()
        light.cleanup()
    finally:
        print("任务退出")
        pid.clear()
        led.cleanup()
        light.cleanup()   

# PID调节协程名字
main_feture = None
    
app = Flask(__name__)

# 获取亮度区间
@app.route('/info')
def info():
    global main_feture
    
    led.init(2000)
    light.init()
    
    if main_feture is not None:
        pid.cancel()
        
        print(main_feture.result())
        
        main_feture = None

    #led最亮
    led.change(1000000)
    time.sleep(0.1)
    #测量亮度
    max = '{:.05f}'.format(light.measure())
    print('最大亮度:',max)
    #led最暗
    led.change(0)
    time.sleep(0.1)
    #测量亮度
    min = '{:.05f}'.format(light.measure())
    print('最大亮度:',min)

    return {"max:":max,"min":min}

# 开始pid调节
@app.route('/start/<float:light>')
def start(light):
    global main_feture
    pid.setTarget(light * 500)
    main_feture = executor.submit(adjust_light)
    return "success"

# 结束pid调节
@app.route('/stop')
def stop():
    global main_feture
    if main_feture is not None:
        pid.cancel()
        print(main_feture.result())
        main_feture = None
    return "success"

# 更改目标亮度    
@app.route('/change/<float:light>')
def change(light):
    pid.setTarget(light * 500)
    return 'success!'

# 建立一个websocket连接来返回数据
@app.route('/light')
def my_socket():
    user_socket = request.environ.get("wsgi.websocket")
    print(user_socket, "连接已经建立了")
    while True:
        user_socket.send("亮度：{:.05f}".format(pid.light))
        time.sleep(2)
    return "200 ok"

@app.route('/web')
def web():
    return render_template("index.html")

if __name__ == '__main__':
    http_serve = WSGIServer(("0.0.0.0", 8080), app, handler_class=WebSocketHandler)
    http_serve.serve_forever()