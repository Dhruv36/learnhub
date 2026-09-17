// TypeScript track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Foundations", items: [
    ["What TypeScript Actually Is", "index.html"],
    ["Types, Unions & Literals", "types-basics.html"],
    ["Structural Typing & Assignability", "structural-typing.html"],
    ["Functions, Overloads & Signatures", "functions.html"]] },
  { title: "2. Type-Level Programming", items: [
    ["Narrowing, Guards & Unions", "narrowing.html"],
    ["Generics & Constraints", "generics.html"],
    ["Conditional Types & infer", "conditional-types.html"],
    ["Mapped & Template Literal Types", "mapped-template-types.html"],
    ["Utility Types and Where They Lie", "utility-types.html"]] },
  { title: "3. Correctness at the Boundary", items: [
    ["strict and the Flags That Matter", "strictness.html"],
    ["Types Stop at the Boundary", "runtime-validation.html"],
    ["Errors, unknown & Result Types", "errors.html"],
    ["Branded & Nominal Types", "branded-types.html"]] },
  { title: "4. Modules, Config & Build", items: [
    ["tsconfig Deep Dive", "tsconfig.html"],
    ["Modules, ESM/CJS & Resolution", "modules.html"],
    ["Declaration Files & Ambient Types", "declaration-files.html"],
    ["Building, Type-Checking & CI", "build-pipeline.html"]] },
  { title: "5. TypeScript in Practice", items: [
    ["Classes, Access & Decorators", "classes.html"],
    ["Async, Promises & Concurrency", "async-types.html"]] },
  { title: "6. Scale & Migration", items: [
    ["Compiler Performance at Scale", "compiler-performance.html"],
    ["Migrating JavaScript to TypeScript", "migration.html"],
    ["Patterns & Anti-Patterns", "patterns.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
