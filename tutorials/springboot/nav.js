// Spring Boot track curriculum — single source of truth for every page's sidebar.
// Deep, interview-mastery curriculum (HTML-track depth). Ordered Basics → Ultra-Advanced.
renderSidebar([
  { title: "1. Core Container", items: [
    ["IoC, DI & Beans", "index.html"],
    ["Bean Scopes & Lifecycle", "bean-lifecycle.html"],
    ["Configuration & @Bean", "configuration.html"],
    ["Auto-Configuration & Starters", "autoconfig.html"],
    ["Spring vs Spring Boot", "spring-vs-boot.html"]] },
  { title: "2. Web Layer", items: [
    ["REST Controllers", "rest.html"],
    ["Request Mapping & Binding", "request-mapping.html"],
    ["Validation", "validation.html"],
    ["Error Handling", "error-handling.html"],
    ["Configuration & Profiles", "config.html"]] },
  { title: "3. Data Layer", items: [
    ["Spring Data JPA", "data-jpa.html"],
    ["JPA Relationships & N+1", "jpa-relationships.html"],
    ["Transactions", "transactions.html"]] },
  { title: "4. Cross-Cutting", items: [
    ["AOP & Proxies", "aop.html"],
    ["Spring Security", "security.html"],
    ["Caching, Async & Scheduling", "caching-async.html"]] },
  { title: "5. Production", items: [
    ["Testing Spring Boot", "testing.html"],
    ["Actuator & Observability", "actuator.html"],
    ["Resilience & Microservices", "microservices.html"],
    ["Production & Deployment", "production.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
