// Node.js track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Runtime Foundations", items: [
    ["The Node Runtime", "index.html"],
    ["Modules: CommonJS & ESM", "modules.html"],
    ["npm, package.json & Dependencies", "npm.html"],
    ["Files, Paths & Buffers", "fs-buffers.html"],
    ["Process, Environment & CLI", "process-cli.html"]] },
  { title: "2. Async Node", items: [
    ["The Event Loop & libuv", "event-loop.html"],
    ["Async Patterns", "async-patterns.html"],
    ["EventEmitter", "events.html"],
    ["Streams & Backpressure", "streams.html"]] },
  { title: "3. Building APIs", items: [
    ["HTTP Without Frameworks", "http.html"],
    ["Express Fundamentals", "express.html"],
    ["Middleware Deep Dive", "middleware.html"],
    ["REST API Design", "rest-api.html"],
    ["Validation & Error Handling", "validation-errors.html"]] },
  { title: "4. Data & Auth", items: [
    ["Databases & ORMs", "databases.html"],
    ["Authentication: Sessions & JWT", "auth.html"],
    ["Security (OWASP for Node)", "security.html"],
    ["Caching & Redis", "caching.html"]] },
  { title: "5. Production Node", items: [
    ["Configuration & Secrets", "config.html"],
    ["Logging & Observability", "errors-logging.html"],
    ["Testing Node Services", "testing.html"],
    ["Performance & Profiling", "performance.html"],
    ["Scaling: Clusters & Workers", "scaling.html"],
    ["Deployment & Hardening", "production.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"],
    ["💻 Try It Yourself", "../../playground/index.html"]] }
]);
