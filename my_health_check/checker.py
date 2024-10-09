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
    level=logging.INFO,  # Set the default log level to INFO
    datefmt="%Y-%m-%d %H:%M:%S"
)

class HealthChecker:
    def __init__(self, config):
        self.config = config
        self.domains_status = {}
        self.lock=asyncio.Lock()

    async def run(self):
        while True:
            tasks=[self.check_endpoint(endpoint) for endpoint in self.config]
            # duration_start=time.monotonic()
            await asyncio.gather(*tasks)
            self.log_results()
            #duration_end=time.monotonic()
            # await asyncio.sleep(15-(duration_start-duration_end))
            await asyncio.sleep(15)

    async def check_endpoint(self, endpoint):
        url = endpoint['url']
        method = endpoint.get('method', 'GET')
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
        except:
            print(e)
        # except OSError as e:
        #     logging.error(f"OS-level error occurred: {e}")

        
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
            #print(f"{domain} has {availability}% availability percentage")
            logging.info(f"{domain} - Availability: {availability}% ({up_count}/{statuses[1]})")
        #print(self.domains_status)             # for testing the counts
