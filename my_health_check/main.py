import argparse
import yaml
from my_health_check.checker import HealthChecker

def main():
    parser = argparse.ArgumentParser(description="Health check for HTTP endpoints")
    parser.add_argument("config_file", help="Path to YAML configuration file")
    args = parser.parse_args()

    with open(args.config_file, "r") as file:
        config = yaml.safe_load(file)
    
    checker = HealthChecker(config)
    checker.run()

if __name__ == "__main__":
    main()
