const quizData = [
    {
        question: "What does HTML stand for?",
        options: ["Hyper Text Markup Language", "Home Tool Markup Language", "Hyperlinks and Text Markup Language"],
        correct: 0
    },
    {
        question: "Which programming language is known as the language of the web?",
        options: ["Python", "JavaScript", "C++"],
        correct: 1
    },
    {
        question: "What does CSS stand for?",
        options: ["Creative Style Sheets", "Cascading Style Sheets", "Computer Styled Sections"],
        correct: 1
    }
];

let currentQuestionIndex = 0;
let score = 0;

const questionEl = document.getElementById("question");
const optionsEl = document.getElementById("options");
const nextButton = document.getElementById("next-btn");
const resultContainer = document.getElementById("result");
const scoreEl = document.getElementById("score");

function loadQuestion() {
    if (currentQuestionIndex >= quizData.length) {
        showResult();
        return;
    }

    const currentQuestion = quizData[currentQuestionIndex];
    questionEl.textContent = currentQuestion.question;
    optionsEl.innerHTML = "";

    currentQuestion.options.forEach((option, index) => {
        const button = document.createElement("button");
        button.textContent = option;
        button.classList.add("option");
        button.onclick = () => checkAnswer(index);
        optionsEl.appendChild(button);
    });

    nextButton.style.display = "none";
}

function checkAnswer(selectedIndex) {
    const currentQuestion = quizData[currentQuestionIndex];
    if (selectedIndex === currentQuestion.correct) {
        score++;
    }

    currentQuestionIndex++;
    nextButton.style.display = "block";
}

function nextQuestion() {
    loadQuestion();
}

function showResult() {
    document.getElementById("quiz").classList.add("hide");
    resultContainer.classList.remove("hide");
    scoreEl.textContent = `${score} / ${quizData.length}`;
}

function restartQuiz() {
    currentQuestionIndex = 0;
    score = 0;
    resultContainer.classList.add("hide");
    document.getElementById("quiz").classList.remove("hide");
    loadQuestion();
}

loadQuestion();
