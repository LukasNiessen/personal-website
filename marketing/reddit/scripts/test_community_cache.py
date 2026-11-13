import copy
from datetime import date
from pathlib import Path
import tempfile
import unittest
from community_cache import expires, name, put, read_cache, state, write_cache


class CacheTests(unittest.TestCase):
    def test_two_calendar_months_and_expiry_boundary(self):
        self.assertEqual(expires(date(2026,12,31)), date(2027,2,28))
        self.assertEqual(expires(date(2023,12,31)), date(2024,2,29))
        entry={'fetch_status':'ok','checked_at':'2026-11-13','expires_at':'2027-01-13'}
        self.assertEqual(state(entry,date(2027,1,12)),'fresh')
        self.assertEqual(state(entry,date(2027,1,13)),'expired')

    def test_normalization_and_missing_observation(self):
        self.assertEqual(name('/r/Angular/'),'angular')
        self.assertEqual(state({'fetch_status':'missing','was_posted_to':True}),'missing')
        with self.assertRaises(ValueError):name('../elsewhere')

    def test_refresh_preserves_posted_history_and_rejects_rate_limit(self):
        data={'schema_version':1,'communities':{'angular':{'was_posted_to':True}}}
        record={'description':'Angular','rules_summary':['No structured rules returned.'],
                'source_urls':['https://www.reddit.com/r/angular/about/rules/']}
        saved=put(data,'r/Angular',record,date(2026,11,13))
        self.assertTrue(saved['was_posted_to'])
        self.assertEqual(saved['expires_at'],'2027-01-13')
        original=copy.deepcopy(data)
        with self.assertRaises(ValueError):
            put(data,'angular',dict(record,fetch_status='unavailable',http_status=429),date(2026,11,14))
        self.assertEqual(data,original)

    def test_unavailable_is_cached_without_becoming_permission(self):
        data={'schema_version':1,'communities':{}}
        entry=put(data,'private',{'fetch_status':'unavailable','http_status':403,
                               'source_urls':['https://www.reddit.com/r/private/about/']},date(2026,11,13))
        self.assertEqual(state(entry,date(2026,11,14)),'fresh')
        self.assertEqual(entry['fetch_status'],'unavailable')

    def test_roundtrip_and_invalid_cache_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'cache.json'
            self.assertEqual(read_cache(path)['communities'],{})
            data={'schema_version':1,'communities':{}}
            write_cache(data,path)
            self.assertEqual(read_cache(path),data)
            path.write_text('{bad')
            with self.assertRaises(ValueError):read_cache(path)
            self.assertEqual(path.read_text(),'{bad')

    def test_future_or_extended_dates_do_not_hit(self):
        with self.assertRaises(ValueError):
            state({'fetch_status':'ok','checked_at':'2026-11-15','expires_at':'2027-01-15'},date(2026,11,14))
        with self.assertRaises(ValueError):
            state({'fetch_status':'ok','checked_at':'2026-11-13','expires_at':'2028-01-13'},date(2026,11,14))

if __name__=='__main__':unittest.main()
