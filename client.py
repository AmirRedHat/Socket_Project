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

login_or_signin = input("Login or SignIn? [L or S]: ")
if login_or_signin.lower() == "l" or login_or_signin.lower() == "login":
    username = input("enter username: ")
    password = input("enter password: ")
    sio.emit("authenticate", {"username": username, "password": password})
elif login_or_signin.lower() == "s" or login_or_signin.lower() == "signin":
    username = input("enter username: ")
    password = input("enter password: ")
    sio.emit("register", {"username": username, "password": password})
else:
    raise Exception("invalid parameter")


is_exiting = False
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
    elif message == "share_media":
        path = input("Enter Path: ")
        path = path.replace("\\", "/")
        file_name = path.split("/")[-1]
        file_format = file_name.split(".")[-1]
        with open(path, "rb") as _file:
            data = _file.read()
            sio.emit("media", {"data": data, "format": file_format, "name": file_name})
            _file.close()
    else:
        sio.emit("room_message", message)

sio.wait()
