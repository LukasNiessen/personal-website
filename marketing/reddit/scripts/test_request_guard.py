import concurrent.futures
from datetime import datetime, timezone
from email.utils import format_datetime
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import request_guard as guard


class RequestGuardTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "guard.json"

    def test_reads_are_spaced_without_mutating_denied_state(self):
        self.assertEqual(guard.acquire("read", self.path, 1000)["status"], "reserved")
        before = self.path.read_bytes()
        self.assertEqual(guard.acquire("read", self.path, 1001), {
            "status": "wait", "reason": "action-spacing", "wait_seconds": 14,
        })
        self.assertEqual(before, self.path.read_bytes())
        self.assertEqual(guard.acquire("read", self.path, 1015)["status"], "reserved")

    def test_post_spacing_survives_intervening_reads(self):
        self.assertEqual(guard.acquire("post", self.path, 1000)["status"], "reserved")
        self.assertEqual(guard.acquire("read", self.path, 1015)["status"], "reserved")
        self.assertEqual(guard.acquire("post", self.path, 1030)["wait_seconds"], 90)
        self.assertEqual(guard.acquire("post", self.path, 1120)["status"], "reserved")
        self.assertEqual(guard.acquire("read", self.path, 1121)["wait_seconds"], 14)

    def test_cooldown_permits_only_one_read_probe_until_confirmed(self):
        guard.rate_limit("30", self.path, 1000)
        for kind in ("read", "post"):
            self.assertEqual(guard.acquire(kind, self.path, 1020)["wait_seconds"], 10)
        self.assertEqual(guard.acquire("post", self.path, 1030)["reason"], "read-only-probe-required")
        self.assertTrue(guard.acquire("read", self.path, 1030)["probe"])
        for kind in ("read", "post"):
            self.assertEqual(guard.acquire(kind, self.path, 1100)["reason"], "probe-result-required")
        guard.probe_ok(self.path)
        self.assertEqual(guard.acquire("post", self.path, 1100)["status"], "reserved")

    def test_retry_after_seconds_http_date_and_invalid_fallback(self):
        now = datetime(2026, 11, 14, tzinfo=timezone.utc).timestamp()
        date = format_datetime(datetime.fromtimestamp(now + 45, timezone.utc), usegmt=True)
        self.assertEqual(guard.retry_deadline(date, now), now + 45)
        self.assertEqual(guard.retry_deadline("30", now), now + 30)
        self.assertEqual(guard.retry_deadline("0", now), now)
        for invalid in (None, "", "bad", "-30", "NaN", "1.5"):
            with self.subTest(value=invalid):
                self.assertEqual(guard.retry_deadline(invalid, now), now + 900)

    def test_shared_cooldown_is_never_shortened(self):
        guard.rate_limit("120", self.path, 1000)
        guard.rate_limit("20", self.path, 1010)
        self.assertEqual(guard.status(Path(str(self.path)), 1020)["blocked_until"], 1120)
        self.assertEqual(guard.acquire("read", self.path, 1020)["wait_seconds"], 100)

    def test_failed_probe_remains_blocked_or_starts_new_cooldown(self):
        guard.rate_limit("30", self.path, 1000)
        guard.acquire("read", self.path, 1030)
        # An error such as HTTP 403 must not call probe_ok.
        self.assertEqual(guard.acquire("post", self.path, 1200)["status"], "blocked")
        # A repeated HTTP 429 instead records another cooldown.
        guard.rate_limit(None, self.path, 1031)
        self.assertFalse(guard.status(self.path, 1032)["probe_pending"])
        self.assertEqual(guard.acquire("read", self.path, 1032)["wait_seconds"], 899)
        with self.assertRaises(ValueError):
            guard.probe_ok(self.path)

    def test_status_missing_state_is_read_only(self):
        self.assertEqual(guard.status(self.path, 1000)["status"], "ready")
        self.assertEqual(list(self.path.parent.iterdir()), [])

    def test_malformed_state_fails_closed_and_is_preserved(self):
        for malformed in (b"broken json", b"{}", b'{"schema_version": 2}'):
            with self.subTest(state=malformed):
                self.path.write_bytes(malformed)
                with self.assertRaises(ValueError):
                    guard.acquire("read", self.path, 1000)
                with self.assertRaises(ValueError):
                    guard.rate_limit("30", self.path, 1000)
                self.assertEqual(self.path.read_bytes(), malformed)

    def test_invalid_state_timestamps_and_probe_flags_fail_closed(self):
        for value in (float("nan"), True, -1):
            state = guard.empty_state()
            state["last_action_at"] = value
            self.path.write_text(json.dumps(state))
            with self.assertRaises(ValueError):
                guard.acquire("read", self.path, 1000)
        state = guard.empty_state()
        state["probe_pending"] = True
        self.path.write_text(json.dumps(state))
        with self.assertRaises(ValueError):
            guard.acquire("read", self.path, 1000)

    def test_concurrent_callers_share_a_single_reserved_slot(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(lambda _: guard.acquire("read", self.path, 1000), range(6)))
        self.assertEqual(sum(result["status"] == "reserved" for result in results), 1)
        self.assertEqual(sum(result["status"] == "wait" for result in results), 5)

    def test_cli_denials_have_nonzero_exit_and_no_request(self):
        command = [sys.executable, str(Path(guard.__file__)), "--state-file", str(self.path), "acquire", "--kind", "read"]
        first = subprocess.run(command, capture_output=True, text=True, check=False)
        second = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 2, second.stderr)
        self.assertEqual(json.loads(second.stdout)["status"], "wait")


if __name__ == "__main__":
    unittest.main()
