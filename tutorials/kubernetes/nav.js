// Kubernetes track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Basics", items: [
    ["Architecture: Control Plane & Nodes", "index.html"],
    ["Pods, ReplicaSets & Deployments", "pods-deployments.html"],
    ["Services & Ingress", "services-ingress.html"],
    ["ConfigMaps & Secrets", "config-secrets.html"]] },
  { title: "2. Intermediate", items: [
    ["Probes, Resources & Limits", "probes-resources.html"],
    ["Autoscaling (HPA)", "autoscaling.html"],
    ["StatefulSets & Storage", "statefulsets-storage.html"],
    ["Helm", "helm.html"]] },
  { title: "3. Advanced", items: [
    ["RBAC & Network Policies", "rbac-network.html"],
    ["Scheduling: Affinity & Taints", "scheduling.html"]] },
  { title: "4. Ultra-Advanced (Production)", items: [
    ["GitOps (ArgoCD/Flux)", "gitops.html"],
    ["Debugging Production Incidents", "debugging-production.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
