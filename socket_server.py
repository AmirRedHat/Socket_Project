import socketio
import eventlet
import os

from flask import Flask, request, render_template
from flask_cors import CORS


html_path = "/home/amir/Desktop/Amir Hosein/Projects/Socket_Project/html/"
flask_app = Flask(__name__, template_folder=html_path, static_folder=html_path, static_url_path="/static")


socket_io = socketio.Server()
app = socketio.WSGIApp(socket_io, flask_app)
password_server = "ServerIsForFun"



@flask_app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# ------------------------------------------------

@socket_io.event
def connect(sio, env):
    print("Connect ", sio)


@socket_io.on("echo")
def echo(sio, data):
    print("CLIENT (%s): " % sio, data["message"])


# @socket_io.on("save_session")
# def save_user_session(sio, data):
#     data["id"] = sio
#     socket_io.save_session(sio, data)
#     welcome_message = "hello %s , welcome to party room" % data["username"]
#     socket_io.emit("message", welcome_message)


@socket_io.on("superuser")
def make_superuser(sio, data):
    password = data["password"]
    session = socket_io.get_session(sio)
    data = {"username": "SERVER"}
    if password == password_server:
        session["is_superuser"] = True
        socket_io.save_session(sio, session)
        data["message"] = "You are superuser now"
    else:
        data["message"] = "Password is invalid"
    socket_io.emit("message", data)


def remove_user_by_admin():
    pass


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
    socket_io.emit("message", enter_message, room=group_name, skip_sid=sio)


@socket_io.on("exit_room")
def remove_user_from_room(sio, data):
    """
        data = { username, group_name }
    """
    username = data["usernamne"]
    group_name = data["group_name"]
    print("%s Leaved the user_chat" % username)
    socket_io.leave_room(sio, room=group_name)
    exit_message = "%s left the group" % username
    socket_io.emit("message", exit_message, room=group_name, skip_sid=sio)


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
    # web.run_app(app)
