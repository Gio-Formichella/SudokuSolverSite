const ws = new WebSocket("ws://" + window.location.host + "/ws/board/");
console.log(ws)

const solveButton = document.querySelector('.solve-button');
const stopButton = document.querySelector('.stop-button');
const sudokuBoard = document.querySelector('.board');


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

solveButton.addEventListener('click', () => {
  const puzzle = getPuzzle();
  ws.send(JSON.stringify(puzzle));
});

stopButton.addEventListener('click', () => {
  // Add logic to handle stopping the solving process (if applicable)
  console.log("Stopping solving...");  // Placeholder for your stop functionality
});

function updateBoard(solutionData) {
  for (let row = 0; row < 9; row++) {
    for (let col = 0; col < 9; col++) {
      const cell = document.getElementById(`cell-${row}-${col}`);
      cell.value = solutionData[row][col];
    }
  }
}

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    board = message[0]
    updateBoard(board);
};
