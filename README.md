# HTTP Endpoint Health Check

A Python-based tool that periodically checks the health of HTTP endpoints and calculates their availability over time. It reads a configuration file in YAML format to define the endpoints, methods, headers, and optional request bodies.

## Features
- **HTTP Health Check**: Supports multiple HTTP methods (e.g., GET, POST).
- **Availability Monitoring**: Logs the availability percentage of each endpoint.
- **Customizable Configuration**: Configured via a YAML file with headers, methods, and request bodies.

## Prerequisites
- Python 3.6 or higher
- `requests` and `PyYAML` libraries

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/suprith-6/health_check_fetch.git
    cd health_check_fetch
    ```

2. Set up a virtual environment (optional but recommended):

    ```bash
    python -m venv my_env
    source my_env/bin/activate  # On Windows: my_env\Scripts\activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -e .
    ```

    or

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Create a configuration YAML file in the `config/` directory that defines the endpoints you want to check. Here's an example `config.yml`:

```yaml
- headers:
    user-agent: fetch-synthetic-monitor
  method: GET
  name: fetch index page
  url: https://fetch.com/
  
- headers:
    user-agent: fetch-synthetic-monitor
  method: GET
  name: fetch careers page
  url: https://fetch.com/careers
  
- body: '{"foo":"bar"}'
  headers:
    content-type: application/json
    user-agent: fetch-synthetic-monitor
  method: POST
  name: fetch some fake post endpoint
  url: https://fetch.com/some/post/endpoint
  
- name: fetch rewards index page
  url: https://www.fetchrewards.com/
```

### YAML Fields:
- `url`: The URL of the endpoint.
- `method`: The HTTP method (defaults to `GET` if not provided).
- `headers`: Optional headers for the request.
- `body`: Optional JSON body for `POST`/`PUT` requests.

## Usage

To run the health checker with your configuration file, execute:

```bash
python my_health_check/main.py config/config.yml
```

The tool will check each endpoint specified in the YAML file, log the result (`UP` or `DOWN`), and calculate the availability percentage after multiple iterations.

### Example Output:

```
fetch.com has 67% availability percentage after 3 checks
www.fetchrewards.com has 100% availability percentage after 1 check
```

### Customization:
The interval between health checks is 5 seconds by default. To modify this interval, change the `time.sleep()` value in the `checker.py` file.

## Development

If you are working on the project and want to make changes while keeping the environment up-to-date, ensure the project is installed in **editable mode** by running:

```bash
pip install -e .
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

