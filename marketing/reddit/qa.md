# Setup QA · 2026-11-08

This setup publishes no Reddit posts or comments. Live account/composer/submission testing is deferred until the user logs in and requests a posting test.

## Checks completed

- Retrieved 10 authenticated submission-listing pages until `after=null`: 922 unique submissions. Saved 675 promotional originals and an exclusion audit for 247 others. No cookie/token was saved in the workspace.
- Compared every retained title and body byte-for-byte against the fetched source and verified SHA-256 hashes, unique IDs, author, permalink, removal metadata, cutoff dates, and complete included/excluded accounting. All passed.
- Verified the local repository paths in the product registry. Canonical names and public links come from each repository's README and Git remote. Planned language-library APIs are distinguished from usable implementations.
- Checked the example selector's category routing, five/six-example limit, body integrity, exclusions for already-read IDs, empty selection, and invalid arguments. It runs locally without network access or corpus writes.
- Reviewed current subreddit guidance and marked restricted, thread-only, and unverified destinations. Added Django after reviewing the first registry draft.
- Reviewed instruction routing, publication/draft-only defaults, category-specific approaches, frozen corpus behavior, and outcome reporting. Corrected ambiguous-submit recovery to check comment history for comments.
- Reviewed curated samples for repeated prose and replaced a near-duplicate project introduction with a more varied original.

## Draft-only workflow smoke check

Input scenario: “Write a gift promotion for ArchUnitTS for an Angular audience, drafts only.”

The route resolves the spoken product to `ArchUnitTS`, selects `gift-promotion`, reads five category examples once, matches `r/angular`, and checks the feature against the current local implementation/test. Candidate destination remains subject to live community rules; no browser publication is attempted.

Evidence: `/Users/78079/Repos/Private/ArchUnitTS/test/files/integration/public-api-boundary.spec.ts` checks allowed barrel imports and forbidden direct internal imports. Its source was inspected; its Jest suite could not be run because this checkout has no installed Jest dependency. This checks the drafting/evidence workflow, not the public package's release state.

Sample draft, retained here as QA output only, never added to the voice corpus:

**Title:** Keeping Angular feature internals out of other features

An Angular feature can have a public API and still end up with half the app importing its internal files. The imports compile, so it's easy to miss how coupled the features have become.

I maintain ArchUnitTS, a library for checking architecture rules in TypeScript projects. One useful rule for this is allowing imports through `index.ts` or `public-api.ts`, while blocking imports into the rest of a feature's folder.

For example, another feature can import from `../orders`, but reaching into `../orders/internal/order.service` fails the architecture check. Files inside `orders` can still use their own internals.

You define the boundary as a test and run it with the rest of your suite. So when someone adds a direct import later, there's a failing test pointing at it.

Repo: [ArchUnitTS](https://github.com/LukasNiessen/ArchUnitTS)

The draft has no em dash, fabricated community request, copied headline, popularity claim, or unsupported “new release” claim. It explains one verified use case in the author's direct technical voice.

## Browser verification

Selected Microsoft Edge. Enabled and verified its Apple Events JavaScript menu setting. The live blank-window test passed: input changed, an `input` event updated another element, a button click fired, expected values were returned, and the owned window closed.

Independent bridge checks also passed: foreign/non-HTTPS/credential-bearing URLs are rejected before Apple Events; JS travels as an argument without shell interpolation; a simulated navigation race blocks the payload before it executes; quotes, newlines, dollar signs and backticks survive argument transport. An execution marker now distinguishes a confirmed JS return from an empty/unconfirmed response; missing markers fail explicitly. Both Python helpers parse successfully.

The initial Reddit check observed a crashed/`about:blank` document. Follow-up investigation found the browser still running 156.0.4314.58 after the installed app had updated to 157.0.4341.42 and removed the old framework. A session-restoring restart and explicit app reopen loaded 157; process inspection confirmed the version change. Reddit then reached `readyState: complete`, the expected page title, 17,154 body characters, and 30 Reddit elements. A separate reload also reached a complete rendered Reddit page. This resolves the earlier loading limitation and supersedes the tentative new-window timing diagnosis.

The browser retained an 18-tab session; some work sites redirected to their sign-in pages. The working Reddit window was left open, the empty restart placeholder closed, and private tab-URL snapshots deleted. Login/account identity and a read-only composer check still precede the later authorized publishing test.

See [browser.md](browser.md) for exact commands, setup requirements, and the boundary of live verification. The browser's actual Reddit login and editor submission still require the user's later test run.

## Coverage limits

Reddit may omit deleted/inaccessible history or apply a backend history cap even when pagination ends. All returned records carry removal/filter metadata; it does not establish the cause. Link-only posts have no body to reconstruct. Current subreddit rules and the selected product's release/API must be checked again for each real campaign.

## Cache and pacing · 2026-11-14

- Seeded 160 community entries from existing local records, including all 140 recoverable historical posting destinations. Forty rule snapshots and four unavailable responses expire two calendar months after their November 13 observation. Missing observations remain explicit misses. No Reddit request was needed to seed the cache.
- Twenty offline tests passed: calendar-month expiry (including leap years), expired/missing entries, preservation of posting history, rejected 429 cache updates, concurrent pacing reservations, read/post intervals, Retry-After seconds/HTTP dates, cooldown recovery probes, malformed-state handling, and denial before browser navigation.
- Existing frozen post bodies and the corpus manifest were unchanged. Pacing is a local load control; it does not establish community permission or guarantee moderation outcomes.
