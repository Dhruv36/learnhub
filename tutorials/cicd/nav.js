// CI/CD track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Basics", items: [
    ["Git Workflows (trunk vs GitFlow)", "index.html"],
    ["What CI Actually Does", "what-is-ci.html"],
    ["GitHub Actions: First Pipeline", "github-actions.html"]] },
  { title: "2. Intermediate", items: [
    ["Testing Stages & Quality Gates", "testing-gates.html"],
    ["Artifacts & Versioning", "artifacts-versioning.html"],
    ["Secrets & OIDC Auth", "secrets-oidc.html"],
    ["Docker in CI", "docker-in-ci.html"]] },
  { title: "3. Advanced", items: [
    ["Deployment Strategies (blue/green, canary)", "deployment-strategies.html"],
    ["Feature Flags & Progressive Delivery", "feature-flags.html"],
    ["Pipeline Performance (caching, parallelism)", "pipeline-performance.html"]] },
  { title: "4. Ultra-Advanced (Production)", items: [
    ["Supply-chain Security (SLSA, signing)", "supply-chain.html"],
    ["DORA Metrics & Platform Engineering", "dora-metrics.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
