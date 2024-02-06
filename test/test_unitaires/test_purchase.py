import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0,str(project_root))

import unittest
from flask import Flask,render_template,request,redirect,flash,url_for
from unittest.mock import patch
from server import app,purchasePlaces,clubs as c,competitions as comp 


class Test_purchased_place(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        app.config['TESTING']= True
        self.client= app.test_client()


    def test_with_not_enough_point(self):
        response = self.client.post('/purchasePlaces',data={'places':'250'},follow_redirects=True)
        self.assertEqual(response.status_code,400)

    
    def test_insuficiant_Places(self):
        data = {
            'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '25'
        }
        with self.app.test_request_context():
            response = self.client.post('/purchasePlaces', data=data,)
            self.assertEqual(response.status_code,302)

    def test_purchase_places_success(self):
        # Set up the request data
        request_data = { 'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '3'
            }
        response = self.client.post('/purchasePlaces', data=request_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Great-booking complete!',response.data)
if __name__ == '__main__':
    unittest.main
