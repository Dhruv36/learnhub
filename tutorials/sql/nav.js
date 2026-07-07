// SQL track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Basics", items: [
    ["SELECT & Filtering", "index.html"],
    ["Sorting, Limiting & Aggregates", "aggregates.html"],
    ["JOINs", "joins.html"],
    ["INSERT, UPDATE, DELETE", "dml.html"]] },
  { title: "2. Intermediate", items: [
    ["Subqueries & CTEs", "subqueries-ctes.html"],
    ["Window Functions", "window-functions.html"],
    ["Schema Design & Normalization", "schema-design.html"],
    ["Constraints & Transactions", "transactions.html"]] },
  { title: "3. Advanced", items: [
    ["Indexes & Query Plans", "indexes.html"],
    ["Isolation Levels & Locking", "isolation.html"],
    ["Query Optimization", "optimization.html"]] },
  { title: "4. Ultra-Advanced (Production)", items: [
    ["Scaling: Replication, Partitioning, Sharding", "scaling.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
