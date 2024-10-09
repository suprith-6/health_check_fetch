import unittest
from unittest.mock import AsyncMock, patch
import asyncio
from my_health_check.checker import HealthChecker

class TestHealthChecker(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.config = [{'url': 'https://example.com', 'method': 'GET'}]
        self.health_checker = HealthChecker(self.config)
    
    # Test case: Endpoint returns 404 status, meaning it's considered DOWN
    @patch('my_health_check.checker.aiohttp.ClientSession')
    async def test_001_endpoint_down_when_status_404(self, mock_client_session):
        mock_response = AsyncMock()
        mock_response.status = 404
        
        mock_session = mock_client_session.return_value
        mock_session.__aenter__.return_value = mock_session
        mock_session.request.return_value.__aenter__.return_value = mock_response

        await self.health_checker.check_endpoint(self.config[0])

        domain = 'example.com'
        self.assertIn(domain, self.health_checker.domains_status, 
                      f"Domain {domain} should be in domains_status")
        self.assertEqual(self.health_checker.domains_status[domain], [0, 1], 
                         f"Expected status [0, 1] for {domain}, but got {self.health_checker.domains_status[domain]}")

    # Test case: Endpoint responds within 0.5 seconds and has a 200 status (success), so it's considered UP
    @patch('time.monotonic')
    @patch('my_health_check.checker.aiohttp.ClientSession')
    async def test_002_endpoint_up_when_response_time_less_than_0_5(self, mock_client_session, mock_time):
        mock_response = AsyncMock()
        mock_response.status = 200
        
        mock_session = mock_client_session.return_value
        mock_session.__aenter__.return_value = mock_session
        mock_session.request.return_value.__aenter__.return_value = mock_response

        mock_time.side_effect = [0, 0.3]

        await self.health_checker.check_endpoint(self.config[0])

        domain = 'example.com'
        self.assertIn(domain, self.health_checker.domains_status, 
                      f"Domain {domain} should be in domains_status")
        self.assertEqual(self.health_checker.domains_status[domain], [1, 1], 
                         f"Expected status [1, 1] for {domain}, but got {self.health_checker.domains_status[domain]}")


    # Test case: Endpoint responds in more than 0.5 seconds, so it should be considered DOWN
    @patch('time.monotonic')
    @patch('my_health_check.checker.aiohttp.ClientSession')
    async def test_003_endpoint_down_when_response_time_greater_than_0_5(self, mock_client_session, mock_time):
        mock_response = AsyncMock()
        mock_response.status = 200
        
        mock_session = mock_client_session.return_value
        mock_session.__aenter__.return_value = mock_session
        mock_session.request.return_value.__aenter__.return_value = mock_response

        mock_time.side_effect = [0, 0.6]

        await self.health_checker.check_endpoint(self.config[0])

        domain = 'example.com'
        self.assertIn(domain, self.health_checker.domains_status, 
                      f"Domain {domain} should be in domains_status")
        self.assertEqual(self.health_checker.domains_status[domain], [0, 1], 
                         f"Expected status [0, 1] for {domain}, but got {self.health_checker.domains_status[domain]}")

    # Test case: Endpoint returns a connection error (Timeout), so it should be considered DOWN
    @patch('my_health_check.checker.aiohttp.ClientSession')
    async def test_004_endpoint_down_on_connection_error(self, mock_client_session):
        mock_session = mock_client_session.return_value
        mock_session.__aenter__.return_value = mock_session
        mock_session.request.side_effect = asyncio.TimeoutError()

        await self.health_checker.check_endpoint(self.config[0])

        domain = 'example.com'
        self.assertIn(domain, self.health_checker.domains_status, 
                      f"Domain {domain} should be in domains_status")
        self.assertEqual(self.health_checker.domains_status[domain], [0, 1], 
                         f"Expected status [0, 1] for {domain}, but got {self.health_checker.domains_status[domain]}")

   
if __name__ == '__main__':
    unittest.main(exit=False)