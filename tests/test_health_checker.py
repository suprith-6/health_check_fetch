import unittest
from unittest.mock import AsyncMock, patch
import asyncio
import time
from my_health_check.checker import HealthChecker

class TestHealthChecker(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.config = [{'url': 'https://example.com', 'method': 'GET'}]
        self.health_checker = HealthChecker(self.config)

    @patch('my_health_check.checker.aiohttp.ClientSession')
    async def test_status_code_outside_200_300(self, mock_client_session):
        # Mocking an async response with a 404 status
        mock_response = AsyncMock()
        mock_response.status = 404

        print(type(mock_response))

        # Correctly mock the async context manager
        
        mock_session = mock_client_session.return_value
        mock_session.__aenter__.return_value = mock_session #telling which session to use
        mock_session.request.return_value = mock_response
        # mock_response object is returned by the mocked session.request() call, in this async with block

        # Call the function and await the result
        await self.health_checker.check_endpoint(self.config[0])

        # Assert that the endpoint is marked as DOWN
        domain = 'example.com'
        self.assertIn(domain, self.health_checker.domains_status)
        self.assertEqual(self.health_checker.domains_status[domain], [0, 1])

    @patch('my_health_check.checker.aiohttp.ClientSession')
    @patch('time.monotonic') 
    async def test_response_time_less_than_0_5(self, mock_client_session, mock_time):
        # Mocking an async response with a 200 status
        mock_response = AsyncMock()
        mock_response.status = 200
        
        # Correctly mock the async context manager
        
        mock_session = mock_client_session.return_value
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None
        mock_session.request.return_value.__aenter__.return_value = mock_response

        # Mock start and end time to simulate response time less than 0.5 seconds
        # mock_start_time = time.monotonic()
        # with patch('time.monotonic', side_effect=[mock_start_time, mock_start_time + 0.3]):
        #     await self.health_checker.check_endpoint(self.config[0])
        mock_time.side_effect = [0, 0.3]
        

        await self.health_checker.check_endpoint(self.config[0])
        print(mock_response)

        # Assert that the endpoint is marked as UP
        domain = 'example.com'
        self.assertIn(domain, self.health_checker.domains_status)
        # Expecting [1, 1] since it's UP and only one request was made
        self.assertEqual(self.health_checker.domains_status[domain], [1, 1])


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False, defaultTest="TestHealthChecker.test_response_time_less_than_0_5")
