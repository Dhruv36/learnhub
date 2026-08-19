// Docker track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Foundations", items: [
    ["What a Container Actually Is", "index.html"],
    ["Images, Layers & the Union Filesystem", "images-containers.html"],
    ["Namespaces: Isolating What You See", "namespaces.html"],
    ["cgroups: Limiting What You Use", "cgroups.html"],
    ["The Runtime Stack: runc, containerd, Docker", "runtime-stack.html"]] },
  { title: "2. Building Images", items: [
    ["Writing a Dockerfile", "dockerfile.html"],
    ["The Build Cache & Layer Ordering", "build-cache.html"],
    ["Multi-stage Builds", "multi-stage.html"],
    ["BuildKit & Modern Build Features", "buildkit.html"],
    ["Image Size & Base Image Choice", "optimization.html"]] },
  { title: "3. Running Containers", items: [
    ["Process Model, PID 1 & Signals", "process-model.html"],
    ["Storage: Volumes, Binds & tmpfs", "volumes.html"],
    ["Networking & Port Publishing", "networking.html"],
    ["Environment, Config & Secrets", "env-secrets.html"]] },
  { title: "4. Composing Systems", items: [
    ["Docker Compose", "compose.html"],
    ["Health Checks & Startup Order", "healthchecks.html"]] },
  { title: "5. Production Concerns", items: [
    ["Security & Non-root Containers", "security.html"],
    ["Resource Limits & the OOM Killer", "resource-limits.html"],
    ["Logging & Observability", "logging.html"],
    ["Debugging Containers", "debugging.html"]] },
  { title: "6. Supply Chain", items: [
    ["Registry, Tagging & Supply Chain", "registry-supply-chain.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
