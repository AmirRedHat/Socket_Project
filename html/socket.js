const socket = io("http://127.0.0.1:4000");
let username;
let group_name;
let chat_username = "ChatUserName";
let target_user_name;

function loading() {
    let is_valid = checkSession();
    if (is_valid == false){
        username = prompt("Enter username: ");
        socket.emit("check_username", {"username": username}, (response) => {
            let = is_exists = response;
            if (is_exists == true){
                alert("username is exists pick up anotehr")
                loading();
            }
            hello_el = document.getElementById("helloEl");
            hello_el.innerHTML = "Hello " + username
            setSession(chat_username, username);
        });
    }
    else{
        hello_el = document.getElementById("helloEl");
        hello_el.innerHTML = "Hello " + username
    }
}

function checkSession() {
    let session_value = getSession(chat_username);
    if (session_value == null || session_value == "null"){
        return false;
    }
    else{
        username = session_value;
        return true;
    }
}

function setSession(key, value) {
    socket.emit("save_user", {"username": value}, (response) => {
        if (response == "success"){
            localStorage.setItem(key, value);
        }
    });
}

function getSession(key) {
    let value = localStorage.getItem(key);
    return value
}

// -----------------------------------------------------

socket.on("message", (data) => {
    add_message_element("["+data["username"]+"] : " + data["message"])
})

// -----------------------------------------------------


function Exit() {
    localStorage.removeItem(chat_username);
    socket.emit("delete_user", {"username": username})
    loading();
}

function joinGroup() {
    group_name = prompt("Enter group name that you want to join it: ");
    if (group_name == "null"){
        joinGroup();
    }
    else{
        socket.emit("enter_room", {"username": username, "group_name": group_name})
    }
}

function leaveGroup() {
    let group_name = prompt("Enter group name that you want to leave it: ");
    if (group_name == "null"){
        leaveGroup();
    }
    else{
        socket.emit("exit_room", {"username": username, "group_name": group_name});
    }
}

function send_message() {
    let message = document.getElementById("text_message").value;
    add_message_element("["+username+"] : " + message)
    socket.emit("room_message", {"message": message, "username": username, "group_name": group_name});
}


function add_message_element(message_body) {
    message_element = document.createElement("p");
    message_element.append(message_body);
    chat_history = document.getElementById("chat_history");
    chat_history.appendChild(message_element);
}

