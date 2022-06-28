const socket = io("http://127.0.0.1:4000");
let username;
let group_name;

function loading() {
    username = prompt("Enter username: ");
    group_name = prompt("Enter group name: ")
    socket.emit("enter_room", {"username": username, "group_name": group_name})
}


socket.on("message", (data) => {
    console.log("["+data["username"]+"] : " + data["message"]);
})

function send_message() {
    let message = document.getElementById("text_message").value;
    socket.emit("room_message", {"message": message, "username": username, "group_name": group_name});
}

