

(function () {
  // ----- State -----
  let examId = null;
  let questions = [];
  let currentIndex = 0;
  
  let answers = {};

  // ----- DOM helpers -----
  function $(id) {
    return document.getElementById(id);
  }

  function showView(name) {
    document.querySelectorAll(".view").forEach((el) => {
      el.hidden = true;
    });
    const view = $(`view-${name}`);
    if (view) view.hidden = false;

    // highlight nav
    document.querySelectorAll(".nav-btn[data-view]").forEach((btn) => {
      btn.style.fontWeight = btn.dataset.view === name ? "650" : "400";
    });
  }

  function setAuthMessage(text, type) {
    const el = $("auth-message");
    if (!text) {
      el.hidden = true;
      el.textContent = "";
      return;
    }
    el.hidden = false;
    el.textContent = text;
    el.className = `message ${type || ""}`;
  }

  function isLoggedIn() {
    return Boolean(API.getToken());
  }

  function updateNav() {
    const nav = $("nav");
    if (isLoggedIn()) {
      nav.hidden = false;
    } else {
      nav.hidden = true;
    }
  }

  // ----- Auth -----
  function setupAuthTabs() {
    document.querySelectorAll(".tab").forEach((tab) => {
      tab.addEventListener("click", () => {
        document.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
        tab.classList.add("active");

        const isLogin = tab.dataset.tab === "login";
        $("login-form").hidden = !isLogin;
        $("register-form").hidden = isLogin;
        setAuthMessage("");
      });
    });
  }

  function setupAuthForms() {
    $("login-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      setAuthMessage("");
      const form = e.target;
      const email = form.email.value.trim();
      const password = form.password.value;

      try {
        const data = await API.login(email, password);
        API.setToken(data.access_token);
        updateNav();
        showView("home");
      } catch (err) {
        setAuthMessage(err.message || "Login failed", "error");
      }
    });

    $("register-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      setAuthMessage("");
      const form = e.target;
      const email = form.email.value.trim();
      const password = form.password.value;

      try {
        await API.register(email, password);
        setAuthMessage("Account created. You can log in now.", "success");
        // switch to login tab
        document.querySelector('.tab[data-tab="login"]').click();
        $("login-form").email.value = email;
      } catch (err) {
        setAuthMessage(err.message || "Registration failed", "error");
      }
    });
  }

  // ----- Exam -----
  function renderQuestion() {
    if (!questions.length) return;

    const q = questions[currentIndex];
    $("exam-progress").textContent = `Question ${currentIndex + 1} / ${questions.length}`;
    $("question-text").textContent = q.text;

    const optionsEl = $("options");
    optionsEl.innerHTML = "";

    const keys = ["A", "B", "C", "D"];
    keys.forEach((key) => {
      const label = q.options[key];
      if (!label) return;

      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "option";
      if (answers[q.id] === key) btn.classList.add("selected");

      btn.innerHTML = `<span class="option-key">${key}.</span><span>${label}</span>`;
      btn.addEventListener("click", () => {
        answers[q.id] = key;
        renderQuestion();
      });

      optionsEl.appendChild(btn);
    });

    $("prev-btn").disabled = currentIndex === 0;

    const isLast = currentIndex === questions.length - 1;
    $("next-btn").hidden = isLast;
    $("submit-exam-btn").hidden = !isLast;
  }

  async function startExam() {
    try {
      const data = await API.startExam();
      examId = data.exam_id;
      questions = data.questions || [];
      currentIndex = 0;
      answers = {};

      if (!questions.length) {
        alert("No questions available. Seed the database first.");
        return;
      }

      showView("exam");
      renderQuestion();
    } catch (err) {
      alert(err.message || "Could not start exam");
    }
  }

  async function submitExam() {
    // ensure current selection is stored (already is via click)
    const unanswered = questions.filter((q) => !answers[q.id]).length;
    if (unanswered > 0) {
      const ok = confirm(`You have ${unanswered} unanswered question(s). Submit anyway?`);
      if (!ok) return;
    }

    try {
      // API expects object with string/number keys
      const payloadAnswers = {};
      Object.keys(answers).forEach((id) => {
        payloadAnswers[id] = answers[id];
      });

      const result = await API.submitExam(examId, payloadAnswers);
      $("result-cefr").textContent = result.cefr_level;
      $("result-score").textContent = `Score: ${result.score} / ${result.total}`;
      showView("result");
    } catch (err) {
      alert(err.message || "Submit failed");
    }
  }

  // ----- Progress -----
  async function loadProgress() {
    const list = $("progress-list");
    list.innerHTML = `<p class="muted">Loading...</p>`;

    try {
      const rows = await API.getProgress();
      if (!rows || !rows.length) {
        list.innerHTML = `<p class="muted">No results yet. Take an exam first.</p>`;
        return;
      }

      list.innerHTML = "";
      rows
        .slice()
        .reverse()
        .forEach((row) => {
          const item = document.createElement("div");
          item.className = "list-item";
          const date = row.date ? new Date(row.date).toLocaleString() : "—";
          item.innerHTML = `
            <span>${date}</span>
            <span>${row.score}/${row.total}</span>
            <span class="level">${row.cefr_level}</span>
          `;
          list.appendChild(item);
        });
    } catch (err) {
      list.innerHTML = `<p class="message error">${err.message || "Failed to load progress"}</p>`;
    }
  }

  // ----- Navigate -----
  function setupNav() {
    document.querySelectorAll("[data-view]").forEach((el) => {
      el.addEventListener("click", () => {
        const view = el.dataset.view;
        if (view === "progress") {
          if (!isLoggedIn()) {
            showView("auth");
            return;
          }
          showView("progress");
          loadProgress();
          return;
        }
        if (view === "home") {
          showView(isLoggedIn() ? "home" : "auth");
          return;
        }
        showView(view);
      });
    });

    $("logout-btn").addEventListener("click", () => {
      API.clearToken();
      updateNav();
      showView("auth");
      setAuthMessage("Logged out.", "success");
    });

    $("start-exam-btn").addEventListener("click", startExam);
    $("prev-btn").addEventListener("click", () => {
      if (currentIndex > 0) {
        currentIndex -= 1;
        renderQuestion();
      }
    });
    $("next-btn").addEventListener("click", () => {
      if (currentIndex < questions.length - 1) {
        currentIndex += 1;
        renderQuestion();
      }
    });
    $("submit-exam-btn").addEventListener("click", submitExam);
  }

  // ----- Init -----
  function init() {
    setupAuthTabs();
    setupAuthForms();
    setupNav();
    updateNav();

    if (isLoggedIn()) {
      showView("home");
    } else {
      showView("auth");
    }
  }

  document.addEventListener("DOMContentLoaded", init);
})();
