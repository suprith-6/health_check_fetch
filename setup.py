from setuptools import setup, find_packages

setup(
    name="my_health_check",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "PyYAML",
        "aiohttp",
    ],
    entry_points={
        'console_scripts': [
            'health-check=my_health_check.main:main',
        ],
    },
    description="A simple package to check HTTP endpoint health",
    author="Suprith",
    author_email="suprithkp.007@gmil.com",
    url="https://github.com/suprith-6/health_check_fetch.git",
)