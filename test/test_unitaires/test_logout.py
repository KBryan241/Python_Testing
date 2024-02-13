import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0,str(project_root))

import unittest
from server import app,logout
from flask import Flask, url_for, session

class TestLogout(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_logout_redirects_to_index(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
