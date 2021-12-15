import socketio
import eventlet

socket_io = socketio.Server()
app = socketio.WSGIApp(socket_io)


def make_message(username: str, msg: str) -> str:
    return "%s:%s" % (username, msg)


@socket_io.event
def connect(sio, env):
    print("-----------")
    print("Connect ", sio)
    print("-----------")
    welcome_message = "hello %s , welcome to party room" % sio
    socket_io.emit("message", welcome_message)


@socket_io.on("message")
def my_message(sio, data):
    print(data)
    username, data = data.split(":")
    print("Message from %s : " % username, data)


# room part
@socket_io.on("enter_room")
def add_sio_to_room(sio):
    print("%s Entered the user_chat" % sio)
    socket_io.enter_room(sio, room="user_chat")


@socket_io.on("exit_room")
def remove_sio_from_room(sio):
    print("%s Leaved the user_chat" % sio)
    socket_io.leave_room(sio, room="user_chat")


@socket_io.on("room_message")
def message_in_room(sio, data):
    socket_io.emit("message", data, room="user_chat", skip_sid=sio)


@socket_io.event
def disconnect(sio):
    print("Disconnect ", sio)


if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("127.0.0.1", 4000)), app)