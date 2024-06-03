console.log("Hello world")
// Create a WebSocket connection to the specified URL
const socket = new WebSocket(
    "ws://" + window.location.host + "/ws/board/"
)
console.log(socket)

// Socket message listener to handle messages from the server
socket.onmessage = (e) => {
    console.log({"Server": e.data})
}

// 'open' event listener to handle connection being enstablished
socket.onopen = (e) => {
    socket.send(JSON.stringify({
        "message": "Hello from client"
    }))
}