import socketio
import eventlet
from datetime import datetime
from hashlib import sha256
import os

socket_io = socketio.Server()
app = socketio.WSGIApp(socket_io)
password_server = "ServerIsForFun"

def make_password():
    now_str = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    hashed_now_str = sha256(now_str.encode())
    return hashed_now_str.hexdigest()


def authenticate(password: str) -> bool:
    if password == password_server:
        return True
    return False


@socket_io.event
def connect(sio, env):
    print("Connect ", sio)


@socket_io.on("save_session")
def save_user_session(sio, data):
    data["id"] = sio
    socket_io.save_session(sio, data)
    welcome_message = "hello %s , welcome to party room" % data["username"]
    socket_io.emit("message", welcome_message)


@socket_io.on("superuser")
def make_superuser(sio, data):
    password = data["password"]
    session = socket_io.get_session(sio)
    data = {"username": "SERVER"}
    if authenticate(password=password):
        session["is_superuser"] = True
        socket_io.save_session(sio, session)
        data["message"] = "You are superuser now"
    else:
        data["message"] = "Password is invalid"    
    socket_io.emit("message", data)


@socket_io.on("remove_user")
def remove_user_by_username(sio, data):
    session = socket_io.get_session(sio)
    username = data["username"]
    if session["is_superuser"]:
        socket_io.emit("left_the_group")
        msg = "%s removed %s" % (session["username"], username)
        print(msg)
        data["message"] = msg
        socket_io.emit("message", data=data, room="user_chat")
    else:
        socket_io.emit("message", {"username": "SERVER", "message": "You are not superuser"})


@socket_io.on("message")
def my_message(sio, data):
    username, data = data.split(":")
    print("Message from %s : " % username, data)


# room part
@socket_io.on("enter_room")
def add_sio_to_room(sio):
    session = socket_io.get_session(sio)
    username = session["username"]
    print("%s Entered the user_chat" % username)
    socket_io.enter_room(sio, room="user_chat")
    enter_message = "%s joined the group" % username
    socket_io.emit("message", enter_message, room="user_chat", skip_sid=sio)


@socket_io.on("exit_room")
def remove_sio_from_room(sio):
    session = socket_io.get_session(sio)
    username = session["usernamne"]
    print("%s Leaved the user_chat" % username)
    socket_io.leave_room(sio, room="user_chat")
    exit_message = "%s left the group" % username
    socket_io.emit("message", exit_message, room="user_chat", skip_sid=sio)


@socket_io.on("room_message")
def message_in_room(sio, data):
    session = socket_io.get_session(sio)
    data = {"message": data, "username": session["username"]}
    socket_io.emit("message", data, room="user_chat", skip_sid=sio)


@socket_io.on("media")
def media_in_room(sio, data):
    file_name = data["name"]
    file_format = data["format"]
    data = data["data"]
    media_folder = "./media"
    if not os.path.isdir(media_folder):
        os.mkdir(media_folder)

    path = "%s/%s.%s" % (media_folder, file_name, file_format)
    with open(path, "wb") as _file:
        _file.write(data)
        _file.close()
    print("file saved in ", path)
    

@socket_io.event
def disconnect(sio):
    print("Disconnect ", sio)


if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("127.0.0.1", 4000)), app)