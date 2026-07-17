// Spring Boot track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Basics", items: [
    ["IoC, DI & Beans", "index.html"],
    ["Auto-Config & Starters", "autoconfig.html"],
    ["REST Controllers", "rest.html"],
    ["Configuration & Profiles", "config.html"]] },
  { title: "2. Intermediate", items: [
    ["Spring Data JPA", "data-jpa.html"],
    ["Validation & Error Handling", "validation.html"],
    ["Testing Spring Boot", "testing.html"]] },
  { title: "3. Advanced", items: [
    ["Spring Security", "security.html"],
    ["Actuator & Observability", "actuator.html"],
    ["Caching, Async & Scheduling", "caching-async.html"]] },
  { title: "4. Ultra-Advanced (Production)", items: [
    ["Production & Deployment", "production.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
