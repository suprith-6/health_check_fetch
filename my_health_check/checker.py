import requests
import time

class HealthChecker:
    def __init__(self, config):
        self.config = config
        self.domains_status = {}

    def run(self):
        while True:
            for endpoint in self.config:
                self.check_endpoint(endpoint)
            self.log_results()
            time.sleep(15)

    def check_endpoint(self, endpoint):
        url = endpoint['url']
        method = endpoint.get('method', 'GET')
        headers = endpoint.get('headers', {})
        body = endpoint.get('body', None)
        
        try:
            response = requests.request(method, url, headers=headers, json=body, timeout=0.5)
            status = 'UP' if response.status_code in range(200, 300) and response.elapsed.total_seconds() < 0.5 else 'DOWN'
        except requests.exceptions.RequestException:
            status = 'DOWN'
        
        domain = url.split('//')[1].split('/')[0]

        if domain not in self.domains_status:
            self.domains_status[domain] = [0,0]      #{domain: [UP_Count,Total_Count]}

        if(status=="UP"):
            self.domains_status[domain][0]+=1   #UP count
        self.domains_status[domain][1]+=1       #Total Count
    
    def log_results(self):
        for domain, statuses in self.domains_status.items():
            up_count = statuses[0]
            availability = round(100 * up_count / statuses[1])
            print(f"{domain} has {availability}% availability percentage")
        print(self.domains_status)             # for testing the counts
