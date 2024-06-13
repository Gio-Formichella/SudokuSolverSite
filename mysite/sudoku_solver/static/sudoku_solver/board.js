const ws = new WebSocket("ws://" + window.location.host + "/ws/board/");
console.log(ws)

const solveButton = document.querySelector('.solve-button');
const sudokuBoard = document.querySelector('.board');
const messageElement = document.querySelector('.solution-message');
const resetButton = document.querySelector('.reset-button');

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
      if (cell.value != puzzle[row][col]){
          // flashing green the new additions
          cell.style.background = '#04AA6D';
          setTimeout(() => {
              cell.style.background = '#fff'; // Reset to white background
          }, 200); // Delay (in milliseconds)
      }
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

function displayMessage(message, error) {
    messageElement.textContent = message;
    if (error) {
        messageElement.classList.add('error-message');
    }
}

solveButton.addEventListener('click', () => {
  puzzle = getPuzzle();
  ws.send(JSON.stringify(puzzle));
  messageElement.textContent = "";
  messageElement.classList.remove('error-message');
});

resetButton.addEventListener('click', () => {
    // Stopping backend from sending updates
    ws.send(JSON.stringify({"reset": true}))
    //TODO: possible bug: rare case where the backend sends an update before flag change and after board clear

    // Clearing board
    for (let row = 0; row < 9; row++) {
        for (let col = 0; col < 9; col++) {
            const cell = document.getElementById(`cell-${row}-${col}`);
            cell.value = "";
        }
    }
});

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    if (message === null) {
        // puzzle has no solution
        flashBoardRed();
        displayMessage("Puzzle has no solution", true)
        updateBoard(puzzle)
    }
    else {
        board = message.board
        updateBoard(board);
        displayMessage(message.msg, false)
    }
};
