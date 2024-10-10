import requests
import time
import asyncio
import aiohttp
import logging 
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,  
    datefmt="%Y-%m-%d %H:%M:%S"
)

class HealthChecker:
    def __init__(self, config):
        self.config = config
        self.domains_status = {}
        self.lock=asyncio.Lock()

    async def run(self):
        while True:
            start_time = time.monotonic()
            tasks=[self.check_endpoint(endpoint) for endpoint in self.config]
            await asyncio.gather(*tasks)
            self.log_results()
            elapsed_time = time.monotonic() - start_time
            # Ensure the next cycle starts exactly after 15 seconds
            if elapsed_time < 15:
                await asyncio.sleep(15 - elapsed_time)
            else:
                logging.warning(f"Health checks took {elapsed_time} seconds, skipping sleep")
                await asyncio.sleep(elapsed_time)

    async def check_endpoint(self, endpoint):
        url = endpoint['url']
        method = endpoint.get('method', 'GET')  # Default to 'GET' if no HTTP method is specified in the YAML configuration
        headers = endpoint.get('headers', {})
        body = endpoint.get('body', None)
        
        try:
            start_time = time.monotonic()
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, headers=headers, json=body, timeout=0.5) as response:
                    end_time = time.monotonic()
                    elapsed_time = end_time - start_time
                    status = 'UP' if response.status in range(200, 300) and elapsed_time < 0.5 else 'DOWN'
                    logging.info(f"{url} - Status: {status}, Response Time: {elapsed_time:.2f} seconds")
        except asyncio.TimeoutError:
            status = 'DOWN'
            logging.error(f"{url} - Status: DOWN due to Timeout")
        except aiohttp.ClientError as e:
            status = 'DOWN'
            logging.error(f"{url} - ClientError: {e}")
        except Exception as e:
            status = 'DOWN'
            print(e)
 
        domain = url.split('//')[1].split('/')[0]

        async with self.lock:
            if domain not in self.domains_status:
                self.domains_status[domain] = [0,0]      #{domain: [UP_Count,Total_Count]}

            if(status=="UP"):
                self.domains_status[domain][0]+=1   #UP count
            self.domains_status[domain][1]+=1       #Total Count
    
    def log_results(self):
        for domain, statuses in self.domains_status.items():
            up_count = statuses[0]
            availability = round(100 * up_count / statuses[1])
            logging.info(f"{domain} - Availability: {availability}% ({up_count}/{statuses[1]})")
        
