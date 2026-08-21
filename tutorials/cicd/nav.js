// CI/CD track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Foundations", items: [
    ["What CI/CD Actually Is", "index.html"],
    ["Branching, Merge Queues & Review Latency", "git-workflows.html"],
    ["Anatomy of a Pipeline", "first-pipeline.html"],
    ["Pipelines as Code: Reuse & Versioning", "pipeline-as-code.html"]] },
  { title: "2. Building & Testing", items: [
    ["Test Strategy in CI", "test-strategy.html"],
    ["Flaky Tests", "flaky-tests.html"],
    ["Quality Gates That Work", "quality-gates.html"],
    ["Builds, Artifacts & Versioning", "build-artifacts.html"]] },
  { title: "3. Pipeline Engineering", items: [
    ["Containers in CI", "containers-in-ci.html"],
    ["Pipeline Performance", "pipeline-performance.html"],
    ["Runners & Build Infrastructure", "runners-infrastructure.html"],
    ["Pipeline Reliability & Debugging", "pipeline-reliability.html"]] },
  { title: "4. Deployment", items: [
    ["Deployment Strategies", "deployment-strategies.html"],
    ["Environments & Promotion", "environments-promotion.html"],
    ["Database Migrations in CD", "database-migrations.html"],
    ["Progressive Delivery & Feature Flags", "progressive-delivery.html"]] },
  { title: "5. Security & Supply Chain", items: [
    ["Secrets & Pipeline Identity", "secrets-and-auth.html"],
    ["Supply-Chain Security", "supply-chain.html"],
    ["Dependency Management", "dependency-management.html"]] },
  { title: "6. Operating & Measuring", items: [
    ["DORA Metrics, Honestly", "dora-metrics.html"],
    ["Platform Engineering & Rollout", "platform-rollout.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
