# Example 1: Detect login panels on a single URL
python main.py --url https://example.com --login

# Example 2: Detect login panels on multiple URLs with a proxy
python main.py --file target_urls.txt --login --proxy http://127.0.0.1:8080

# Example 3: Run SQL injection testing on a single URL
python main.py --url https://example.com --sqli
