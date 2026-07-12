// ASP.NET Core track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Basics", items: [
    ["Minimal APIs: First Endpoint", "index.html"],
    ["Routing & Model Binding", "routing-binding.html"],
    ["Dependency Injection & Configuration", "di-config.html"]] },
  { title: "2. Intermediate", items: [
    ["Controllers & MVC", "controllers-mvc.html"],
    ["EF Core: Data Access", "efcore-data.html"],
    ["Validation & Error Handling", "validation-errors.html"],
    ["Middleware Pipeline", "middleware.html"]] },
  { title: "3. Advanced", items: [
    ["AuthN/AuthZ (Identity, JWT, OIDC)", "authn-authz.html"],
    ["Caching & Background Services", "caching-background.html"],
    ["SignalR (Realtime)", "signalr.html"]] },
  { title: "4. Ultra-Advanced (Production)", items: [
    ["Clean Architecture, CQRS & API Versioning", "clean-architecture.html"],
    ["Production Readiness: Health Checks, OpenTelemetry & Deployment", "production-readiness.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
