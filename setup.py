# setup.py
from setuptools import setup, find_packages

setup(
    name="productivity-dashboard",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "productivity-dashboard=productivity_dashboard.dashboard:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A command-line productivity dashboard with tasks, weather, crypto prices, and focus timer",
    keywords="productivity cli dashboard tasks weather crypto",
)