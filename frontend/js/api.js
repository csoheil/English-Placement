

const API_BASE = "http://localhost:8000/api/v1";

function getToken() {
  return localStorage.getItem("access_token");
}

function setToken(token) {
  localStorage.setItem("access_token", token);
}

function clearToken() {
  localStorage.removeItem("access_token");
}

/**
 * @param {string} path - path after /api/v1
 * @param {object} options - fetch options
 */
async function request(path, options = {}) {
  const headers = { ...(options.headers || {}) };

  const token = getToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  // JSON body
  if (options.body && !(options.body instanceof URLSearchParams) && !(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
    if (typeof options.body !== "string") {
      options.body = JSON.stringify(options.body);
    }
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  let data = null;
  const text = await res.text();
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = text;
    }
  }

  if (!res.ok) {
    const detail = data && data.detail ? data.detail : res.statusText;
    const error = new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
    error.status = res.status;
    error.data = data;
    throw error;
  }

  return data;
}

/** Register */
function register(email, password) {
  return request("/auth/register", {
    method: "POST",
    body: { email, password },
  });
}

/**
 * Login with email + password.
 */
function login(email, password) {
  const body = new URLSearchParams();
  body.set("username", email);
  body.set("password", password);

  return request("/auth/login", {
    method: "POST",
    body,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
}

/**new exam */
function startExam() {
  return request("/exams/start", { method: "POST" });
}

/**
 * Submit answers 
 * @param {number} examId
 * @param {Object.<string|number, string>} answers - questionId -> "A"|"B"|"C"|"D"
 */
function submitExam(examId, answers) {
  return request("/results/submit", {
    method: "POST",
    body: {
      exam_id: examId,
      answers,
    },
  });
}

/** Get user progress **/
function getProgress() {
  return request("/progress/", { method: "GET" });
}

/** Get exam history*/
function getHistory(page = 1, pageSize = 10) {
  return request(`/history/?page=${page}&page_size=${pageSize}`, { method: "GET" });
}

// Expose for app.js
window.API = {
  getToken,
  setToken,
  clearToken,
  register,
  login,
  startExam,
  submitExam,
  getProgress,
  getHistory,
};
