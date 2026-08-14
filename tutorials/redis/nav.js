// Redis track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Foundations", items: [
    ["What Redis Actually Is", "index.html"],
    ["Strings, Keys & Expiry", "strings-keys.html"],
    ["Hashes, Lists & Sets", "data-structures.html"],
    ["Sorted Sets & Ranking", "sorted-sets.html"],
    ["The Single-Threaded Model", "single-threaded.html"]] },
  { title: "2. Working With Redis", items: [
    ["Commands, Pipelining & Round Trips", "pipelining.html"],
    ["Transactions & Lua Scripting", "transactions.html"],
    ["Caching Patterns", "caching.html"],
    ["Cache Invalidation & Stampedes", "cache-invalidation.html"]] },
  { title: "3. Messaging & Data Flow", items: [
    ["Pub/Sub", "pubsub.html"],
    ["Streams & Consumer Groups", "streams.html"],
    ["Rate Limiting", "rate-limiting.html"]] },
  { title: "4. Durability & Distribution", items: [
    ["Persistence: RDB & AOF", "persistence.html"],
    ["Replication & Failover", "replication.html"],
    ["Redis Cluster", "cluster.html"],
    ["Distributed Locks", "locks.html"]] },
  { title: "5. Production", items: [
    ["Memory & Eviction", "memory.html"],
    ["Performance & Latency", "performance.html"],
    ["Observability & Debugging", "observability.html"],
    ["Security & Operations", "security-ops.html"],
    ["Production Use Cases", "use-cases.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
