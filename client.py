import socketio
from datetime import datetime

sio = socketio.Client()


@sio.event
def connect():
    print("Connection established")


@sio.on("message")
def my_message(data):
    try:
        username, msg = data["username"], data["message"]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("[%s] %s : " % (now, username), msg)
    except:
        print("Message : ", data)

@sio.on("left_the_group")
def left_the_group():
    sio.emit("exit_room")


@sio.event
def disconnect():
    print("Connection failed")


sio.connect("http://127.0.0.1:4000")

is_exiting = False
username = input("Enter a username: ")
joined_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
sio.emit("save_session", {"username": username,
                          "joinded_date": joined_date})
sio.emit("enter_room")
while not is_exiting:
    message = input("[You] >>> ")

    if message.startswith("remove"):
        command, username = message.split(" ")
        sio.emit("remove_user", {"username", username})

    if message == "leave_room":
        print("Leaving...")
        left_the_group()
    elif message == "want_superuser":
        password = input("Enter Password: ")
        sio.emit("superuser", {"password": password})
    elif message == "exit":
        is_exiting = True
        sio.disconnect()
    else:
        sio.emit("room_message", message)

sio.wait()
