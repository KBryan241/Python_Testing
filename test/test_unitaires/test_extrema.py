import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0,str(project_root))

import unittest
from flask import Flask
from unittest.mock import patch
from server import app


class Test_extrema(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_minima(self):
        response = self.client.post('/purchasePlaces',data={'places':'-1'})
        self.assertEqual(response.status_code,400)
    
    def test_maxima(self):
        response = self.client.post('/purchasePlaces',data={'places':'13'})
        self.assertEqual(response.status_code,400)
        
if __name__ == '__main__':
    unittest.main