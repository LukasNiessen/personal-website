# Windows Codex task: use the teammate's existing Edge session

Implement and test native Windows browser support for the Reddit workflow on this Windows machine.

## Start from the latest remote revision

From the repository root, run `git status --short --branch`, verify that `origin` points to `LukasNiessen/personal-website`, and run `git fetch origin` before editing. Start a dedicated feature branch at the freshly fetched `origin/main`. In a clean checkout, use `git switch -c codex/windows-edge-browser origin/main`. If you also update a clean local `main`, use `git pull --ff-only origin main` while on `main`. If the checkout contains local work or local `main` has diverged, create a separate worktree from `origin/main` and work there. Preserve existing commits, edits, and untracked files. Verify your branch starts at the fetched revision and reread this task there.

## Context and implementation

Start with the root `AGENTS.md`, then read `marketing/reddit/AGENTS.md`, `browser.md`, and `README.md` in the Reddit directory. Inspect `marketing/reddit/scripts/browser.py`, `request_guard.py`, and their tests. The repository already handles writing, community rules, request pacing, weekly posting caps, and campaign reports.

On macOS, the browser helper sends JavaScript to the user's Microsoft Edge session through Apple Events. It opens a task-owned tab with the user's existing login, checks its URL before acting, and leaves requested drafts open for human review. Mirror that experience on Windows.

1. Keep `browser.py` as the entry point. Select the transport once based on the OS. Preserve the existing Mac commands and behavior. A small Windows adapter is sufficient.
2. Use Microsoft Edge Stable with Microsoft's published Playwright Extension. Prefer the official local CLI in extension mode (`playwright-cli attach --extension=msedge`). MCP is acceptable if simpler. Pick one integration. Connect to the teammate's already-open Edge profile. Allow them to approve the connection and choose a tab or group. Report an attachment failure instead of launching a fresh profile.
3. Support the current operations for probing browser control, opening and inspecting an owned tab, evaluating an action against an expected page, and explicitly closing an owned tab. For review handoff, detach and leave the populated tabs open. Tab indexes can shift, and two composers can have identical URLs. Verify the target's identity before acting and stop if it is ambiguous.
4. Port the existing guard's state path and interprocess lock. It currently uses `/private/tmp`, `os.getuid()`, and `fcntl`. On Windows, all worktrees for one user must share a ledger. Preserve the existing JSON format, pacing, weekly cap, pending reservations, rate-limit handling, and Mac state path.
5. Update the Reddit onboarding and browser guides with the exact Windows setup, permissions, commands, and successful probe output you verified. Keep the existing campaign workflow and use the published extension.

## Test on the actual Windows machine

Use a local test page for browser QA. Do not run a promotional campaign, submit a Reddit post or comment, or click Reddit's Post button.

- Run the existing suite from the repository root with `py -3 -X utf8 -m unittest discover -s marketing/reddit/scripts -p "test_*.py"`, or the equivalent command for the installed Python. Add focused Windows tests, including two independent processes competing for one remaining reservation. Use isolated test state.
- Run a real probe in the user's open Edge session with the installed extension. Fill an input, trigger an event, click a harmless local button, and read the result back. Check that a separate, unrelated tab stays untouched.
- Open two test tabs at the same URL. Close or reorder one. Verify that the helper locates the intended surviving tab or reports that its target was lost.
- Fill a title, multiline body, and flair-like control on the local page. Attach a small local video, verify its preview, then disconnect. Confirm the correct tab still contains the text, selection, and video. If extension file access is blocked by machine policy, verify a manual-attachment handoff and report that limitation.
- Diagnose failures, make the smallest appropriate fix, and rerun the failed check and relevant regression tests. Continue until the supported workflow works. If a human must install the extension or approve a prompt, ask for the specific action and resume testing afterward.

Finish with a short report covering changes, verified setup commands, results observed in real Edge, and anything still blocked or tested only with mocks.

References: [Playwright attach and detach](https://playwright.dev/agent-cli/commands/attach), [Microsoft's extension guide](https://github.com/microsoft/playwright/blob/main/packages/extension/README.md), and the [Windows extension file-upload report](https://github.com/microsoft/playwright-mcp/issues/1481).
