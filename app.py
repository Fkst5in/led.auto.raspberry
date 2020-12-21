#!/usr/bin/python3
# _*_ coding: utf-8 _*_
# 引入 flask web框架
# 引入 geven-websocket 实现 websocket
# 引入 monkey 实现非阻塞的 websocket
from flask import Flask, request, render_template
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.server import WSGIServer
from geventwebsocket.websocket import WebSocket
from gevent import monkey
from concurrent.futures import ThreadPoolExecutor
# 引入led_pid类
# from controller import LED_PID
import controller
# 一定一些全局变量
monkey.patch_all()

led_pid = controller.LED_PID(10000,20000,100,0.01)
executor = ThreadPoolExecutor(2)
main_feture = None

app = Flask(__name__)

#挂载路由

# 渲染web页面
@app.route('/')
def web():
    # return render_template("index.html") #这个需要使用jinja2模版引擎
    return app.send_static_file('index.html')

#获取可调节的亮度范围
@app.route('/info')
def info():
    global main_feture
    # 判断是否在调节中
    if main_feture is not None:
        # 结束调节
        led_pid.cancel()
        # 等待协程结束
        print(main_feture.result())
        main_feture = None
    # 测量
    return controller.get_interval()

#获取当前亮度及调节目标亮度
@app.route('/light',methods=['GET', 'POST'])
def light():
    if request.methods = 'GET':
        return {"now":led_pid.light,"target":led_pid.target,"success":True}
    elif request.methods = 'POST':
        global main_feture

        try:
            # 可能是无效的数据
            value = float(request.form['value'])
        except:
            return {"success":False,"message":"Invalid input"}
        else:

            # 判断是否在调节中
            if main_feture is None:
                # 不在调节中
                led_pid.setTarget(value)
                main_feture = executor.submit(led_pid.led_adjust)
                return {"target":led_pid.target,"success":True}
            elif:
                # 已在调节中
                led_pid.setTarget(value)
                return {"target":led_pid.target,"success":True}
    else:
        return {"success":False,"message":"Invalid method"}

# websocket连接，用于实时监听led调节信息
@app.route('/listen')
def listen():
    led_socket = request.environ.get("wsgi.websocket")
    print("- ",led_socket," 连接已建立")
    while True:
        led_socket.send("亮度：{:.05f}".format(led_pid.light))
        sleep(2)
    return {"success":True}

@app.route('/stop')
def stop():
    global main_feture
    # 判断是否在调节中
    if main_feture is not None:
        # 结束调节
        led_pid.cancel()
        # 等待协程结束
        print(main_feture.result())
        main_feture = None
    return {"success":True}

# 启动app
if __name__ == '__main__':
    http_serve = WSGIServer(("0.0.0.0", 9090), app, handler_class=WebSocketHandler)
    http_serve.serve_forever()