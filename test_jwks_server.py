import unittest #USED TO RUN CODE
from jwks_server import app #used for Flask app
class JWKSAuthTest(unittest.TestCase): #Test case
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    def test_jwks_endpoint(self): #testing endpoints
        response = self.app.get('/jwks')
        self.assertEqual(response.status_code, 200)
    def test_auth_endpoint(self): #sends a POST request to the endpoint
        response = self.app.post('/auth')
        self.assertEqual(response._status_code, 200)
        data = response.get_json() # assign JSON to a data variable
        self.assertIn('token', data) #make sure token is present
if __name__ == '__main__':
    unittest.main()
