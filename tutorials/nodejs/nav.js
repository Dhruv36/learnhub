// Node.js track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Basics", items: [
    ["Runtime, Modules & npm", "index.html"],
    ["HTTP & Express Basics", "http-express.html"],
    ["Routing & Middleware", "middleware.html"],
    ["REST API Design & Validation", "rest-api.html"]] },
  { title: "2. Intermediate", items: [
    ["Auth: JWT & Sessions", "auth.html"],
    ["Databases & ORMs", "databases.html"],
    ["Error Handling & Logging", "errors-logging.html"]] },
  { title: "3. Advanced", items: [
    ["Event Loop & libuv Internals", "event-loop.html"],
    ["Streams & Backpressure", "streams.html"],
    ["Scaling: Clusters & Workers", "scaling.html"]] },
  { title: "4. Ultra-Advanced (Production)", items: [
    ["Testing APIs", "testing.html"],
    ["Production Hardening & Deployment", "production.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
