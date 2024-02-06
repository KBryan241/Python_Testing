import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0,str(project_root))

import unittest
from flask import Flask
from server import app

class Test_connnexion(unittest.TestCase):
    def tearDown(self):
        pass

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_with_valid_email(self):
        response = self.client.post('/showSummary',data={'email':'admin@irontemple.com'})
        self.assertEqual(response.status_code,200)
    
    def test_with_no_email(self):
        response = self.client.post('/showSummary',data={'email':''})
        self.assertIn(b'Enter a valid email please',response.data)
        self.assertEqual(response.status_code,200)
    
    def test_with_invalid_email(self):
        response = self.client.post('/showSummary',data={'email':'email@email.com'})
        self.assertIn(b'No clubs exist for this email',response.data)
        self.assertEqual(response.status_code,200)

if __name__ == '__main__':
    unittest.main