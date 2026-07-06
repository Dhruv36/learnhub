// Python track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Basics", items: [
    ["Syntax, Types & Variables", "index.html"],
    ["Control Flow & Functions", "control-flow.html"],
    ["Data Structures", "data-structures.html"],
    ["Strings, Files & I/O", "strings-io.html"]] },
  { title: "2. Intermediate", items: [
    ["OOP & Dataclasses", "oop.html"],
    ["Comprehensions, Iterators & Generators", "comprehensions-generators.html"],
    ["Decorators & Context Managers", "decorators-context.html"],
    ["Modules, Packaging & Environments", "modules-packaging.html"]] },
  { title: "3. Advanced", items: [
    ["Type Hints & Typing", "typing.html"],
    ["Concurrency: GIL, Threads, Async", "concurrency.html"],
    ["Testing with pytest", "testing.html"]] },
  { title: "4. Ultra-Advanced (Production)", items: [
    ["FastAPI & Production APIs", "fastapi.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
