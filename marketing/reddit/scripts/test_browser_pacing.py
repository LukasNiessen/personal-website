import unittest
from unittest.mock import patch
import browser


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

if __name__=='__main__':unittest.main()
