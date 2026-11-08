#!/usr/bin/env python3
"""Targeted Microsoft Edge Apple Events bridge. No publishing logic or credentials."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit


def run(script, *arguments):
    source = 'on run argv\nwith timeout of 10 seconds\ntell application "Microsoft Edge"\n' + script + '\nend tell\nend timeout\nend run\n'
    try:
        result = subprocess.run(
            ["osascript", "-", *map(str, arguments)], input=source,
            text=True, capture_output=True, timeout=15, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("Apple Events timed out. Inspect Edge before retrying any action; its outcome may be unknown.") from exc
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "Apple Events failed")
    return result.stdout.rstrip("\n")


def open_tab(url):
    parsed = urlsplit(url)
    if url != "about:blank" and not (
        parsed.scheme == "https" and parsed.hostname in {"reddit.com", "www.reddit.com", "old.reddit.com"}
        and not parsed.username and not parsed.password
    ):
        raise ValueError("Open only about:blank or an HTTPS Reddit URL.")
    ids = run('''set taskWindow to make new window
set taskWindowID to id of taskWindow
delay 1
set taskTab to active tab of taskWindow
set taskTabID to id of taskTab
set URL of taskTab to item 1 of argv
return (taskWindowID as text) & ":" & (taskTabID as text)''', url).split(":")
    return {"window_id": int(ids[0]), "tab_id": int(ids[1])}


TARGET = '''set taskWindow to window id (item 1 of argv as integer)
set taskTab to tab id (item 2 of argv as integer) of taskWindow
'''


def evaluate(window_id, tab_id, expected_url, javascript):
    # Check URL again inside the same JS evaluation to detect a navigation race.
    sentinel = "__REDDIT_BRIDGE_EXECUTED__:"
    guarded = "(() => { if (location.href !== " + json.dumps(expected_url) + ") throw new Error('Target URL changed'); return " + json.dumps(sentinel) + " + String((0,eval)(" + json.dumps(javascript) + ")); })()"
    result = run(TARGET + '''if URL of taskTab is not item 3 of argv then error "Target URL changed; inspect the tab before continuing."
return execute taskTab javascript (item 4 of argv)''', window_id, tab_id, expected_url, guarded)
    if not result.startswith(sentinel):
        raise RuntimeError("JavaScript execution was not confirmed. DOM may not be ready or script execution may be blocked. Inspect before retrying; never retry a mutation blindly.")
    return result[len(sentinel):]


def close_tab(window_id, tab_id, expected_url):
    return run(TARGET + '''if URL of taskTab is not item 3 of argv then error "Target URL changed; refusing to close."
close taskTab''', window_id, tab_id, expected_url)


def probe():
    target = open_tab("about:blank")
    try:
        result = evaluate(**target, expected_url="about:blank", javascript='''(() => {
          document.body.innerHTML = '<input id="probe"><button id="go">Test</button><p id="out"></p>';
          const input = document.querySelector('#probe');
          input.addEventListener('input', () => document.querySelector('#out').textContent = input.value);
          input.value = 'apple-events-ok';
          input.dispatchEvent(new Event('input', {bubbles:true}));
          let clicked = false;
          document.querySelector('#go').addEventListener('click', () => clicked = true);
          document.querySelector('#go').click();
          return JSON.stringify({value:input.value,eventResult:document.querySelector('#out').textContent,clicked});
        })()''')
        data = json.loads(result)
        if data != {"value": "apple-events-ok", "eventResult": "apple-events-ok", "clicked": True}:
            raise RuntimeError("DOM probe returned unexpected data: " + result)
        return data
    finally:
        close_tab(**target, expected_url="about:blank")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("probe", help="Create a blank window, verify DOM events, then close it")
    opening = commands.add_parser("open", help="Open a dedicated Reddit window and return its stable IDs")
    opening.add_argument("url")
    for name in ("status", "eval", "close"):
        command = commands.add_parser(name)
        command.add_argument("--window-id", type=int, required=True)
        command.add_argument("--tab-id", type=int, required=True)
        if name != "status":
            command.add_argument("--expect-url", required=True, help="Exact URL observed in status")
        if name == "eval":
            command.add_argument("--js-file", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "probe":
        print(json.dumps(probe()))
    elif args.command == "open":
        print(json.dumps(open_tab(args.url)))
    elif args.command == "status":
        value = run(TARGET + 'return URL of taskTab', args.window_id, args.tab_id)
        print(json.dumps({"window_id": args.window_id, "tab_id": args.tab_id, "url": value}))
    elif args.command == "eval":
        print(evaluate(args.window_id, args.tab_id, args.expect_url, args.js_file.read_text()))
    else:
        close_tab(args.window_id, args.tab_id, args.expect_url)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
