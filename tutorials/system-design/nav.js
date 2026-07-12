// System Design curriculum — sections 1–3 mirror the local PDF library; section 4 = staff-level additions.
renderSidebar([
  { title: "1. Fundamentals", items: [
    ["How to Scale a System", "index.html"],
    ["Back-of-Envelope Estimation", "estimation.html"],
    ["CAP Theorem & Consistency Models", "cap-theorem.html"],
    ["Consistent Hashing", "consistent-hashing.html"],
    ["Caching Strategies", "caching.html"],
    ["Replication & Failover", "replication.html"],
    ["Bloom Filters, Merkle Trees, Inverted Index", "bloom-merkle.html"],
    ["Pub/Sub vs Message Queues", "pubsub-queues.html"],
    ["REST, API Contracts, Serverless", "rest-serverless.html"],
    ["Microservices Architecture", "microservices.html"],
    ["Heartbeat, Gossip, Retry with Back-off", "heartbeat-gossip.html"]] },
  { title: "2. Deep Dives", items: [
    ["Concurrency Control (ACID, Isolation)", "concurrency-control.html"],
    ["Authentication (JWT, OAuth2, OIDC)", "auth-deep-dive.html"],
    ["Security (TLS, Encryption-at-Rest)", "security-deep-dive.html"],
    ["Realtime Apps (WebSockets, Push)", "realtime-apps.html"],
    ["Concurrent Programming & Deadlocks", "concurrent-programming.html"],
    ["Observability Engineering", "observability.html"]] },
  { title: "3. Case Studies", items: [
    ["Design TinyURL", "design-tinyurl.html"],
    ["Design API Rate Limiter", "design-rate-limiter.html"],
    ["Design Unique ID Generator", "design-id-generator.html"],
    ["Design Key-Value Store (Dynamo)", "design-key-value-store.html"],
    ["Design Real-Time Chat", "design-chat.html"],
    ["Design Notification System", "#"],
    ["Design Geo-Spatial Apps / Uber", "#"],
    ["Design Amazon / E-Commerce", "#"],
    ["Design Recommendation System", "#"],
    ["Design Search Engine", "#"],
    ["Design Gmail", "#"],
    ["Design Instagram News Feed", "#"]] },
  { title: "4. Senior / Staff Level", items: [
    ["Trade-off Driven Design", "#"],
    ["Distributed Consensus (Raft, Quorums)", "#"],
    ["Data Platforms (CDC, Event Sourcing)", "#"],
    ["Multi-Region & Disaster Recovery", "#"],
    ["Cost, Capacity & SLO Engineering", "#"],
    ["Migration Strategies at Scale", "#"],
    ["Interview Framework", "#"]] },
  { title: "Practice", items: [["📝 System Design Quiz", "quiz.html"]] }
]);
