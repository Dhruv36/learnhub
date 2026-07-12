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
    ["Concurrency Control (ACID, Isolation)", "#"],
    ["Authentication (JWT, OAuth2, OIDC)", "#"],
    ["Security (TLS, Encryption-at-Rest)", "#"],
    ["Realtime Apps (WebSockets, Push)", "#"],
    ["Concurrent Programming & Deadlocks", "#"],
    ["Observability Engineering", "#"]] },
  { title: "3. Case Studies", items: [
    ["Design TinyURL", "#"],
    ["Design API Rate Limiter", "#"],
    ["Design Unique ID Generator", "#"],
    ["Design Key-Value Store (Dynamo)", "#"],
    ["Design Real-Time Chat", "#"],
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
