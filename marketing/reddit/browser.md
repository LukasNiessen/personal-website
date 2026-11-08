# Browser: Microsoft Edge

Use **Microsoft Edge** on this Mac for Reddit posting through JavaScript from Apple Events. Its stable window and tab IDs let an agent keep working in its own window without relying on whichever tab the user has selected.

Verified on November 8, 2026: Edge's **View → Developer → Allow JavaScript from Apple Events** is enabled. The blank-page probe changed an input, dispatched an `input` event, clicked a local button, and returned the expected values. After the restart described below, the running Edge **157.0.4341.42** also loaded Reddit's homepage, returned its real rendered DOM through this helper, and passed a reload test. No post was submitted. Safari 27.0.1 exposed `do JavaScript`, but its window-creation calls timed out, so it is not the selected browser.

The earlier crashed/`about:blank` problem was resolved by completing a pending Edge update. Process inspection found a browser running for over four days with **156.0.4314.58** helpers, while the app bundle contained only **157.0.4341.42** and the old framework directory was gone. A built-in `edge://restart` followed by reopening the installed app switched all observed helpers to 157. Reddit then rendered normally and reloaded successfully. The 18-tab session was retained, with some work sites redirecting to sign-in; the working Reddit window was left open and the empty restart placeholder closed. Private diagnostic tab snapshots were deleted. This corrects the initial tentative explanation about new-window navigation timing.

The helper's URL guard and execution marker also passed independent checks. The first authorized live campaign on November 8, 2026 verified account identity, text-post composition, flair selection, top-level comments, submission, and rendered code through Edge using Reddit's classic UI. The user selected **u/127001-sweet-127001** for that campaign, overriding the historical corpus account. Four posts and one showcase-thread comment were submitted; FastAPI awaited moderator approval. See the [campaign report](runs/2026-11-08-archunitpython-gift.md). Inspect the current DOM and account again for future campaigns.

## Setup and troubleshooting

- Log in to the intended Reddit account in Edge's normal profile. Confirm the username before posting.
- Keep **View → Developer → Allow JavaScript from Apple Events** checked. Check its state before changing it; never blindly toggle it.
- If macOS requests Automation access, allow the actual calling app (Codex or Terminal) to control Microsoft Edge under **System Settings → Privacy & Security → Automation**. The JavaScript menu option and macOS Automation permission are separate.
- In the Codex filesystem sandbox, `osascript` returned a connection error. GUI Apple Events worked with the normal sandbox escalation. Use that mechanism if necessary; do not interpret a sandbox error as a missing browser.
- If new tabs crash after an update, compare the running helper framework versions with the installed app before changing profile data. A stale running version can need a normal restart. Microsoft documents that [restarting applies a downloaded update](https://support.microsoft.com/en-us/edge/microsoft-edge-update-settings). Use the browser's normal session-restoring restart, respect any unsaved-work prompt, and verify the new process version and restored tabs.
- On a timeout, inspect the dedicated tab and current post state before retrying. A timed-out click may already have succeeded. Do not resubmit blindly.

Safari is a fallback only after another successful probe. Its documented setting is **Safari → Settings → Advanced → Show features for web developers**, then **Developer → Allow JavaScript from Apple Events**. See [Apple's Developer settings](https://developer.apple.com/documentation/safari-developer-tools/developer-settings) and [WebKit's developer-feature instructions](https://webkit.org/web-inspector/enabling-web-inspector/). Installed AppleScript dictionaries were inspected at `/Applications/Safari.app/Contents/Resources/Safari.sdef` and `/Applications/Microsoft Edge.app/Contents/Resources/scripting.sdef`.

## Small browser bridge

From the repository root:

```sh
python3 marketing/reddit/scripts/browser.py probe
python3 marketing/reddit/scripts/browser.py open 'https://www.reddit.com/'
```

`open` returns `window_id` and `tab_id`. Retain both for this run. Use only that dedicated window; never select an arbitrary front tab. Substitute those IDs below:

```sh
python3 marketing/reddit/scripts/browser.py status --window-id 123 --tab-id 456
python3 marketing/reddit/scripts/browser.py eval --window-id 123 --tab-id 456 --expect-url 'https://www.reddit.com/' --js-file /tmp/reddit-inspect.js
```

For example, the JS file can contain `JSON.stringify({url:location.href,title:document.title})`. Pass code through a file, not shell interpolation. `eval` checks the exact expected URL both before and inside JavaScript, and refuses to operate if it changed. It also requires an execution marker, so an empty browser response cannot masquerade as successful JavaScript. `status` reads only the specified tab. Re-read status after navigation, then verify the DOM's URL and readiness with read-only JavaScript before entering content; a browser URL alone does not prove the document loaded. The bridge captures stable IDs, lets a new window initialize before navigating, bounds Apple Events and subprocess timeouts, and never retries automatically. Only read-only readiness checks may be retried while a page loads.

Use `close` with the same IDs and `--expect-url` to close only the owned tab when finished. A normal window shares the browser's login session; the helper does not read, store, or inject cookies.

## Posting workflow

1. Inspect the live subreddit rules and posting UI. Verify account, destination, post type, and required flair. Use the category examples and actual product evidence as described in `AGENTS.md`.
2. Inspect current controls and labels before writing selectors; Reddit's markup changes. Traverse open shadow roots if needed. Set inputs using their native setters and dispatch bubbling `input`/`change` events; inspect rendered values afterward. Rich-text editors may need their own input handling. Do not assume setting `innerHTML` changes editor state.
3. Fill the title/body and any required flair. Read the final visible text back, checking code formatting and links. Submit once when the task authorizes publishing. Draft-only requests stop before submission.
4. Wait for navigation or a visible submission result, then confirm the resulting permalink, author, title, body, and moderation status. For a comment in a promotion thread, verify its parent thread and body instead of a title. If the outcome is uncertain, inspect the profile's submissions or comments, matching the contribution type, before any retry. A created post may still be pending moderation or removed; report that accurately.
5. Stop for a CAPTCHA, login/2FA prompt, browser permission prompt, rate limit, or subreddit prohibition. Do not replay the pasted GraphQL, tracking, reCAPTCHA, or signed partial-page requests to publish.

Keep new post links and statuses in the run report, separate from the frozen example corpus. The live campaign validated Reddit's classic UI. A valid permalink and authenticated view do not by themselves guarantee public visibility or moderator approval.

## Video drafts: verified November 8, 2026

The redesigned composer was verified with 18 unsubmitted video drafts, including formatted bodies, completed uploads, and selected flairs. See the [draft report](runs/2026-11-08-archunit-video-drafts.md). The recordings remain outside this repository in a temporary directory recorded there.

- JavaScript can focus the visible Video control, but opening its file chooser required a native Space key through macOS System Events. Verify the dedicated window/tab and focused control before keyboard input. Accessibility permission is separate from JavaScript from Apple Events.
- In the native file chooser, use Go to Folder to select the exact local recording. Confirm each expected dialog before advancing; never send Return to the composer itself. Wait for the upload indicator to disappear and a valid video preview to appear.
- The rich-text editor accepted a clipboard paste event containing both plain text and escaped HTML paragraphs. Plain `insertText` collapsed paragraph breaks. Verify the final rendered body against the intended text, not just the event's return value.
- Flair radio selection worked through JavaScript, but the dialog's Add button needed native keyboard activation. Confirm the dialog closes and the applied flair chip appears; a checked radio alone is insufficient.
- Reddit disabled Save Draft for these video forms. Leave requested review tabs open and preserve a local text/metadata backup. A fresh composer URL does not restore their contents. Do not close or reload populated draft tabs during cleanup.
