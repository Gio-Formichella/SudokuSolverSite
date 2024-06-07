console.log("Hello world");

// Create a WebSocket connection to the specified URL
const socket = new WebSocket(
  "ws://" + window.location.host + "/ws/board/"
);
console.log(socket);

// Socket message listener to handle messages from the server
socket.onmessage = (e) => {
  const data = JSON.parse(e.data);
  if (data.hasOwnProperty("solved_board")) {
    const solvedBoard = data.solved_board;
    for (let i = 0; i < 9; i++) {
      for (let j = 0; j < 9; j++) {
        const cellId = `cell-${i}-${j}`;
        const cellElement = document.getElementById(cellId);
        cellElement.value = solvedBoard[i][j];
      }
    }
  }
};

// 'open' event listener to handle connection being established
socket.onopen = (e) => {
  socket.send(JSON.stringify({ message: "Hello from client" }));
};

// Function to capture user input and send updated puzzle state
function sendUpdatedPuzzle() {
  const puzzle = [];
  for (let i = 0; i < 9; i++) {
    puzzle[i] = [];
    for (let j = 0; j < 9; j++) {
      const cellId = `cell-${i}-${j}`;
      const cellElement = document.getElementById(cellId);
      puzzle[i][j] = parseInt(cellElement.value) || 0; // Handle empty cells as 0
    }
  }
  socket.send(JSON.stringify({ puzzle }));
}

// Add event listener to the solve button
const solveButton = document.querySelector(".solve-button");
solveButton.addEventListener("click", sendUpdatedPuzzle);
