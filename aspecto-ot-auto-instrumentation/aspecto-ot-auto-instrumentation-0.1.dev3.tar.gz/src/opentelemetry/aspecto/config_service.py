#!/usr/bin/python
import socketio


def get_config(token, callback):
    sio = socketio.Client()

    @sio.on("config")
    def on_config(config):
        callback(config)

    @sio.on("connect")
    def on_connect():
        sio.emit("get-config")

    @sio.event
    def connect_error():
        pass

    @sio.event
    def disconnect():
        pass

    sio.connect("https://config.aspecto.io?token=" + token)
    # sio.connect("http://localhost:1080?token=" + token)
