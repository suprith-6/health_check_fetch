import argparse
import asyncio
import yaml
from my_health_check.checker import HealthChecker

async def main():
    parser = argparse.ArgumentParser(description="Health check for HTTP endpoints")
    parser.add_argument("config_file", help="Path to YAML configuration file")
    args = parser.parse_args()

    with open(args.config_file, "r") as file:
        config = yaml.safe_load(file)
    
    checker = HealthChecker(config)
    await checker.run()

if __name__ == "__main__":
    asyncio.run(main())
