#!/usr/bin/env python3
"""Reserve one paced Reddit action; never send requests, sleep, or retry.

Only acquire's ``reserved`` result permits the caller to perform one action.
After a rate limit, the first permitted action is one read-only probe. Call
probe-ok only after checking that response succeeded, never for a 403, timeout,
or other error. Until then, further actions remain blocked. A newly observed
rate limit starts another cooldown through rate-limit.
"""

import argparse
from contextlib import contextmanager
from email.utils import parsedate_to_datetime
import fcntl
import json
import math
import os
from pathlib import Path
import tempfile
import time

ACTION_INTERVAL = 15
POST_INTERVAL = 120
DEFAULT_COOLDOWN = 900
DEFAULT_STATE = Path(f"/private/tmp/codex-reddit-request-guard-{os.getuid()}.json")


def empty_state():
    return {
        "schema_version": 1,
        "last_action_at": None,
        "last_post_at": None,
        "blocked_until": None,
        "probe_required": False,
        "probe_pending": False,
    }


def timestamp(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("Invalid timestamp")
    try:
        valid = math.isfinite(value) and value >= 0
    except OverflowError:
        valid = False
    if not valid:
        raise ValueError("Invalid timestamp")
    return value


def validate_state(state):
    if not isinstance(state, dict) or set(state) != set(empty_state()):
        raise ValueError("Malformed request guard state; do not reset it automatically")
    if type(state["schema_version"]) is not int or state["schema_version"] != 1:
        raise ValueError("Unsupported request guard state version")
    for field in ("last_action_at", "last_post_at", "blocked_until"):
        if state[field] is not None:
            timestamp(state[field])
    for field in ("probe_required", "probe_pending"):
        if type(state[field]) is not bool:
            raise ValueError("Invalid request guard probe state")
    if (state["probe_pending"] or state["blocked_until"] is not None) and not state["probe_required"]:
        raise ValueError("Inconsistent request guard cooldown state")
    if state["last_post_at"] is not None and (
        state["last_action_at"] is None or state["last_post_at"] > state["last_action_at"]
    ):
        raise ValueError("Inconsistent request guard submission timing")
    return state


def load_state(path):
    try:
        with Path(path).open(encoding="utf-8") as handle:
            return validate_state(json.load(handle))
    except FileNotFoundError:
        return empty_state()
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ValueError("Malformed request guard state; do not reset it automatically") from exc


def save_state(path, state):
    validate_state(state)
    path = Path(path)
    descriptor, name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2, allow_nan=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextmanager
def locked(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path.with_name(path.name + ".lock"), os.O_CREAT | os.O_RDWR, 0o600)
    with os.fdopen(descriptor, "a+") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield load_state(path)
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def remaining(deadline, now):
    return max(0, math.ceil((deadline or 0) - now))


def action_wait(state, kind, now):
    deadline = state["last_action_at"] + ACTION_INTERVAL if state["last_action_at"] is not None else 0
    if kind == "post" and state["last_post_at"] is not None:
        deadline = max(deadline, state["last_post_at"] + POST_INTERVAL)
    return remaining(deadline, now)


def acquire(kind, path=DEFAULT_STATE, now=None):
    """Reserve one read/post action, or return wait/blocked without changing state."""
    if kind not in ("read", "post"):
        raise ValueError("kind must be read or post")
    now = timestamp(time.time() if now is None else now)
    with locked(path) as state:
        wait = remaining(state["blocked_until"], now)
        if wait:
            return {"status": "wait", "reason": "rate-limit", "wait_seconds": wait}
        if state["probe_pending"]:
            return {"status": "blocked", "reason": "probe-result-required", "wait_seconds": None}
        if state["probe_required"] and kind == "post":
            return {"status": "blocked", "reason": "read-only-probe-required", "wait_seconds": 0}
        wait = action_wait(state, kind, now)
        if wait:
            return {"status": "wait", "reason": "action-spacing", "wait_seconds": wait}
        probe = state["probe_required"]
        state["last_action_at"] = now
        if kind == "post":
            state["last_post_at"] = now
        if probe:
            state["probe_pending"] = True
        save_state(path, state)
        return {"status": "reserved", "kind": kind, "probe": probe, "wait_seconds": 0}


def retry_deadline(value, now):
    if value is not None:
        value = str(value).strip()
        try:
            if value.isascii() and value.isdigit():
                return timestamp(now + int(value))
            parsed = parsedate_to_datetime(value)
            if parsed.tzinfo is not None:
                return max(now, timestamp(parsed.timestamp()))
        except (TypeError, ValueError, OverflowError, IndexError):
            pass
    return now + DEFAULT_COOLDOWN


def rate_limit(retry_after=None, path=DEFAULT_STATE, now=None):
    """Record a server cooldown; never shorten a cooldown already in progress."""
    now = timestamp(time.time() if now is None else now)
    deadline = retry_deadline(retry_after, now)
    with locked(path) as state:
        state["blocked_until"] = max(state["blocked_until"] or 0, deadline)
        state["last_action_at"] = max(state["last_action_at"] or 0, now)
        state["probe_required"] = True
        state["probe_pending"] = False
        save_state(path, state)
        return {
            "status": "blocked",
            "reason": "rate-limit",
            "wait_seconds": remaining(state["blocked_until"], now),
            "blocked_until": state["blocked_until"],
            "next_action": "one read-only probe after cooldown",
        }


def probe_ok(path=DEFAULT_STATE):
    """Acknowledge a verified successful probe, never an error/403 response."""
    with locked(path) as state:
        if not state["probe_pending"]:
            raise ValueError("No pending recovery probe to confirm")
        state["probe_required"] = False
        state["probe_pending"] = False
        state["blocked_until"] = None
        save_state(path, state)
        return {"status": "probe-confirmed", "note": "Normal read/post spacing still applies"}


def status(path=DEFAULT_STATE, now=None):
    """Read an atomic snapshot, without creating or changing state or lock files."""
    now = timestamp(time.time() if now is None else now)
    state = load_state(path)
    wait = remaining(state["blocked_until"], now)
    label = "cooldown" if wait else (
        "probe-pending" if state["probe_pending"] else (
            "probe-required" if state["probe_required"] else "ready"
        )
    )
    return {
        "status": label,
        "cooldown_wait_seconds": wait,
        "read_spacing_wait_seconds": action_wait(state, "read", now),
        "post_spacing_wait_seconds": action_wait(state, "post", now),
        **state,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Reserve a paced Reddit action slot; this command does not execute any request.",
        epilog="Only acquire status=reserved authorizes one action. Waiting never sleeps or retries. "
               "All worktrees share the default file. Do not switch files to bypass a cooldown.",
    )
    parser.add_argument("--state-file", type=Path, default=DEFAULT_STATE,
                        help="Isolated-test override; place before the subcommand")
    commands = parser.add_subparsers(dest="command", required=True)
    reserve = commands.add_parser("acquire", help="Reserve one action, or exit 2 with wait/blocked")
    reserve.add_argument("--kind", choices=("read", "post"), required=True,
                         help="post includes comment submissions")
    limit = commands.add_parser("rate-limit", help="Record HTTP 429 and require a recovery probe")
    limit.add_argument("--retry-after", help="Retry-After seconds or HTTP-date; invalid/absent means 15 minutes")
    commands.add_parser("probe-ok", help="Confirm a verified successful pending probe; never use for errors/403")
    commands.add_parser("status", help="Read-only timing snapshot; does not reserve an action")
    args = parser.parse_args(argv)
    try:
        if args.command == "acquire":
            result = acquire(args.kind, args.state_file)
        elif args.command == "rate-limit":
            result = rate_limit(args.retry_after, args.state_file)
        elif args.command == "probe-ok":
            result = probe_ok(args.state_file)
        else:
            result = status(args.state_file)
        print(json.dumps(result))
        return 2 if args.command == "acquire" and result["status"] != "reserved" else 0
    except (ValueError, OSError) as exc:
        print(json.dumps({"status": "error", "message": str(exc), "action": "Do not send a request"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
