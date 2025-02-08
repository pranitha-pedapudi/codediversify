let min = 1, max = 100;
let randomNumber = Math.floor(Math.random() * (max - min + 1)) + min;
let chances = 5;

const guessInput = document.getElementById("guessInput");
const guessBtn = document.getElementById("guessBtn");
const message = document.getElementById("message");
const chancesLeft = document.getElementById("chances");
const restartBtn = document.getElementById("restartBtn");

guessBtn.addEventListener("click", checkGuess);
restartBtn.addEventListener("click", restartGame);

// 🎯 Listen for "Enter" key press
document.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        if (!guessInput.disabled) {
            checkGuess();
        } else if (!restartBtn.classList.contains("hidden")) {
            restartGame();
        }
    }
});

function checkGuess() {
    let guess = parseInt(guessInput.value);

    if (isNaN(guess) || guess < min || guess > max) {
        message.innerHTML = "🚨 Enter a number between " + min + " and " + max;
        message.style.color = "red";
        return;
    }

    message.className = ""; // Reset previous styles

    if (guess === randomNumber) {
        message.innerHTML = "🎉 Correct! You guessed it!";
        message.classList.add("correct");
        endGame();
    } else {
        chances--;
        let difference = Math.abs(randomNumber - guess);

        if (chances > 0) {
            if (difference >= 20) {
                message.innerHTML = guess < randomNumber ? "📉 Too Low!" : "📈 Too High!";
                message.classList.add(guess < randomNumber ? "too-low" : "too-high");
            } else if (difference < 20 && difference >= 10) {
                message.innerHTML = guess < randomNumber ? "🔍 Closer!" : "🌡️ High!";
                message.classList.add(guess < randomNumber ? "closer" : "high");
            }

            chancesLeft.innerHTML = chances;
            guessInput.style.animation = "shake 0.5s";
        } else {
            message.innerHTML = `❌ Game Over! The number was <strong>${randomNumber}</strong>`;
            message.className = "game-over";  // Now Game Over is red
            endGame();
        }
    }

    guessInput.value = "";
}

function endGame() {
    guessInput.disabled = true;
    guessBtn.disabled = true;
    restartBtn.classList.remove("hidden");
}

function restartGame() {
    randomNumber = Math.floor(Math.random() * (max - min + 1)) + min;
    chances = 5;
    chancesLeft.innerHTML = chances;
    message.innerHTML = "";
    guessInput.value = "";
    guessInput.disabled = false;
    guessBtn.disabled = false;
    restartBtn.classList.add("hidden");
}
