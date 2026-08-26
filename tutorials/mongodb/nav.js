// MongoDB track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Foundations", items: [
    ["What MongoDB Actually Is", "index.html"],
    ["Documents, BSON & _id", "documents-bson.html"],
    ["CRUD and What It Guarantees", "crud-semantics.html"],
    ["Queries, Operators & Arrays", "queries-operators.html"]] },
  { title: "2. Schema Design", items: [
    ["Embed vs Reference", "schema-design.html"],
    ["Schema Design Patterns", "patterns.html"],
    ["Relationships & $lookup", "relationships.html"],
    ["Schema Validation & Evolution", "schema-validation.html"]] },
  { title: "3. Indexes & Query Performance", items: [
    ["How Indexes Work", "indexes.html"],
    ["Index Types & Their Traps", "index-types.html"],
    ["Reading Explain Plans", "explain-plans.html"],
    ["Query Tuning in Production", "query-tuning.html"]] },
  { title: "4. Aggregation", items: [
    ["The Aggregation Pipeline", "aggregation.html"],
    ["Advanced Stages", "aggregation-advanced.html"],
    ["Aggregation Performance", "aggregation-performance.html"]] },
  { title: "5. Distribution & Durability", items: [
    ["Replica Sets & Read Concerns", "replication.html"],
    ["Transactions", "transactions.html"],
    ["Sharding & Shard Keys", "sharding.html"],
    ["Durability, Backup & Recovery", "durability-backup.html"]] },
  { title: "6. Production", items: [
    ["Operating MongoDB", "operations.html"],
    ["Security & Encryption", "security-ops.html"],
    ["Anti-Patterns at Scale", "anti-patterns.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
