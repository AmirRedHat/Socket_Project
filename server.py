import socketio
import eventlet
import cv2
import json

socket_io = socketio.Server()
app = socketio.WSGIApp(socket_io)


@socket_io.event
def connect(sio, env):
    print("-----------")
    print("Connect ", sio)
    print("-----------")


@socket_io.event
def my_message(sio, data):
    print("Message : ", data)


# room part
@socket_io.on("enter_room")
def add_sio_to_room(sio):
    print("%s Entered the user_chat" % sio)
    socket_io.enter_room(sio, room="user_chat")


@socket_io.on("exit_room")
def remove_sio_to_room(sio):
    print("%s Leaved the user_chat" % sio)
    socket_io.leave_room(sio, room="user_chat")


@socket_io.on("room_message")
def message_in_room(sio, data):
    print("sio : ", data)


@socket_io.on("transfer_image")
def transfer_image(sio, data):
    loaded_data = json.loads(data)
    cv2.imwrite("transfer_data.%s" % loaded_data["format"], loaded_data["data"])
    print("Saved!")


@socket_io.on("sum")
def return_datetime(sio, data):
    s = 0
    for i in data: s += i
    socket_io.emit("reply_sum", s)


@socket_io.event
def disconnect(sio):
    print("Disconnect ", sio)


if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("127.0.0.1", 4000)), app)
