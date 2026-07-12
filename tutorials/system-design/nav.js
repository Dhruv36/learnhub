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
    ["Design Notification System", "design-notifications.html"],
    ["Design Geo-Spatial Apps / Uber", "design-geospatial-uber.html"],
    ["Design Amazon / E-Commerce", "design-amazon.html"],
    ["Design Recommendation System", "design-recommendation.html"],
    ["Design Search Engine", "design-search-engine.html"],
    ["Design Gmail", "design-gmail.html"],
    ["Design Instagram News Feed", "design-instagram-feed.html"]] },
  { title: "4. Senior / Staff Level", items: [
    ["Trade-off Driven Design", "tradeoff-driven-design.html"],
    ["Distributed Consensus (Raft, Quorums)", "distributed-consensus.html"],
    ["Data Platforms (CDC, Event Sourcing)", "data-platforms.html"],
    ["Multi-Region & Disaster Recovery", "multi-region-dr.html"],
    ["Cost, Capacity & SLO Engineering", "cost-capacity-slo.html"],
    ["Migration Strategies at Scale", "migration-strategies.html"],
    ["Interview Framework", "interview-framework.html"]] },
  { title: "Practice", items: [["📝 System Design Quiz", "quiz.html"]] }
]);
