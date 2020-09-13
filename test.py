import requests
import string
from itertools import cycle
import traceback
proxies = []
def get_proxies():
    with open("prox.txt",'r') as fp:
        while True:
            line = fp.readline()
            line = line.translate({ord(c): None for c in string.whitespace})
            try:
                res = requests.get("https://www.urlvoid.com/scan/" + "paypal.com" + "/" , proxies={"http": line, "https": line}, timeout=6)
                proxies.append(line)
                print(line + " worked")
            except:
                print(line + " proxy didnt work")
            if not line:
                break
    with open("proxies_working_2", 'w') as fp:
        for proxy in proxies:
            fp.write(proxy)
            fp.write("\n")


def remove_dups():
    lines_seen = set()
    with open("output.txt", 'w') as out:

        with open("prox.txt", 'r') as fp:
            while True:
                
                line = fp.readline()
                if line != '':
                    print(line)
                    line = line.translate({ord(c): None for c in string.whitespace})
                    line = line.split(':')
                    half_line = line[0]
                    if half_line not in lines_seen:
                        if line[0] != '':
                            print(line)
                            lines_seen.add(half_line)
                            out.write(line[0] + ":" + line[1])
                            out.write('\n')
                if not line:
                    break

def check_proxy():
    proxy = "122.50.5.147:10000"
    res = requests.get("https://www.urlvoid.com/scan/" + "paypal.com" + "/" , proxies={"http": proxy, "https": proxy}, timeout=10)
    print(res)

def get_proxies():
    proxies = []
    with open('proxies_working.txt', 'r') as fp:
        while True:
            proxy = fp.readline()
            if not proxy:
                break
            if proxy not in ['\n', '\r\n']:
                proxy = proxy.translate({ord(c): None for c in string.whitespace})
                proxy_split = proxy.split(":")
                ip_port = proxy_split[0] + ":" + proxy_split[1]
                if len(proxy_split) > 2:
                    username = proxy_split[2]
                    password = proxy_split[3]
                    single = {"https":"https://" + username + ":" + password +"@"+ ip_port}
                else:
                    single = {"https": ip_port}
                proxies.append(single)
    return proxies

proxies = get_proxies()
proxy_pool = cycle(proxies)
#print(proxy_pool)
proxy = next(proxy_pool)
print(proxy)