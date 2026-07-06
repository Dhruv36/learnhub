// Shared quiz engine v2: {q, options, answer, explain?} — renders, scores,
// reveals per-question explanations after submit, and offers a retake.
function renderQuiz(questions) {
  const quizEl = document.getElementById("quiz");
  quizEl.innerHTML = questions.map((item, i) => `
    <div class="quiz-q" data-q="${i}">
      <p><strong>Q${i + 1}. ${item.q}</strong></p>
      ${item.options.map((opt, j) => `
        <label><input type="radio" name="q${i}" value="${j}"> ${opt}</label>
      `).join("")}
      ${item.explain ? `<div class="quiz-explain">💡 ${item.explain}</div>` : ""}
    </div>
  `).join("");

  const submitBtn = document.getElementById("submitBtn");
  submitBtn.textContent = "Submit Answers";
  submitBtn.onclick = () => {
    let score = 0, attempted = 0;
    questions.forEach((item, i) => {
      const chosen = document.querySelector(`input[name="q${i}"]:checked`);
      const qEl = document.querySelector(`.quiz-q[data-q="${i}"]`);
      const labels = qEl.querySelectorAll("label");
      labels.forEach(l => l.classList.remove("correct", "wrong"));
      labels[item.answer].classList.add("correct");
      qEl.classList.add("revealed");
      if (chosen) {
        attempted++;
        if (Number(chosen.value) === item.answer) score++;
        else labels[Number(chosen.value)].classList.add("wrong");
      }
    });
    const pct = Math.round((score / questions.length) * 100);
    const grade = pct >= 90 ? "🏆 Outstanding!" : pct >= 75 ? "🎉 Great — solid grasp." :
                  pct >= 50 ? "📖 Getting there — review the explanations below." :
                  "💪 Revisit the lessons, then retake.";
    document.getElementById("result").innerHTML =
      `Score: ${score} / ${questions.length} (${pct}%) — ${grade}` +
      (attempted < questions.length ? `<br><small>${questions.length - attempted} unanswered</small>` : "") +
      ` <button class="btn btn-outline" style="margin-left:.8rem" onclick="location.reload()">Retake</button>`;
    document.getElementById("result").scrollIntoView({ behavior: "smooth", block: "nearest" });
  };
}
