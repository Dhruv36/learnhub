// HTML track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Basics", items: [
    ["Introduction", "index.html"],
    ["Document Structure", "document-structure.html"],
    ["Text & Headings", "text-headings.html"],
    ["Links & Images", "links-images.html"],
    ["Lists & Tables", "lists-tables.html"]] },
  { title: "2. Intermediate", items: [
    ["Forms & Validation", "forms.html"],
    ["Semantic HTML", "semantic-html.html"],
    ["Media (audio/video)", "media.html"]] },
  { title: "3. Advanced", items: [
    ["Accessibility (ARIA)", "accessibility.html"],
    ["SEO & Meta Tags", "seo.html"],
    ["Performance (lazy loading, preload)", "performance.html"]] },
  { title: "4. Ultra-Advanced (Production)", items: [
    ["Web Components & Shadow DOM", "web-components.html"],
    ["Security (XSS, CSP, sanitization)", "security.html"],
    ["Production Patterns (SSR, hydration)", "production-patterns.html"]] },
  { title: "Practice", items: [
    ["📝 HTML Quiz", "quiz.html"],
    ["💻 Try It Yourself", "../../playground/index.html"]] }
]);
