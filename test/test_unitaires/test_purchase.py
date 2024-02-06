import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0,str(project_root))

import unittest
from flask import Flask
from unittest.mock import patch
from server import app


class Test_purchased_place(unittest.TestCase):
    def setUp(self):
        self.client= app.test_client()


    def test_with_no_value(self):
        response = self.client.post('/purchasePlaces',data={'places':''})
        self.assertEqual(response.status_code,400)

    def test_with_not_enough_point(self):
        response = self.client.post('/purchasePlaces',data={'places':'250'})
        self.assertEqual(response.status_code,400)

if __name__ == '__main__':
    unittest.main