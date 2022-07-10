import socketio
import eventlet
import os

from flask import Flask, render_template
from backend import BackEnd


html_path = "/home/amir/Desktop/Amir Hosein/Projects/Socket_Project/html/"
flask_app = Flask(__name__, template_folder=html_path, static_folder=html_path, static_url_path="/static")


socket_io = socketio.Server()
app = socketio.WSGIApp(socket_io, flask_app)
password_server = "ServerIsForFun"
backend = BackEnd()



@flask_app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# ------------------------------------------------

@socket_io.on("connect")
def connect(sio, env):
    print("Connect ", sio)


@socket_io.on("check_username")
def check_username(io, data):
    # print("username in check_username: ", data["username"])
    user = backend.read_user({"username": data["username"]})
    if user:
        return True
    else:
        return False


@socket_io.on("save_user")
def save_user(sio, data):
    return backend.write_user(data)

@socket_io.on("delete_user")
def delete_user(sio, data):
    return backend.delete_user(data)


@socket_io.on("enter_room")
def add_user_to_room(sio, data):
    """
        data = { username, group_name }
    """
    username = data["username"]
    group_name = data["group_name"]
    print("%s Entered the user_chat" % username)
    socket_io.enter_room(sio, room=group_name)
    enter_message = "%s joined the group" % username
    data = {"username": "SERVER", "message": enter_message}
    socket_io.emit("message", data, room=group_name, skip_sid=sio)


@socket_io.on("exit_room")
def remove_user_from_room(sio, data):
    """
        data = { username, group_name }
    """
    username = data["username"]
    group_name = data["group_name"]
    print("%s Leaved the user_chat" % username)
    socket_io.leave_room(sio, room=group_name)
    exit_message = "%s left the group" % username
    data = {"username": "SERVER", "message": exit_message}
    socket_io.emit("message", data, room=group_name, skip_sid=sio)


@socket_io.on("room_message")
def message_in_room(sio, data):
    """
        data = { username, message, group_name }
    """
    username = data["username"]
    message = data["message"]
    group_name = data["group_name"]
    data = {"message": message, "username": username}
    socket_io.emit("message", data, room=group_name, skip_sid=sio)


@socket_io.on("disconnect")
def disconnect(sio):
    pass


if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("127.0.0.1", 4000)), app)
    # web.run_app(app)
