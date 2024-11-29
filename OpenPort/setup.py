from setuptools import setup, find_packages

setup(
    name='OpenPort',  # Name of the package
    version='0.1',  # Version of the package
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        'scapy',  # Required dependency for ARP scanning
    ],
    entry_points={
        'console_scripts': [
            'port-scanner=PortScanner:main',  # Entry point for the command-line interface
        ],
    },
    description='A simple Python port scanner that discovers live hosts in a subnet and scans for open ports.',
    author='Your Name',  # Replace with your name
    author_email='your.email@example.com',  # Replace with your email
    url='https://github.com/RonakSharma11/PortScanner',  # Replace with your GitHub repository URL
)