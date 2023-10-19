import sys
import time
import logging
import coloredlogs
import click
import subprocess
import socket
import os
from concurrent.futures import ThreadPoolExecutor
from modules import login_detection
from config import settings
from fake_useragent import UserAgent
import requests

# Define a logger for SQL injection errors
sql_injection_logger = logging.getLogger('sql_injection_errors')
sql_injection_logger.setLevel(logging.ERROR)

# Create a file handler for SQL injection errors
sql_injection_log_file = 'logs/sql_injection_errors.log'
sql_injection_file_handler = logging.FileHandler(sql_injection_log_file)
sql_injection_file_handler.setLevel(logging.ERROR)

# Define the log format for SQL injection errors
sql_injection_formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
sql_injection_file_handler.setFormatter(sql_injection_formatter)

# Add the file handler to the SQL injection logger
sql_injection_logger.addHandler(sql_injection_file_handler)

# Function to check if a port is available
def is_port_available(port):
    # ... (rest of your code)

# Initialize the logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] - %(message)s')
logger = logging.getLogger('my_security_tool')
log_file = 'logs/activity.log'
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
coloredlogs.install(level='DEBUG', logger=logger, fmt='%(asctime)s [%(levelname)s] - %(message)s')

# Rest of your code...

# Function to load SQL payloads from a file
def load_sql_payloads(category, payloads_directory):
    # ... (rest of your code)

# Function to perform SQL injection testing
def perform_sql_injection_test(url, proxy, user_agent, category, payloads_directory):
    try:
        payloads = load_sql_payloads(category, payloads_directory)

        # Create a session for the HTTP requests
        session = requests.Session()

        # Convert the proxy string to a dictionary format
        proxies = {'http': proxy, 'https': proxy} if proxy else None

        # Set headers including the user-agent
        headers = {'User-Agent': user_agent}
        session.headers.update(headers)

        # Send requests with each payload
        for payload in payloads:
            # Construct the request with the payload
            request_url = f"{url}?parameter={payload}"

            # Send the request through the proxy if specified
            if proxies:
                response = session.get(request_url, proxies=proxies, verify=False)
            else:
                response = session.get(request_url, verify=False)

            # Analyze the response to detect SQL injection vulnerabilities
            if "error" in response.text.lower() or "exception" in response.text.lower():
                # SQL injection detected, log it
                sql_injection_logger.warning(f"SQL Injection Detected: {request_url}")

            # You can add more detection criteria based on your application's behavior

    except Exception as e:
        sql_injection_logger.exception(f'Error during SQL injection testing: {str(e)}')

# Main function
@click.command()
@click.option('--url', help='Target URL')
@click.option('--file', help='Target hosts list file')
@click.option('--proxy', help='Proxy (e.g., http://127.0.0.1:8080)')
@click.option('--login', is_flag=True, help='Run only Login panel Detector')
@click.option('--sqli', is_flag=True, help='Run SQL Injection testing')
@click.option('--category', help='SQL Injection payload category (e.g., generic_sql_injection)')
@click.option('-n', '--inputname', help='Customize actual username input for SQLi scan (default "username")')
@click.option('-t', '--threads', type=int, help='Number of threads (default 30)')
def main(url, file, proxy, login, sqli, category, inputname, threads):
    try:
        if not (url or file):
            logger.error('You must specify either --url or --file.')
            return

        if not (login or sqli):
            logger.error('You must specify either --login or --sqli.')
            return

        # Generate a random User-Agent
        user_agent = UserAgent().random

        ban()

        with ThreadPoolExecutor(max_workers=threads) as executor:
            if login:
                login_urls = executor.map(login_detection.detect_login_panels, [url], [proxy], [{'User-Agent': user_agent}])
                login_urls = [url for sublist in login_urls for url in sublist]
                get_login_results(login_urls)
            elif sqli:
                perform_sql_injection_test(url, proxy, user_agent, category, "payloads")
                # Implement SQL injection testing with concurrency
                pass

    except Exception as e:
        logger.exception(f'An error occurred: {str(e)}')
        sys.exit(1)

if __name__ == '__main__':
    main()
