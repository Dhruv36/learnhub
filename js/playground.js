// Runs the editor code inside a sandboxed iframe (scripts allowed, no same-origin access).
function run() {
  document.getElementById("output").srcdoc = document.getElementById("code").value;
}
document.getElementById("runBtn").addEventListener("click", run);
run(); // show initial example on load
