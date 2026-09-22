---
"@opencoredev/social-sdk": patch
---

Run the CLI when invoked through the installed bin symlink. The entry guard now resolves the invoked path before comparing it to the module URL, so `social-sdk` from node_modules/.bin executes instead of exiting silently.
