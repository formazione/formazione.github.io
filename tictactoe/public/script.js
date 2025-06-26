const socket = io();

const cells = document.querySelectorAll('.cell');
let currentPlayer = 'X';

cells.forEach(cell => {
    cell.addEventListener('click', () => {
        if (cell.textContent === '') {
            socket.emit('makeMove', { index: cell.dataset.index, player: currentPlayer });
        }
    });
});

socket.on('moveMade', ({ index, player }) => {
    cells[index].textContent = player;
    currentPlayer = player === 'X' ? 'O' : 'X';
});

socket.on('reset', () => {
    cells.forEach(cell => cell.textContent = '');
    currentPlayer = 'X';
});
