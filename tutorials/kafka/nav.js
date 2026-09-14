// Apache Kafka track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Foundations", items: [
    ["What Kafka Actually Is", "index.html"],
    ["Topics, Partitions & the Log", "log-partitions.html"],
    ["Producers: Batching, Keys & Partitioners", "producers.html"],
    ["Consumers & Consumer Groups", "consumers.html"]] },
  { title: "2. Delivery & Durability", items: [
    ["Replication, ISR & acks", "replication.html"],
    ["Offsets & Commit Strategies", "offsets.html"],
    ["Idempotence & Transactions", "exactly-once.html"],
    ["Rebalancing & Group Membership", "rebalancing.html"]] },
  { title: "3. Data Design", items: [
    ["Serialization & Schema Evolution", "schemas.html"],
    ["Event Design: Keys, Ordering & Payloads", "event-design.html"],
    ["Retention & Log Compaction", "retention-compaction.html"]] },
  { title: "4. Processing & Integration", items: [
    ["Kafka Streams: KStream, KTable & State", "kafka-streams.html"],
    ["Time, Windows & Joins", "windowing-joins.html"],
    ["Kafka Connect & CDC", "connect-cdc.html"],
    ["Errors, Retries & Dead Letter Topics", "error-handling.html"]] },
  { title: "5. Operations", items: [
    ["Cluster Architecture & KRaft", "kraft-cluster.html"],
    ["Partition Count & Capacity Planning", "capacity.html"],
    ["Performance: Throughput vs Latency", "performance.html"],
    ["Monitoring & Debugging", "monitoring.html"],
    ["Security: TLS, SASL, ACLs & Quotas", "security.html"]] },
  { title: "6. Architecture", items: [
    ["Multi-Region & Disaster Recovery", "multi-region.html"],
    ["Kafka vs the Alternatives", "choosing-kafka.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
