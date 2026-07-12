// .NET (C#) track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Basics", items: [
    ["C# Syntax, Types & Control Flow", "index.html"],
    ["OOP: Classes, Interfaces, Records", "oop.html"],
    ["Collections & Generics", "collections-generics.html"],
    ["Exceptions & Nullability", "exceptions-nullability.html"]] },
  { title: "2. Intermediate", items: [
    ["LINQ Deep Dive", "linq.html"],
    ["Delegates, Events & Lambdas", "delegates-events.html"],
    ["async/await & Tasks", "async-await.html"],
    ["Testing (xUnit)", "testing.html"]] },
  { title: "3. Advanced", items: [
    ["Memory: Span<T>, GC, IDisposable", "memory.html"],
    ["Dependency Injection & Hosting", "di-hosting.html"]] },
  { title: "4. Ultra-Advanced (Production)", items: [
    ["EF Core in Production", "efcore.html"],
    ["Performance, NativeAOT & Trimming", "performance-aot.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
