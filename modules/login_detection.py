import requests
from bs4 import BeautifulSoup
import re
from termcolor import colored
from config import settings

def detect_login_panels(urls, proxies, useragent):
    login_urls = []

    for url in urls:
        try:
            req = requests.get(url, headers=useragent, proxies=proxies, verify=False, timeout=8, allow_redirects=True)
            response = str(req.content)
            soup = BeautifulSoup(response, "html.parser")
            form_elements = soup.find_all("form")
            action = form_elements[0].attrs.get("action") if form_elements else ""
            
            if not action or action == "?":
                action = ""
            elif action[0] == "/":
                action = action[1:]

            check = re.search("login", str(req.url))

            if not check:
                action = ""

            if req.status_code == 200:
                for login in settings.LOGN_INPUTS:
                    try:
                        find = re.compile(login).search(str(response))
                        if find:
                            login_urls.append(req.url + str(action))
                            print(colored("[+] Login panel found! [{}] - {}", "green").format(req.url, req.status_code))
                            break
                    except IndexError:
                        pass
        except IOError:
            pass
        except IndexError:
            pass
        except KeyboardInterrupt:
            print("\nStopped")
            exit(0)

    return login_urls
