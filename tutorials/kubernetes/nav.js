// Kubernetes track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Foundations", items: [
    ["Architecture & the Reconciliation Loop", "index.html"],
    ["Objects, the API & How Apply Works", "objects-yaml.html"],
    ["Pods: The Unit of Scheduling", "pods.html"],
    ["Deployments, ReplicaSets & Rollouts", "deployments.html"],
    ["The Scheduler: Affinity, Taints & Spread", "scheduling.html"]] },
  { title: "2. Networking & Traffic", items: [
    ["Services, Endpoints & kube-proxy", "services.html"],
    ["Cluster DNS & Service Discovery", "dns-discovery.html"],
    ["Ingress, Gateway API & Load Balancers", "ingress-gateway.html"],
    ["Network Policies", "network-policy.html"]] },
  { title: "3. Configuration & State", items: [
    ["ConfigMaps & Secrets", "config-secrets.html"],
    ["Volumes, PVs, PVCs & StorageClasses", "storage.html"],
    ["StatefulSets & Stable Identity", "statefulsets.html"],
    ["Jobs, CronJobs & One-shot Work", "jobs-cronjobs.html"]] },
  { title: "4. Scaling & Reliability", items: [
    ["Probes: Liveness, Readiness & Startup", "probes.html"],
    ["Requests, Limits & QoS", "resources.html"],
    ["Autoscaling: HPA, VPA & Cluster Autoscaler", "autoscaling.html"],
    ["Disruptions, Draining & Zero-Downtime", "disruptions.html"]] },
  { title: "5. Security & Multi-tenancy", items: [
    ["RBAC & ServiceAccounts", "rbac.html"],
    ["Pod Security & Admission Control", "pod-security.html"]] },
  { title: "6. Operating Clusters", items: [
    ["Helm & Templating", "helm.html"],
    ["GitOps with Argo CD & Flux", "gitops.html"],
    ["Debugging Production Clusters", "debugging-production.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
