// Docker track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Basics", items: [
    ["Introduction: Containers vs VMs", "index.html"],
    ["Images & Containers", "images-containers.html"],
    ["Writing a Dockerfile", "dockerfile.html"],
    ["Volumes & Networking", "volumes-networking.html"]] },
  { title: "2. Intermediate", items: [
    ["Docker Compose", "compose.html"],
    ["Multi-stage Builds", "multi-stage.html"],
    ["Environment & Secrets", "env-secrets.html"],
    ["Debugging Containers", "debugging.html"]] },
  { title: "3. Advanced", items: [
    ["Image Optimization", "optimization.html"],
    ["Security & Non-root", "security.html"],
    ["Runtime Internals: Namespaces & cgroups", "internals.html"]] },
  { title: "4. Ultra-Advanced (Production)", items: [
    ["Registry & Supply Chain", "registry-supply-chain.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
