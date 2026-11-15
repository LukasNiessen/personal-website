import unittest
from unittest.mock import patch
from contextlib import redirect_stderr
import io
from pathlib import Path
import tempfile
import browser
import request_guard as guard


class BrowserPacingTests(unittest.TestCase):
    def test_denied_slot_never_opens_browser(self):
        with patch('browser.request_guard.acquire', return_value={'status':'wait','wait_seconds':15}), patch('browser.run') as run:
            with self.assertRaises(RuntimeError):browser.open_tab('https://www.reddit.com/')
            run.assert_not_called()

    def test_granted_navigation_uses_one_slot(self):
        with patch('browser.request_guard.acquire', return_value={'status':'reserved'}) as acquire, patch('browser.run',return_value='123:456'):
            self.assertEqual(browser.open_tab('https://www.reddit.com/'),{'window_id':123,'tab_id':456})
            acquire.assert_called_once_with('read')

    def test_local_blank_probe_does_not_consume_network_slot(self):
        with patch('browser.request_guard.acquire') as acquire, patch('browser.run',return_value='123:456'):
            browser.open_tab('about:blank')
            acquire.assert_not_called()

    def test_post_without_subreddit_never_reserves_or_executes(self):
        args = ['eval', '--window-id', '123', '--tab-id', '456', '--expect-url',
                'https://old.reddit.com/r/angular/submit', '--js-file', '/nonexistent',
                '--network-kind', 'post']
        with redirect_stderr(io.StringIO()), patch('browser.request_guard.acquire') as acquire, patch('browser.evaluate') as execute:
            with self.assertRaises(SystemExit) as error:
                browser.main(args)
            self.assertEqual(error.exception.code, 2)
            acquire.assert_not_called()
            execute.assert_not_called()

    def test_mismatched_subreddit_never_reserves_or_executes(self):
        for url in ['https://old.reddit.com/r/angular/submit',
                    'https://www.reddit.com/submit?sr=angular']:
            with self.subTest(url=url), patch('browser.request_guard.acquire') as acquire, patch('browser.evaluate') as execute:
                with self.assertRaisesRegex(ValueError, 'Subreddit differs'):
                    browser.main(['eval', '--window-id', '123', '--tab-id', '456',
                                  '--expect-url', url, '--js-file', '/nonexistent',
                                  '--network-kind', 'post', '--subreddit', 'django'])
                acquire.assert_not_called()
                execute.assert_not_called()

    def test_weekly_denial_blocks_browser_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'guard.json'
            js = Path(directory) / 'submit.js'
            js.write_text('document.querySelector("button").click()')
            guard.import_posts([
                {'id': 't3_first', 'subreddit': 'angular', 'created_at': 900},
                {'id': 't3_second', 'subreddit': 'angular', 'created_at': 950},
            ], path, 1000)
            real_acquire = guard.acquire
            with patch('browser.request_guard.acquire', side_effect=lambda kind, **kw: real_acquire(kind, path, 1000, **kw)), patch('browser.evaluate') as execute:
                with self.assertRaisesRegex(RuntimeError, 'subreddit-weekly-cap'):
                    browser.main(['eval', '--window-id', '123', '--tab-id', '456',
                                  '--expect-url', 'https://old.reddit.com/r/angular/submit',
                                  '--js-file', str(js), '--network-kind', 'post', '--subreddit', 'Angular'])
                execute.assert_not_called()

    def test_timeout_keeps_reservation_and_exposes_its_id(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'guard.json'
            js = Path(directory) / 'submit.js'
            js.write_text('document.querySelector("button").click()')
            guard.import_posts([], path, 1000)
            real_acquire = guard.acquire
            stderr = io.StringIO()
            with redirect_stderr(stderr), patch('browser.request_guard.acquire', side_effect=lambda kind, **kw: real_acquire(kind, path, 1000, **kw)), patch('browser.evaluate', side_effect=RuntimeError('timeout')):
                with self.assertRaisesRegex(RuntimeError, 'timeout'):
                    browser.main(['eval', '--window-id', '123', '--tab-id', '456',
                                  '--expect-url', 'https://old.reddit.com/r/angular/submit',
                                  '--js-file', str(js), '--network-kind', 'post', '--subreddit', 'Angular'])
            state = guard.status(path, 1001, subreddit='angular')
            self.assertEqual(state['weekly']['count'], 1)
            pending = next(iter(state['pending_reservations']))
            self.assertIn(pending, stderr.getvalue())

if __name__=='__main__':unittest.main()
