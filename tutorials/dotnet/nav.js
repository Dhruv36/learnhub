// .NET (C#) track curriculum — single source of truth for every page's sidebar.
// v4 mastery curriculum. Modern C#/.NET: current LTS, nullable-aware, span-conscious.
renderSidebar([
  { title: "1. Foundations", items: [
    ["C# & .NET: How It Runs", "index.html"],
    ["Types & Variables: Value vs Reference", "types.html"],
    ["Control Flow & Operators", "control-flow.html"],
    ["Strings & Text", "strings.html"],
    ["Methods, Parameters & Overloading", "methods.html"]] },
  { title: "2. Object-Oriented C#", items: [
    ["Classes & Encapsulation", "oop.html"],
    ["Inheritance, Polymorphism & Interfaces", "inheritance.html"],
    ["Records, Structs & Equality", "records-structs.html"],
    ["Generics Deep Dive", "generics.html"],
    ["Pattern Matching & Switch Expressions", "pattern-matching.html"]] },
  { title: "3. Core Libraries", items: [
    ["Collections & Their Internals", "collections-generics.html"],
    ["LINQ Deep Dive", "linq.html"],
    ["Delegates, Events & Lambdas", "delegates-events.html"],
    ["Exceptions & Nullable Reference Types", "exceptions-nullability.html"]] },
  { title: "4. Async & Concurrency", items: [
    ["async/await & Tasks", "async-await.html"],
    ["Async Patterns & Pitfalls", "async-patterns.html"],
    ["Threads, Parallelism & Synchronization", "threading.html"]] },
  { title: "5. Runtime & Performance", items: [
    ["Memory & GC: Span, IDisposable", "memory.html"],
    ["Performance, Benchmarking & NativeAOT", "performance-aot.html"]] },
  { title: "6. Professional .NET", items: [
    ["Dependency Injection & the Generic Host", "di-hosting.html"],
    ["EF Core in Production", "efcore.html"],
    ["Testing with xUnit", "testing.html"],
    ["Modern C# & Project Idioms", "modern-csharp.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
