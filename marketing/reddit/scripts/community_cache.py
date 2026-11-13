#!/usr/bin/env python3
"""Local Reddit rule summaries. No network calls; observations last two calendar months."""
import argparse
import calendar
from datetime import date, datetime
import json
from pathlib import Path
import re
import sys
import tempfile
from zoneinfo import ZoneInfo

CACHE = Path(__file__).resolve().parents[1] / 'community-cache.json'


def today():
    return datetime.now(ZoneInfo('Europe/Berlin')).date()


def name(value):
    value = value.strip().lower().removeprefix('/').removeprefix('r/').rstrip('/')
    if not re.fullmatch(r'[a-z0-9_]{1,21}', value):
        raise ValueError('Use a subreddit name, such as angular or r/angular')
    return value


def expires(checked):
    month = checked.month + 2
    year = checked.year + (month - 1) // 12
    month = (month - 1) % 12 + 1
    return date(year, month, min(checked.day, calendar.monthrange(year, month)[1]))


def read_cache(path=CACHE):
    if not path.exists():
        return {'schema_version': 1, 'communities': {}}
    data = json.loads(path.read_text())
    if data.get('schema_version') != 1 or not isinstance(data.get('communities'), dict):
        raise ValueError('Invalid cache format; preserve the file and inspect it')
    return data


def write_cache(data, path=CACHE):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        json.dump(data, handle, indent=2, ensure_ascii=False, sort_keys=True)
        handle.write('\n')
    temporary.replace(path)


def state(entry, on=None):
    on = on or today()
    if not entry or entry.get('fetch_status') == 'missing':
        return 'missing'
    if entry.get('fetch_status') not in ('ok', 'unavailable'):
        raise ValueError('Invalid observation status')
    checked = date.fromisoformat(entry['checked_at'])
    expiry = date.fromisoformat(entry['expires_at'])
    if checked > on or expiry > expires(checked):
        raise ValueError('Invalid cache dates; refresh this entry from actual evidence')
    return 'fresh' if on < expiry else 'expired'


def put(data, subreddit, record, on=None):
    on = on or today()
    allowed = {'checked_at', 'expires_at', 'fetch_status', 'http_status', 'description',
               'rules_summary', 'source_urls', 'notes', 'was_posted_to'}
    if not isinstance(record, dict) or set(record) - allowed:
        raise ValueError('Store only the documented community summary fields')
    status = record.get('fetch_status', 'ok')
    if status not in ('ok', 'unavailable'):
        raise ValueError('An observation must be ok or unavailable')
    if status == 'unavailable' and record.get('http_status') not in (403, 404):
        raise ValueError('Only observed 403/404 responses are cached as unavailable; never cache 429')
    if status == 'ok' and record.get('http_status', 200) != 200:
        raise ValueError('A failed response is not a successful rule observation')
    checked = date.fromisoformat(record.get('checked_at', on.isoformat()))
    if checked > on:
        raise ValueError('checked_at cannot be in the future')
    if not isinstance(record.get('description', ''), str):
        raise ValueError('description must be text')
    for field in ('rules_summary', 'source_urls', 'notes'):
        values = record.get(field, [])
        if not isinstance(values, list) or not all(isinstance(x, str) for x in values):
            raise ValueError(field + ' must be a list of strings')
    if not record.get('source_urls'):
        raise ValueError('Include the public source URL(s) for the observation')
    if status == 'ok' and not record.get('rules_summary'):
        raise ValueError('Summarize the rules, or explicitly state that none were returned')
    subreddit = name(subreddit)
    old = data['communities'].get(subreddit, {})
    record = dict(record, checked_at=checked.isoformat(), expires_at=expires(checked).isoformat(),
                  fetch_status=status, was_posted_to=bool(old.get('was_posted_to') or record.get('was_posted_to')))
    data['communities'][subreddit] = record
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache-file', type=Path, default=CACHE)
    commands = parser.add_subparsers(dest='command', required=True)
    get = commands.add_parser('get', help='Read selected entries; never fetch or refresh')
    get.add_argument('subreddits', nargs='+')
    listing = commands.add_parser('list', help='Compact inventory, without full rule text')
    listing.add_argument('--posted', action='store_true')
    store = commands.add_parser('put', help='Save one observed summary; expiry is computed automatically')
    store.add_argument('subreddit')
    store.add_argument('--file', type=Path, required=True)
    for command in ('invalidate', 'mark-posted'):
        commands.add_parser(command).add_argument('subreddit')
    args = parser.parse_args()
    data = read_cache(args.cache_file)
    if args.command == 'get':
        output = []
        for sub in dict.fromkeys(map(name, args.subreddits)):
            entry = data['communities'].get(sub)
            output.append({'subreddit': sub, 'cache_state': state(entry), 'entry': entry})
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return int(any(x['cache_state'] != 'fresh' for x in output))
    if args.command == 'list':
        print(json.dumps([{'subreddit': k, 'cache_state': state(v),
                           'fetch_status': v['fetch_status'], 'was_posted_to': v.get('was_posted_to', False)}
                          for k, v in sorted(data['communities'].items())
                          if not args.posted or v.get('was_posted_to')], indent=2))
        return 0
    sub = name(args.subreddit)
    if args.command == 'put':
        put(data, sub, json.loads(args.file.read_text()))
    elif args.command == 'invalidate':
        if sub in data['communities']:
            data['communities'][sub]['expires_at'] = today().isoformat()
    else:
        entry = data['communities'].setdefault(sub, {'fetch_status': 'missing', 'checked_at': None,
                                                     'expires_at': None, 'rules_summary': [], 'source_urls': []})
        entry['was_posted_to'] = True
    write_cache(data, args.cache_file)
    print(json.dumps({'subreddit': sub, 'cache_state': state(data['communities'].get(sub))}))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(2)
