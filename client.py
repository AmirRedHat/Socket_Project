import socketio
import cv2
import json

sio = socketio.Client()


def make_message(username: str, msg: str) -> str:
    return "%s:%s" % (username, msg)


@sio.event
def connect():
    print("Connection established")


@sio.on("message")
def my_message(data):
    try:
        username, data = data.split(":")
        print("Message from %s : " % username, data)
    except:
        print("Message : ", data)

@sio.event
def disconnect():
    print("Connection failed")


sio.connect("http://127.0.0.1:4000")

is_exiting = False
username = input("Enter a username: ")
sio.emit("enter_room")
while not is_exiting:
    message = input(">>> ")
    if message == "leave_room":
        print("Leaving...")
        sio.emit("exit_room")
    elif message == "exit":
        is_exiting = True
        sio.disconnect()
    else:
        sio.emit("room_message", make_message(username, message))

sio.wait()
