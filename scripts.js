function getBoard() {
    const grid = document.querySelectorAll('#sudoku-grid input');
    let board = [];
    for (let i = 0; i < 9; i++) {
        let row = [];
        for (let j = 0; j < 9; j++) {
            let val = grid[i * 9 + j].value;
            row.push(val ? parseInt(val) : 0);
        }
        board.push(row);
    }
    return board;
}

function showPopup(message) {
    const popup = document.getElementById('popup');
    popup.textContent = message;
    popup.classList.remove('hidden');
    setTimeout(() => popup.classList.add('hidden'), 3000);
}

async function submitAttempt() {
    const board = getBoard();
    const res = await fetch('/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ board })
    });
    const data = await res.json();
    showPopup(data.message);

    // Disable everything if success or fail
    if (data.status === 'success' || data.status === 'fail') {
        document.querySelectorAll('input').forEach(inp => inp.disabled = true);
        document.querySelectorAll('button').forEach(btn => btn.disabled = true);
    }
}

document.getElementById('submit-btn').addEventListener('click', submitAttempt);

document.getElementById('solution-btn').addEventListener('click', async () => {
    const res = await fetch('/solution');
    const data = await res.json();
    const grid = document.querySelectorAll('#sudoku-grid input');
    let k = 0;
    data.solution.flat().forEach(num => {
        grid[k].value = num;
        grid[k].disabled = true;
        k++;
    });
});

document.getElementById('restart-btn').addEventListener('click', async () => {
    const res = await fetch('/restart');
    const data = await res.json();
    const grid = document.querySelectorAll('#sudoku-grid input');
    let k = 0;
    data.puzzle.flat().forEach(num => {
        grid[k].value = num === 0 ? '' : num;
        grid[k].disabled = num !== 0;
        k++;
    });
    document.querySelectorAll('button').forEach(btn => btn.disabled = false);
    showPopup(data.message);
});
