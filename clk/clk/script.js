// script.js
let score = 0;
const scoreDisplay = document.getElementById("score");
const target = document.getElementById("target");
const gameArea = document.getElementById("game-area");

function getRandomPosition() {
    const areaWidth = gameArea.clientWidth;
    const areaHeight = gameArea.clientHeight;
    const x = Math.floor(Math.random() * (areaWidth - 50));
    const y = Math.floor(Math.random() * (areaHeight - 50));
    return { x, y };
}

function moveTarget() {
    const { x, y } = getRandomPosition();
    target.style.left = `${x}px`;
    target.style.top = `${y}px`;
    target.style.display = "block";
}

target.addEventListener("click", () => {
    score++;
    scoreDisplay.textContent = score;
    moveTarget();
});

// Start the game by moving the target every second
setInterval(moveTarget, 1000);
