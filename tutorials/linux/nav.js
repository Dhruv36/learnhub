// Unix & Linux curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Foundations", items: [
    ["How Unix Is Put Together", "index.html"],
    ["The Filesystem & Paths", "filesystem.html"],
    ["Files, Inodes & Links", "inodes-links.html"],
    ["Users, Groups & Permissions", "permissions.html"]] },
  { title: "2. The Shell", items: [
    ["The Shell Executes a Line", "shell.html"],
    ["Redirection, Pipes & File Descriptors", "redirection-pipes.html"],
    ["Text Processing: grep, sed & awk", "text-processing.html"],
    ["Finding Files: find & xargs", "find-xargs.html"]] },
  { title: "3. Processes & The Kernel", items: [
    ["Processes, fork & exec", "processes.html"],
    ["Signals & Job Control", "signals-jobs.html"],
    ["System Calls & strace", "syscalls.html"],
    ["Memory: Virtual Memory & the OOM Killer", "memory.html"]] },
  { title: "4. The Running System", items: [
    ["Storage, Filesystems & Mounts", "storage-filesystems.html"],
    ["Networking From the Socket Up", "networking.html"],
    ["systemd & Service Management", "systemd.html"],
    ["Logs, Journals & Time", "logging.html"]] },
  { title: "5. Production Skills", items: [
    ["Shell Scripting That Survives", "shell-scripting.html"],
    ["Performance Debugging & the USE Method", "performance.html"],
    ["Namespaces, cgroups & Containers", "namespaces-cgroups.html"],
    ["Hardening & The Production Checklist", "hardening.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
