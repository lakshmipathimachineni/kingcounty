import unittest
import requests

class TestBusTransportBackend(unittest.TestCase):
    
    def test_get_stop_by_name(self):
        # Make a GET request to the API endpoint to get a stop by name
        response = requests.get('http://localhost:5000/stops?name=Bellevue Transit Center')
        print(response.content) # Print the response content
        
        # Assert that the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)
        
        # Assert that the response data is correct
        expected_data = {'stop_id': 1234, 'stop_name': 'Bellevue Transit Center', 'stop_lat': 47.6141, 'stop_lon': -122.192}
        self.assertEqual(response.json(), expected_data)
        
    def test_get_routes_by_stop(self):
        # Make a GET request to the API endpoint to get routes by stop ID
        response = requests.get('http://localhost:5000/routes?stop_id=1234')
        print(response.content) # Print the response content
        
        # Assert that the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)
        
        # Assert that the response data is correct
        expected_data = [{'route_id': 1, 'route_short_name': '101', 'route_desc': 'Bellevue to Seattle'}, {'route_id': 2, 'route_short_name': 'B', 'route_desc': 'Bellevue to Kirkland'}]
        self.assertEqual(response.json(), expected_data)
