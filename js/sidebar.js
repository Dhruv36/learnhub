// Shared sidebar: each track defines its curriculum once (nav.js) and every lesson page renders it.
// Highlights the link matching the current page automatically.
function renderSidebar(sections) {
  const el = document.getElementById("sidebar");
  const here = location.pathname.split("/").pop() || "index.html";
  el.innerHTML = sections.map(s =>
    `<h4>${s.title}</h4>` +
    s.items.map(it => {
      const [label, href] = it;
      const active = href === here ? ' class="active"' : (href === "#" ? ' class="soon"' : "");
      return `<a href="${href}"${active}>${label}</a>`;
    }).join("")
  ).join("");
}
