// Redis track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Basics", items: [
    ["Introduction & Data Model", "index.html"],
    ["Strings, Keys & TTL", "strings-keys.html"],
    ["Hashes, Lists, Sets & Sorted Sets", "data-structures.html"]] },
  { title: "2. Intermediate", items: [
    ["Caching Patterns", "caching.html"],
    ["Pub/Sub & Streams", "pubsub-streams.html"],
    ["Persistence: RDB & AOF", "persistence.html"]] },
  { title: "3. Advanced", items: [
    ["Replication & Sentinel", "replication.html"],
    ["Distributed Locks", "locks.html"],
    ["Redis Cluster", "cluster.html"]] },
  { title: "4. Ultra-Advanced (Production)", items: [
    ["Production Use Cases", "use-cases.html"],
    ["Memory Optimization & Eviction", "memory.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
