// MongoDB track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Basics", items: [
    ["Documents & Collections", "index.html"],
    ["CRUD Operations", "crud.html"],
    ["Query Operators & Projection", "queries.html"]] },
  { title: "2. Intermediate", items: [
    ["Schema Design: Embed vs Reference", "schema-design.html"],
    ["Aggregation Pipeline", "aggregation.html"],
    ["Indexes", "indexes.html"]] },
  { title: "3. Advanced", items: [
    ["Transactions & Consistency", "transactions.html"],
    ["Replica Sets & Read Preferences", "replication.html"],
    ["Change Streams", "change-streams.html"]] },
  { title: "4. Ultra-Advanced (Production)", items: [
    ["Sharding & Shard Keys", "sharding.html"],
    ["Performance Tuning", "performance.html"],
    ["Anti-Patterns at Scale", "anti-patterns.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
