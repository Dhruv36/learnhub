// ASP.NET Core track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Foundations", items: [
    ["How ASP.NET Core Runs", "index.html"],
    ["Minimal APIs", "minimal-apis.html"],
    ["Routing", "routing.html"],
    ["Model Binding & Validation", "model-binding.html"],
    ["Configuration & Options", "configuration.html"]] },
  { title: "2. The Pipeline", items: [
    ["Middleware Pipeline", "middleware.html"],
    ["Dependency Injection", "di-config.html"],
    ["Filters & Cross-Cutting Concerns", "filters.html"],
    ["Error Handling & Problem Details", "validation-errors.html"]] },
  { title: "3. Building APIs", items: [
    ["Controllers & MVC", "controllers-mvc.html"],
    ["REST API Design in ASP.NET", "api-design.html"],
    ["API Versioning", "versioning.html"],
    ["OpenAPI & Client Generation", "openapi.html"]] },
  { title: "4. Data", items: [
    ["EF Core: Modelling & Querying", "efcore-data.html"],
    ["EF Core: Change Tracking & Transactions", "efcore-advanced.html"],
    ["Caching & Output Caching", "caching.html"]] },
  { title: "5. Security & Realtime", items: [
    ["Authentication (Identity, JWT, OIDC)", "authn-authz.html"],
    ["Authorization Policies & Requirements", "authorization.html"],
    ["Securing ASP.NET Core Apps", "security.html"],
    ["SignalR (Realtime)", "signalr.html"]] },
  { title: "6. Production", items: [
    ["Background Services & Hosted Workers", "caching-background.html"],
    ["Testing ASP.NET Core", "testing.html"],
    ["Clean Architecture & CQRS", "clean-architecture.html"],
    ["Production Readiness & Observability", "production-readiness.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
