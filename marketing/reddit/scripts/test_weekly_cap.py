import concurrent.futures
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import request_guard as guard


WEEK = 7 * 24 * 60 * 60


class WeeklyCapTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "guard.json"

    def initialize(self, records=None, now=1000):
        result = guard.import_posts(records or [], self.path, now)
        self.assertEqual(result["status"], "imported")

    def weekly(self, subreddit="angular", now=1000):
        return guard.status(self.path, now, subreddit=subreddit)["weekly"]

    def test_posting_requires_history_but_reading_does_not(self):
        result = guard.acquire("post", self.path, 1000, subreddit="angular")
        self.assertEqual(result["reason"], "posting-history-required")
        self.assertEqual(guard.acquire("read", self.path, 1000)["status"], "reserved")
        self.assertFalse(guard.status(self.path, 1000)["history_initialized"])

    def test_posting_requires_an_explicit_community(self):
        self.initialize()
        before = self.path.read_bytes()
        with self.assertRaises(ValueError):
            guard.acquire("post", self.path, 1000)
        self.assertEqual(before, self.path.read_bytes())

    def test_third_post_is_blocked_and_community_case_is_normalized(self):
        self.initialize()
        first = guard.acquire("post", self.path, 1000, subreddit="Angular")
        second = guard.acquire("post", self.path, 1120, subreddit="r/angular")
        self.assertEqual(first["status"], "reserved")
        self.assertEqual(second["status"], "reserved")
        self.assertNotEqual(first["reservation_id"], second["reservation_id"])
        before = self.path.read_bytes()
        result = guard.acquire("post", self.path, 1240, subreddit="ANGULAR")
        self.assertEqual(result["reason"], "subreddit-weekly-cap")
        self.assertEqual(result["next_available_at"], 1000 + WEEK)
        self.assertEqual(result["wait_seconds"], 1000 + WEEK - 1240)
        self.assertEqual(before, self.path.read_bytes())
        self.assertEqual(self.weekly(now=1240), {
            "subreddit": "angular", "limit": 2, "count": 2,
            "remaining": 0, "next_available_at": 1000 + WEEK,
        })

    def test_other_community_keeps_its_own_capacity(self):
        self.initialize([
            {"id": "t3_first", "subreddit": "angular", "created_at": 900},
            {"id": "t3_second", "subreddit": "angular", "created_at": 950},
        ])
        self.assertEqual(
            guard.acquire("post", self.path, 1000, subreddit="django")["status"],
            "reserved",
        )
        self.assertEqual(self.weekly("angular")["remaining"], 0)
        self.assertEqual(self.weekly("django")["remaining"], 1)

    def test_window_is_rolling_and_excludes_exact_seven_day_boundary(self):
        self.initialize([
            {"id": "t3_first", "subreddit": "angular", "created_at": 1000},
            {"id": "t3_second", "subreddit": "angular", "created_at": 1120},
        ], now=1120)
        self.assertEqual(
            guard.acquire("post", self.path, 1000 + WEEK - 1, subreddit="angular")["reason"],
            "subreddit-weekly-cap",
        )
        result = guard.acquire("post", self.path, 1000 + WEEK, subreddit="angular")
        self.assertEqual(result["status"], "reserved")
        self.assertEqual(self.weekly(now=1000 + WEEK)["count"], 2)
        self.assertEqual(self.weekly(now=1000 + WEEK)["next_available_at"], 1120 + WEEK)

    def test_pacing_denial_does_not_consume_weekly_capacity(self):
        self.initialize()
        guard.acquire("post", self.path, 1000, subreddit="angular")
        before = self.path.read_bytes()
        self.assertEqual(
            guard.acquire("post", self.path, 1010, subreddit="angular")["reason"],
            "action-spacing",
        )
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(self.weekly(now=1010)["count"], 1)

    def test_uncertain_reservation_stays_counted_across_instances(self):
        self.initialize()
        guard.acquire("post", self.path, 1000, subreddit="angular")
        # A timeout or unknown result has no cancellation/confirmation call.
        other_path_object = Path(str(self.path))
        guard.acquire("post", other_path_object, 1120, subreddit="angular")
        result = guard.acquire("post", other_path_object, 1240, subreddit="angular")
        self.assertEqual(result["reason"], "subreddit-weekly-cap")

    def test_explicit_cancellation_releases_only_pending_slot_and_keeps_pacing(self):
        self.initialize([
            {"id": "t3_published", "subreddit": "angular", "created_at": 900},
        ])
        reserved = guard.acquire("post", self.path, 1000, subreddit="angular")
        guard.cancel_post(reserved["reservation_id"], "Visible validation rejected submission", self.path)
        self.assertEqual(self.weekly(now=1001)["count"], 1)
        self.assertEqual(guard.status(self.path, 1001)["last_post_at"], 1000)
        self.assertEqual(
            guard.acquire("post", self.path, 1001, subreddit="angular")["reason"],
            "action-spacing",
        )
        with self.assertRaises(ValueError):
            guard.cancel_post("t3_published", "Removed by moderator", self.path)
        self.assertEqual(self.weekly(now=1120)["count"], 1)

    def test_confirmation_uses_actual_creation_time_without_double_counting(self):
        self.initialize()
        reserved = guard.acquire("post", self.path, 1000, subreddit="angular")
        guard.confirm_post(reserved["reservation_id"], "t3_actual", 1002, self.path, 1003)
        self.assertEqual(self.weekly(now=1003)["count"], 1)
        self.assertEqual(self.weekly(now=1000 + WEEK)["count"], 1)
        self.assertEqual(self.weekly(now=1002 + WEEK)["count"], 0)

    def test_repeated_imports_union_existing_history_and_are_idempotent(self):
        first = {"id": "t3_first", "subreddit": "angular", "created_at": 900}
        second = {"id": "t3_second", "subreddit": "angular", "created_at": 950}
        self.initialize([first])
        guard.import_posts([first, second], self.path, 1000)
        guard.import_posts([first], self.path, 1000)
        guard.import_posts([], self.path, 1000)
        self.assertEqual(self.weekly()["count"], 2)

    def test_confirmation_and_profile_import_do_not_duplicate_published_id(self):
        self.initialize()
        reserved = guard.acquire("post", self.path, 1000, subreddit="angular")
        guard.confirm_post(reserved["reservation_id"], "t3_actual", 1002, self.path, 1003)
        guard.import_posts([
            {"id": "t3_actual", "subreddit": "angular", "created_at": 1002},
        ], self.path, 1010)
        self.assertEqual(self.weekly(now=1010)["count"], 1)

    def test_profile_import_before_confirmation_reconciles_the_reservation(self):
        self.initialize()
        reserved = guard.acquire("post", self.path, 1000, subreddit="angular")
        guard.import_posts([
            {"id": "t3_actual", "subreddit": "angular", "created_at": 1002},
        ], self.path, 1010)
        guard.confirm_post(reserved["reservation_id"], "t3_actual", 1002, self.path, 1010)
        self.assertEqual(self.weekly(now=1010)["count"], 1)

    def test_concurrent_campaigns_cannot_reserve_more_than_two_slots(self):
        self.initialize()
        with patch.object(guard, "ACTION_INTERVAL", 0), patch.object(guard, "POST_INTERVAL", 0):
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                results = list(pool.map(
                    lambda _: guard.acquire("post", self.path, 1000, subreddit="angular"),
                    range(8),
                ))
        self.assertEqual(sum(r["status"] == "reserved" for r in results), 2)
        self.assertEqual(sum(r.get("reason") == "subreddit-weekly-cap" for r in results), 6)
        self.assertEqual(self.weekly()["count"], 2)

    def test_legacy_migration_preserves_existing_cooldown_and_pacing(self):
        self.path.write_text(json.dumps({
            "schema_version": 1, "last_action_at": 1000, "last_post_at": 990,
            "blocked_until": 1120, "probe_required": True, "probe_pending": False,
        }))
        self.initialize(now=1010)
        current = guard.status(self.path, 1010)
        self.assertTrue(current["history_initialized"])
        self.assertEqual(current["last_action_at"], 1000)
        self.assertEqual(current["last_post_at"], 990)
        self.assertEqual(current["blocked_until"], 1120)
        self.assertTrue(current["probe_required"])
        self.assertEqual(
            guard.acquire("post", self.path, 1010, subreddit="angular")["reason"],
            "rate-limit",
        )

    def test_corrupt_history_fails_closed_without_overwriting_it(self):
        self.initialize()
        current = json.loads(self.path.read_text())
        current["posts"] = []
        self.path.write_text(json.dumps(current))
        before = self.path.read_bytes()
        with self.assertRaises(ValueError):
            guard.acquire("post", self.path, 1000, subreddit="angular")
        with self.assertRaises(ValueError):
            guard.import_posts([], self.path, 1000)
        self.assertEqual(before, self.path.read_bytes())


if __name__ == "__main__":
    unittest.main()
