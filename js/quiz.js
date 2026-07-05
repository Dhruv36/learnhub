// Shared quiz engine: pages pass an array of {q, options, answer} and this renders + scores it.
function renderQuiz(questions) {
  const quizEl = document.getElementById("quiz");
  quizEl.innerHTML = questions.map((item, i) => `
    <div class="quiz-q" data-q="${i}">
      <p><strong>Q${i + 1}. ${item.q}</strong></p>
      ${item.options.map((opt, j) => `
        <label><input type="radio" name="q${i}" value="${j}"> ${opt}</label>
      `).join("")}
    </div>
  `).join("");

  document.getElementById("submitBtn").addEventListener("click", () => {
    let score = 0;
    questions.forEach((item, i) => {
      const chosen = document.querySelector(`input[name="q${i}"]:checked`);
      const labels = document.querySelectorAll(`.quiz-q[data-q="${i}"] label`);
      labels.forEach(l => l.classList.remove("correct", "wrong"));
      labels[item.answer].classList.add("correct");
      if (chosen) {
        if (Number(chosen.value) === item.answer) score++;
        else labels[Number(chosen.value)].classList.add("wrong");
      }
    });
    document.getElementById("result").textContent =
      `Your score: ${score} / ${questions.length}` + (score === questions.length ? " 🎉 Perfect!" : "");
  });
}
