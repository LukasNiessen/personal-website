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
import re
import tempfile
import time
import uuid

ACTION_INTERVAL = 15
POST_INTERVAL = 120
DEFAULT_COOLDOWN = 900
WEEK = 7 * 24 * 60 * 60
WEEKLY_LIMIT = 2
DEFAULT_STATE = Path(f"/private/tmp/codex-reddit-request-guard-{os.getuid()}.json")


def empty_state():
    return {
        "schema_version": 2,
        "last_action_at": None,
        "last_post_at": None,
        "blocked_until": None,
        "probe_required": False,
        "probe_pending": False,
        "history_initialized": False,
        "posts": {},
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


def subreddit_name(value):
    if not isinstance(value, str):
        raise ValueError("A subreddit is required for every post reservation")
    value = value.strip().lower().removeprefix('/').removeprefix('r/').rstrip('/')
    if not re.fullmatch(r'[a-z0-9_]{1,21}', value):
        raise ValueError("Use a subreddit name, such as angular or r/angular")
    return value


def validate_state(state):
    if not isinstance(state, dict) or set(state) != set(empty_state()):
        raise ValueError("Malformed request guard state; do not reset it automatically")
    if type(state["schema_version"]) is not int or state["schema_version"] != 2:
        raise ValueError("Unsupported request guard state version")
    for field in ("last_action_at", "last_post_at", "blocked_until"):
        if state[field] is not None:
            timestamp(state[field])
    for field in ("probe_required", "probe_pending", "history_initialized"):
        if type(state[field]) is not bool:
            raise ValueError("Invalid request guard probe state")
    if (state["probe_pending"] or state["blocked_until"] is not None) and not state["probe_required"]:
        raise ValueError("Inconsistent request guard cooldown state")
    if state["last_post_at"] is not None and (
        state["last_action_at"] is None or state["last_post_at"] > state["last_action_at"]
    ):
        raise ValueError("Inconsistent request guard submission timing")
    if not isinstance(state['posts'], dict):
        raise ValueError("Malformed posting history; do not reset it")
    for identity, post in state['posts'].items():
        if not re.fullmatch(r'(?:t[13]_[a-z0-9]+|pending_[a-f0-9]{32})', identity):
            raise ValueError("Invalid post or reservation ID")
        if not isinstance(post, dict) or set(post) != {'subreddit', 'created_at'}:
            raise ValueError("Invalid posting-history record")
        if subreddit_name(post['subreddit']) != post['subreddit']:
            raise ValueError("Posting history must use normalized subreddit names")
        timestamp(post['created_at'])
    return state


def load_state(path):
    try:
        with Path(path).open(encoding="utf-8") as handle:
            state = json.load(handle)
        if isinstance(state, dict) and type(state.get('schema_version')) is int and state['schema_version'] == 1:
            expected = set(empty_state()) - {'history_initialized', 'posts'}
            if set(state) != expected:
                raise ValueError("Malformed legacy guard state; preserve it")
            # Retain all pacing/cooldown state. Posts stay blocked until history is imported.
            state = dict(state, schema_version=2, history_initialized=False, posts={})
        return validate_state(state)
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


def weekly_status(state, subreddit, now):
    times = sorted(post['created_at'] for post in state['posts'].values()
                   if post['subreddit'] == subreddit and post['created_at'] > now - WEEK)
    return {'subreddit': subreddit, 'limit': WEEKLY_LIMIT, 'count': len(times),
            'remaining': max(0, WEEKLY_LIMIT - len(times)),
            'next_available_at': times[-WEEKLY_LIMIT] + WEEK if len(times) >= WEEKLY_LIMIT else None}


def acquire(kind, path=DEFAULT_STATE, now=None, subreddit=None):
    """Reserve one read/post action, or return wait/blocked without changing state."""
    if kind not in ("read", "post"):
        raise ValueError("kind must be read or post")
    if kind == 'post':
        subreddit = subreddit_name(subreddit)
    now = timestamp(time.time() if now is None else now)
    with locked(path) as state:
        wait = remaining(state["blocked_until"], now)
        if wait:
            return {"status": "wait", "reason": "rate-limit", "wait_seconds": wait}
        if state["probe_pending"]:
            return {"status": "blocked", "reason": "probe-result-required", "wait_seconds": None}
        if state["probe_required"] and kind == "post":
            return {"status": "blocked", "reason": "read-only-probe-required", "wait_seconds": 0}
        if kind == 'post':
            if not state['history_initialized']:
                return {'status': 'blocked', 'reason': 'posting-history-required', 'wait_seconds': None}
            weekly = weekly_status(state, subreddit, now)
            if not weekly['remaining']:
                return {'status': 'blocked', 'reason': 'subreddit-weekly-cap', **weekly,
                        'wait_seconds': remaining(weekly['next_available_at'], now)}
        wait = action_wait(state, kind, now)
        if wait:
            return {"status": "wait", "reason": "action-spacing", "wait_seconds": wait}
        probe = state["probe_required"]
        state["last_action_at"] = now
        if kind == "post":
            state["last_post_at"] = now
            reservation_id = 'pending_' + uuid.uuid4().hex
            state['posts'][reservation_id] = {'subreddit': subreddit, 'created_at': now}
        if probe:
            state["probe_pending"] = True
        save_state(path, state)
        result = {"status": "reserved", "kind": kind, "probe": probe, "wait_seconds": 0}
        if kind == 'post':
            result.update(reservation_id=reservation_id, subreddit=subreddit)
        return result


def confirmed_record(record, now):
    if not isinstance(record, dict) or set(record) != {'id', 'subreddit', 'created_at'}:
        raise ValueError("History requires id, subreddit and created_at per post")
    identity = record['id']
    if not isinstance(identity, str) or not re.fullmatch(r't[13]_[a-z0-9]+', identity):
        raise ValueError("Use a Reddit post/comment ID, such as t3_abc123")
    at = timestamp(record['created_at'])
    if at > now:
        raise ValueError("A confirmed post cannot be in the future")
    return identity, {'subreddit': subreddit_name(record['subreddit']), 'created_at': at}


def import_posts(records, path=DEFAULT_STATE, now=None):
    """Merge observed publication metadata without removing history or pending attempts."""
    now = timestamp(time.time() if now is None else now)
    if not isinstance(records, list):
        raise ValueError("Expected a list of observed posts")
    records = [confirmed_record(record, now) for record in records]
    with locked(path) as state:
        for identity, post in records:
            if identity in state['posts'] and state['posts'][identity] != post:
                raise ValueError("Conflicting publication metadata for " + identity)
            state['posts'][identity] = post
        state['history_initialized'] = True
        save_state(path, state)
        return {'status': 'imported', 'records': len(records)}


def confirm_post(reservation_id, post_id, created_at, path=DEFAULT_STATE, now=None):
    """Replace one pending attempt with its observed publication, even if later removed."""
    now = timestamp(time.time() if now is None else now)
    with locked(path) as state:
        if not reservation_id.startswith('pending_') or reservation_id not in state['posts']:
            raise ValueError("No pending reservation with that ID")
        pending = state['posts'][reservation_id]
        identity, post = confirmed_record({'id': post_id, 'subreddit': pending['subreddit'],
                                           'created_at': created_at}, now)
        if created_at < pending['created_at'] - 300:
            raise ValueError("Publication predates this reservation; inspect instead of freeing its slot")
        if identity in state['posts'] and state['posts'][identity] != post:
            raise ValueError("Conflicting publication metadata")
        del state['posts'][reservation_id]
        state['posts'][identity] = post
        save_state(path, state)
        return {'status': 'confirmed', 'post_id': identity, 'subreddit': post['subreddit']}


def cancel_post(reservation_id, reason, path=DEFAULT_STATE):
    """Release only a verified non-submission. Ambiguous or removed posts must stay counted."""
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("Explain the observed proof that no submission occurred")
    with locked(path) as state:
        if not reservation_id.startswith('pending_') or reservation_id not in state['posts']:
            raise ValueError("Only pending reservations can be cancelled")
        del state['posts'][reservation_id]
        save_state(path, state)
        return {'status': 'cancelled', 'reservation_id': reservation_id, 'reason': reason}


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


def status(path=DEFAULT_STATE, now=None, subreddit=None):
    """Read an atomic snapshot, without creating or changing state or lock files."""
    now = timestamp(time.time() if now is None else now)
    state = load_state(path)
    wait = remaining(state["blocked_until"], now)
    label = "cooldown" if wait else (
        "probe-pending" if state["probe_pending"] else (
            "probe-required" if state["probe_required"] else "ready"
        )
    )
    result = {
        "status": label,
        "cooldown_wait_seconds": wait,
        "read_spacing_wait_seconds": action_wait(state, "read", now),
        "post_spacing_wait_seconds": action_wait(state, "post", now),
        **{key: value for key, value in state.items() if key != 'posts'},
        'posts_tracked': len(state['posts']),
        'pending_reservations': {key: value for key, value in state['posts'].items() if key.startswith('pending_')},
    }
    if subreddit is not None:
        result['weekly'] = weekly_status(state, subreddit_name(subreddit), now)
    return result


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
    reserve.add_argument('--subreddit', help='Required for posts; weekly cap is shared across campaigns')
    importing = commands.add_parser('import-posts', help='Merge observed post metadata; never reset history')
    importing.add_argument('--file', type=Path, required=True,
                           help='JSON list of {id, subreddit, created_at}; timestamps are Unix seconds')
    confirm = commands.add_parser('confirm-post', help='Record a verified publication against its reservation')
    confirm.add_argument('--reservation', required=True)
    confirm.add_argument('--post-id', required=True)
    confirm.add_argument('--created-at', type=float, required=True)
    cancel = commands.add_parser('cancel-post', help='Release a verified non-submission, never an ambiguous attempt')
    cancel.add_argument('--reservation', required=True)
    cancel.add_argument('--reason', required=True)
    limit = commands.add_parser("rate-limit", help="Record HTTP 429 and require a recovery probe")
    limit.add_argument("--retry-after", help="Retry-After seconds or HTTP-date; invalid/absent means 15 minutes")
    commands.add_parser("probe-ok", help="Confirm a verified successful pending probe; never use for errors/403")
    inspection = commands.add_parser("status", help="Read-only timing snapshot; does not reserve an action")
    inspection.add_argument('--subreddit', help='Also show remaining weekly capacity for this community')
    args = parser.parse_args(argv)
    try:
        if args.command == "acquire":
            result = acquire(args.kind, args.state_file, subreddit=args.subreddit)
        elif args.command == 'import-posts':
            result = import_posts(json.loads(args.file.read_text()), args.state_file)
        elif args.command == 'confirm-post':
            result = confirm_post(args.reservation, args.post_id, args.created_at, args.state_file)
        elif args.command == 'cancel-post':
            result = cancel_post(args.reservation, args.reason, args.state_file)
        elif args.command == "rate-limit":
            result = rate_limit(args.retry_after, args.state_file)
        elif args.command == "probe-ok":
            result = probe_ok(args.state_file)
        else:
            result = status(args.state_file, subreddit=args.subreddit)
        print(json.dumps(result))
        return 2 if args.command == "acquire" and result["status"] != "reserved" else 0
    except (ValueError, OSError) as exc:
        print(json.dumps({"status": "error", "message": str(exc), "action": "Do not send a request"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
