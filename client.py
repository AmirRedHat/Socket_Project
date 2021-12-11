import socketio
import cv2
import json

sio = socketio.Client()


@sio.event
def connect():
    print("Connection established")


@sio.event
def my_message(data):
    print("Message : ", data)


@sio.on("reply_sum")
def reply_sum(data):
    print("Reply : ", data)


@sio.event
def disconnect():
    print("Connection failed")


sio.connect("http://127.0.0.1:4000")

is_exiting = False
while not is_exiting:
    message = input(">>> ")
    if message.startswith("sum:"):
        after_dot = message[message.index(":")+1:]
        after_dot.replace(" ", "")
        number1, number2 = after_dot.strip().split(",")
        number1, number2 = int(number1.strip()), int(number2.strip())
        sio.emit("sum", [number1, number2])
    else:
        sio.emit("room_message", message)

    if message == "enter_room":
        sio.emit("enter_room")
    if message == "leave_room":
        print("Leaving...")
        sio.emit("exit_room")

    elif message == "transfer_media":
        img = cv2.imread("186105.jpg")
        content = {"data": img.tolist(), "format": "jpg"}
        json_content = json.dumps(content)
        print(json_content)
        sio.emit("transfer_image", json_content)

    elif message == "exit":
        is_exiting = True
        sio.disconnect()

sio.wait()
