const ws = new WebSocket("ws://" + window.location.host + "/ws/board/");
console.log(ws)

const solveButton = document.querySelector('.solve-button');
const sudokuBoard = document.querySelector('.board');
const messageElement = document.querySelector('.solution-message');
const resetButton = document.querySelector('.reset-button');
const stepByStepButton = document.querySelector('.step-by-step-button');

let puzzle; // Will hold user puzzle
const stepByStepMessageQueue = [];  // holds updates
let stepByStepCounter = 0  // updates counter
let interval;  // Reference to interval, used to stop

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
  ws.send(JSON.stringify({
    "type": "solve",
    "puzzle": puzzle
    }
  ));
  messageElement.textContent = "";
  messageElement.classList.remove('error-message');
});

resetButton.addEventListener('click', () => {
    // Stopping backend from sending updates
    ws.send(JSON.stringify({
        "type": "reset"
    }))
    //TODO: possible bug: rare case where the backend sends an update before flag change and after board clear

    // Clearing board
    for (let row = 0; row < 9; row++) {
        for (let col = 0; col < 9; col++) {
            const cell = document.getElementById(`cell-${row}-${col}`);
            cell.value = "";
        }
    }
});

stepByStepButton.addEventListener('click', () => {
  puzzle = getPuzzle();
  ws.send(JSON.stringify({
    "type": "step-by-step",
    "puzzle": puzzle
  }));
  messageElement.textContent = "";
  messageElement.classList.remove('error-message');
});


ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    switch(message.type){
        case "solve":
            if (message.board === null){
                // puzzle has no solution
                flashBoardRed();
                displayMessage("Puzzle has no solution", true)
            } else {
                updateBoard(message.board);
                displayMessage(message.msg, false)
            }
            break;
        case "step-by-step":
            stepByStepMessageQueue.push(message)
            if (stepByStepCounter == 0) {
                stepByStepCounter++;
                interval = setInterval(displayStepByStepUpdates, 100);
            }
            break;
    }
};

function displayStepByStepUpdates() {
    found = false;
    i = 0; // queue iterator
    while (!found && i < stepByStepMessageQueue.length){
        if (stepByStepMessageQueue[i].count == stepByStepCounter){
            // updating data
            update = stepByStepMessageQueue[i];
            const cell = document.getElementById(`cell-${update.row}-${update.col}`);
            cell.value = update.value;
            // flashing update green
            cell.style.background = '#04AA6D';
            setTimeout(() => {
                cell.style.background = '#fff'; // Reset to white background
            }, 200); // Delay (in milliseconds)

            found = true;
            stepByStepCounter++;
        }
        i++;
    }
}