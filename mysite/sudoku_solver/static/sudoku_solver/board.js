const ws = new WebSocket("ws://" + window.location.host + "/ws/board/");
console.log(ws)

const solveButton = document.querySelector('.solve-button');
const sudokuBoard = document.querySelector('.board');
const messageElement = document.querySelector('.solution-message');

let puzzle; // Will hold user puzzle

function getPuzzle() {
  const puzzle = [];
  for (let row = 0; row < 9; row++) {
    const rowData = [];
    for (let col = 0; col < 9; col++) {
      const cell = document.getElementById(`cell-${row}-${col}`);
      const value = parseInt(cell.value) || null;
      rowData.push(value);
    }
    puzzle.push(rowData);
  }
  return puzzle;
}


function updateBoard(solutionData) {
  for (let row = 0; row < 9; row++) {
    for (let col = 0; col < 9; col++) {
      const cell = document.getElementById(`cell-${row}-${col}`);
      cell.value = solutionData[row][col];
    }
  }
}

function flashBoardRed() {
  for (let row = 0; row < 9; row++) {
    for (let col = 0; col < 9; col++) {
      const cell = document.getElementById(`cell-${row}-${col}`);
      cell.style.background = '#f00'; // Set red background
      setTimeout(() => {
          cell.style.background = '#fff'; // Reset to white background
      }, 200); // Delay (in milliseconds)
    }
  }
}

function displayMessage(message, type) {
    if (type == "no-solution") {
        messageElement.textContent = message;
        messageElement.classList.add('error-message');
    }
}

solveButton.addEventListener('click', () => {
  puzzle = getPuzzle();
  ws.send(JSON.stringify(puzzle));
  messageElement.classList.remove('error-message');
});

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    if (message === null) {
        // puzzle has no solution
        flashBoardRed();
        displayMessage("Puzzle has no solution", "no-solution")
        if (puzzle){
            updateBoard(puzzle)
        }
    }
    else {
        board = message[0]
        updateBoard(board);
    }
};
