const quizContainer = document.getElementById("quiz-container");
const questionElement = document.getElementById("question");
const choicesElement = document.getElementById("choices");
const nextButton = document.getElementById("next-button");
const resultElement = document.getElementById("result");
const explanationElement = document.getElementById("explanation");

let questions = [];
let currentQuestionIndex = 0;

fetch("ex_questions.json")
    .then(response => response.json())
    .then(data => {
        questions = data;
        loadQuestion(currentQuestionIndex);
    })
    .catch(error => console.error("Error loading questions:", error));

function loadQuestion(index) {
    const question = questions[index];
    questionElement.textContent = question.question;

    choicesElement.innerHTML = "";
    question.choices.forEach((choice, choiceIndex) => {
        const choiceButton = document.createElement("button");
        choiceButton.textContent = String.fromCharCode(65 + choiceIndex) + ". " + choice;
        choiceButton.className = "choice-button";
        choiceButton.addEventListener("click", () => selectAnswer(choiceIndex));
        choicesElement.appendChild(choiceButton);
        choicesElement.appendChild(document.createElement("br"));
    });
}

function selectAnswer(choiceIndex) {
    const correctAnswerIndices = Array.isArray(questions[currentQuestionIndex].correct_answer_index)
        ? questions[currentQuestionIndex].correct_answer_index
        : [questions[currentQuestionIndex].correct_answer_index];

    if (correctAnswerIndices.includes(choiceIndex)) {
        resultElement.innerHTML = "Correct!<br><br>";
    } else {
        const correctLetters = correctAnswerIndices.map(index => String.fromCharCode(65 + index));
        const correctChoices = correctAnswerIndices.map(index => questions[currentQuestionIndex].choices[index]); 
        resultElement.innerHTML = "Incorrect. <br><br>The correct answer(s) are: <br>" + formatCorrectAnswers(correctLetters, correctChoices) + "<br><br>";
    }

    explanationElement.textContent = questions[currentQuestionIndex].explanation;

    nextButton.disabled = false;
}
    
function formatCorrectAnswers(letters, choices) {
    const formattedAnswers = letters.map((letter, index) => letter + ". " + choices[index]);
    return formattedAnswers.join("<br>");
}

function nextQuestion() {
    currentQuestionIndex++;
    if (currentQuestionIndex < questions.length) {
        loadQuestion(currentQuestionIndex);
        resultElement.textContent = "";
        explanationElement.textContent = "";
        nextButton.disabled = true;
    } else {
        quizContainer.innerHTML = "<h2>Quiz Completed!</h2>";
    }
}


nextButton.addEventListener("click", () => {
    nextQuestion();
});
