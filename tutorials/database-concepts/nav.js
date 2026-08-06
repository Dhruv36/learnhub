// Database Concepts & Architecture curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Storage Foundations", items: [
    ["How a Database Stores Data", "index.html"],
    ["Pages, Heap Files & Row Layout", "pages-heap-files.html"],
    ["B+Trees In Depth", "btrees.html"],
    ["LSM-Trees & Write-Optimised Storage", "lsm-trees.html"],
    ["Buffer Pool & Page Cache", "buffer-pool.html"]] },
  { title: "2. Durability & Concurrency", items: [
    ["WAL, Checkpoints & Crash Recovery", "wal-recovery.html"],
    ["MVCC & Snapshot Isolation", "mvcc.html"],
    ["Locking, Latches & Deadlocks", "locking-latches.html"]] },
  { title: "3. Query Processing", items: [
    ["Parser, Rewriter & Planner", "query-planner.html"],
    ["Cost Models & Statistics", "cost-models.html"],
    ["Join & Aggregation Algorithms", "join-algorithms.html"]] },
  { title: "4. Design Perspective", items: [
    ["Physical Schema Design for the Engine", "physical-design.html"],
    ["OLTP vs OLAP & Row vs Columnar", "oltp-olap.html"],
    ["The Engine Landscape", "engine-landscape.html"],
    ["Choosing a Database", "choosing-a-database.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
