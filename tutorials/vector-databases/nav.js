// Vector Databases & RAG curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Foundations", items: [
    ["What a Vector Database Is For", "index.html"],
    ["Embeddings & Vector Space", "embeddings.html"],
    ["Similarity Metrics & Normalisation", "similarity-metrics.html"],
    ["The Curse of Dimensionality", "dimensionality.html"]] },
  { title: "2. Indexing & Search", items: [
    ["Exact kNN vs Approximate Search", "knn-vs-ann.html"],
    ["HNSW Deep Dive", "hnsw.html"],
    ["IVF, PQ & Quantisation", "ivf-pq.html"],
    ["Tuning Recall vs Latency", "tuning-recall.html"]] },
  { title: "3. The Landscape", items: [
    ["pgvector & SQL-Native Vectors", "pgvector.html"],
    ["Dedicated Vector Stores", "dedicated-stores.html"],
    ["Metadata Filtering & Hybrid Search", "hybrid-search.html"]] },
  { title: "4. RAG in Production", items: [
    ["Chunking & Ingestion", "chunking.html"],
    ["Retrieval Pipelines & Reranking", "retrieval-reranking.html"],
    ["Evaluating Retrieval", "evaluation.html"],
    ["Scaling, Cost & Operations", "scaling-ops.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
