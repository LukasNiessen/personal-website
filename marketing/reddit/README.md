# Team setup for Reddit campaigns

You need this workspace and the source for the product you plan to write about. Git and Python handle repository setup, the frozen writing examples and the community rule cache. Publishing also requires Microsoft Edge on a Mac.

## Open the workspace

Check that Git and Python 3.9 or newer are available. If needed, install them first. [Git downloads](https://git-scm.com/downloads) · [Python downloads](https://www.python.org/downloads/)

```sh
git --version
python3 --version
```

Clone the workspace or open your existing checkout in Codex or Claude Code. Run the remaining commands from its root. You can skip the website's npm setup. When a post needs a runnable example, use the toolchain specified by that product.

```sh
git clone https://github.com/LukasNiessen/personal-website.git
cd personal-website
```

For a guided start, paste this into either agent from the workspace root. Replace the product and source folder with your own.

> Read marketing/reddit/AGENTS.md and follow marketing/reddit/README.md. Set me up for ArchUnitPython. My repositories are in ~/Projects. Reuse my checkout or clone it there if missing. Help me verify Edge on this Mac. This is setup only.

## Find the product source

```sh
python3 marketing/reddit/scripts/repos.py setup ArchUnitPython --root ~/Projects --clone-missing
python3 marketing/reddit/scripts/repos.py path ArchUnitPython
```

The first command reuses a matching Git checkout or clones the missing product. Omit `--clone-missing` for discovery only. Pass multiple product names for a campaign covering several libraries. By default the helper looks beside this workspace. With `--root` it checks that folder and its immediate children with known repository names. Give the exact path for a renamed or deeply nested checkout. You can repeat `--root`; missing clones go in the first folder, or beside it if that folder is itself a checkout. Git needs network access for missing clones and your usual GitHub access for private repositories.

The second command prints the verified local path that the agent will use. Setup saves paths under the Git-ignored `marketing/reddit/.local/repos/` in this checkout. If you move a library, rerun setup with its new location. The shared registry contains public links and hints about where to look for a feature. [Product registry](products.md)

## Try a draft

> Read marketing/reddit/AGENTS.md. Draft one ArchUnitPython gift promotion for a FastAPI audience. Return the title, body and proposed destination here in chat only.

A chat draft works before you set up Edge or sign in to Reddit. Check that it shows a concrete result and gives your actual relationship to the project. The agent flags any eligibility checks the publisher still needs to make. **Say “draft only” when you want to review first.** The workspace treats an ordinary promotion request as permission to publish.

## Set up a publishing Mac

1. Open the normal Microsoft Edge profile you'll use for the campaign. Sign in to Reddit yourself. Open Reddit's account menu and note the exact username. [Download Edge](https://www.microsoft.com/edge/download)
2. In Edge's macOS menu bar, open **View → Developer** and check **Allow JavaScript from Apple Events**. If it's already checked, leave it enabled.
3. Ask the same app you'll use for campaigns to run the command below. When macOS prompts, allow that app to control Microsoft Edge. You can review the grant in **System Settings → Privacy & Security → Automation**. The probe exercises an input and button in its own blank window and closes the tab. Look for `"eventResult": "apple-events-ok"` and `"clicked": true`.

```sh
python3 marketing/reddit/scripts/browser.py probe
```

For a first live run, name the account and keep the count small. Replace the placeholder with the username you confirmed.

> Read marketing/reddit/AGENTS.md. Publish one ArchUnitPython gift promotion in an eligible community as u/YOUR_USERNAME. Report the permalink and moderation status.

The publishing agent verifies the account in its own Edge window. One teammate can publish while others draft. The weekly cap is **two promotional contributions per subreddit across the team in a rolling seven days**. Each Mac and macOS user keeps a separate ledger. Before switching publishers, reconcile recent team submissions and pending attempts. [Browser troubleshooting](browser.md) · [Publisher handoff](cache.md#switching-publishers)

## Windows

Windows teammates can set up product checkouts, read the example posts and cached rules, and draft in chat. In PowerShell, run the same Python commands with `py -3 -X utf8` in place of `python3`, and use your Windows source folder. The cache uses the Europe/Berlin timezone. If Python reports missing timezone data, run `py -3 -m pip install tzdata` in the same Python environment. [Python timezone support](https://docs.python.org/3/library/zoneinfo.html#data-sources)

```powershell
py -3 -X utf8 marketing/reddit/scripts/repos.py setup ArchUnitPython --root "$HOME\Projects" --clone-missing
py -3 -X utf8 marketing/reddit/scripts/select_examples.py gift-promotion --list
```

Hand drafts to a Mac publisher for browser review or submission. The current bridge uses macOS Apple Events and the posting ledger uses Unix file locking. Native Windows publishing would need a browser bridge such as Edge WebDriver and a compatible ledger lock. [Microsoft Edge WebDriver](https://learn.microsoft.com/en-us/microsoft-edge/webdriver/)
