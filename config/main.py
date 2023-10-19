import sys
import time
import logging
import coloredlogs
import click
import subprocess
import socket
from concurrent.futures import ThreadPoolExecutor
from modules import login_detection
from config import settings
from fake_useragent import UserAgent

# Function to check if a port is available
def is_port_available(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", port))
        return True
    except:
        return False
    finally:
        sock.close()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] - %(message)s')
logger = logging.getLogger('my_security_tool')
log_file = 'logs/activity.log'
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
coloredlogs.install(level='DEBUG', logger=logger, fmt='%(asctime)s [%(levelname)s] - %(message)s')

def ban():
    logger.info('Starting the tool...')
    
    # Specify a list of ports to try (e.g., 8080, 8081, 8082, etc.)
    ports_to_try = [8080, 8081, 8082, 8083, 8084]  # You can extend this list
    
    # Find an available port from the list
    for port in ports_to_try:
        if is_port_available(port):
            subprocess.Popen(["mitmdump", "--mode", f"regular@{port}"])
            break
    else:
        logger.error('All specified ports are in use. Please specify a different range of ports.')

def get_login_results(login_urls):
    for url in login_urls:
        print(f"Login panel found: {url}")

@click.command()
@click.option('--url', help='Target URL for testing. Example: https://example.com')
@click.option('--file', help='Path to a file containing a list of target URLs. One URL per line.')
@click.option('--proxy', help='Specify a proxy server for requests. Example: http://127.0.0.1:8080')
@click.option('--login', is_flag=True, help='Detect login panels on target URLs.')
@click.option('--sqli', is_flag=True, help='Run SQL injection testing on target URLs.')
@click.option('-n', '--inputname', help='Customize the username input for SQL injection testing. Default: "username"')
@click.option('-t', '--threads', type=int, help='Number of concurrent threads for testing. Default: 30')
def main(url, file, proxy, login, sqli, inputname, threads):
    """
    My Security Tool - A tool for web security testing.

    Use this tool to perform security tests on web applications. You can detect login panels and perform SQL injection testing.

    Examples:
    1. Detect login panels on a single URL:
       python main.py --url https://example.com --login

    2. Detect login panels on multiple URLs with a proxy:
       python main.py --file target_urls.txt --login --proxy http://127.0.0.1:8080

    3. Run SQL injection testing on a single URL:
       python main.py --url https://example.com --sqli
    """
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
                # Implement SQL injection testing with concurrency
                pass
            else:
                login_urls = executor.map(login_detection.detect_login_panels, [url], [proxy], [{'User-Agent': user_agent}])
                login_urls = [url for sublist in login_urls for url in sublist]
                get_login_results(login_urls)
                # Implement other functionalities with concurrency as needed

    except Exception as e:
        logger.exception(f'An error occurred: {str(e)}')
        sys.exit(1)

if __name__ == '__main__':
    main()
