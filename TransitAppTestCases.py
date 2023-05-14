import requests
import unittest


class TransitAppTestCases(unittest.TestCase):

    def test_1_getAPI(self):
        url = "http://127.0.0.1:5000/"

        
        # A GET  request to the API
        response = requests.get(url)
        # Print the response
        
        print(response.text)
        
        # Test case result
        self.assertEqual(True, response.text!=None)  
            
    def test_2_getAPI(self):
        url = "http://127.0.0.1:5000/get_all_trip_details/347461003"

        
        # A GET  request to the API
        response = requests.get(url)
        # Print the response
        
        print(response.text)
        
        # Test case result
        self.assertEqual(True, response.text!=None)  
 

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TransitAppTestCases)
    testResult = unittest.TextTestRunner(verbosity=2).run(suite)
