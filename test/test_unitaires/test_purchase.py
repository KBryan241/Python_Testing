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
# class TestPurchasePlaces(unittest.TestCase):

#     def setUp(self):
#         app.config['TESTING'] = True
#         self.client = app.test_client()
#         self.competitions = comp
#         self.clubs = c

#     def test_purchasePlaces_success(self):
#         # Arrange
#         data = {
#             'competition': 'Competition 1',
#             'club': 'Club 1',
#             'places': '5'
#         }
#         expected_message = 'Great-booking complete!'

#         # Act
#         response = self.client.post('/purchasePlaces', data=data, follow_redirects=True)
#         actual_message = session.get('message', None)

#         # Assert
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(expected_message, actual_message)
#         self.assertEqual(self.competitions[0]['numberOfPlaces'], 5)
#         self.assertEqual(self.clubs[0]['points'], 45)

#     def test_purchasePlaces_not_enough_points(self):
#         # Arrange
#         data = {
#             'competition': 'Competition 1',
#             'club': 'Club 2',
#             'places': '15'
#         }
#         expected_message = 'Your points is not enough'

#         # Act
#         response = self.client.post('/purchasePlaces', data=data, follow_redirects=True)
#         actual_message = session.get('message', None)

#         # Assert
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(expected_message, actual_message)
#         self.assertEqual(self.competitions[0]['numberOfPlaces'], 10)
#         self.assertEqual(self.clubs[1]['points'], 30)

#     def test_purchasePlaces_no_places_available(self):
#         # Arrange
#         data = {
#             'competition': 'Competition 1',
#             'club': 'Club 1',
#             'places': '15'
#         }
#         expected_message = 'No place available for this competition'

#         # Act
#         response = self.client.post('/purchasePlaces', data=data, follow_redirects=True)
#         actual_message = session.get('message', None)

#         # Assert
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(expected_message, actual_message)
#         self.assertEqual(self.competitions[0]['numberOfPlaces'], 10)
#         self.assertEqual(self.clubs[0]['points'], 50)

# if __name__ == '__main__':
#     unittest.main()