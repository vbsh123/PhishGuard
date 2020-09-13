import requests
import socket   
import sys
from urllib.request import Request, urlopen, ssl, socket
import json
import ssl 
import datetime
from datetime import date
import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import xmltodict
import time
from dom_compare import similiar
import random
from permutations.permutation import permutation_go as pm
import favicon
import tldextract
from sklearn import tree
from sklearn.metrics import accuracy_score
import numpy as np
from detection import decision_tree
from send_mail import send_email
from lxml.html import fromstring
from itertools import cycle
import traceback
import string

#will be added to requests
user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
user_agent = random.choice(user_agent_list)
headers = {'User-Agent': user_agent}
#will be added to requests

existing_domains = []
found_domains = []
data_set_urls = []
original_url = "hi"
hostname = "bye" 

class domain:
    def __init__(self, ssl, hostname, url):
        self.ssl=ssl
        self.hostname=hostname
        self.url=url
        self.redirected_hostname = ""
        self.redirected_url = ""
        self.redirection=-1
        self.ssl_duration=-1
        self.rank=-1
        self.https_token=-1
        self.dash_token=-1
        self.iframe=-1
        self.mail=-1
        self.too_many_requests=-1
        self.url_length=-1
        self.favicon=-1
        self.report=-1
        self.dots=-1
        self.result=-1
        self.dangerous=-1


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

proxy= next(proxy_pool)


def send_to_email(email, contents):
    send_email(email,contents)

def get_dots(sus_domain):
    if sus_domain.redirection == 1:
        url = sus_domain.redirected_url
    else:
        url = sus_domain.url
    
    counter = 0
    for letter in url:
        if letter == '.':
            counter+=1
            if counter == 2:
                sus_domain.dots=0
            if counter > 2:
                sus_domain.dots = 1
                break

def get_favicon(sus_domain):
    if sus_domain.redirection == 1:
        url = sus_domain.redirected_url
    else:
        url = sus_domain.url
    
    icons = favicon.get(url)
    
    if not icons:
        sus_domain.icons = 1


def compare_doms(sus_domain):
    if sus_domain.redirection == 1:
        sus_url = sus_domain.redirected_url
    else:
        sus_url = sus_domain.url
    
    sus_resp = requests.get(sus_url)
    resp = requests.get(original_url)
    acc =  similiar(sus_resp.text,resp.text,0.15) * 100
    if acc > 0.6:
        sus_domain.dangerous = 1
    else:
        sus_domain.dangerous = -1
def check_ssl_and_exist(domain_name, suffix):
    log("Checking if " + "https://" + domain_name + "." + suffix + " exists")
    try:
        hostname = domain_name + "." + suffix
        url = "https://" + hostname
        res = requests.get(url,timeout=3)
        existing_domains.append(domain(-1,hostname,url))
        log("SUCCESS " + url + " exists")
        return 0
    except:
        log("Failed")
        log("Checking if " + "http://" + domain_name + "." + suffix + " exists")
        try:
            hostname = domain_name + "." + suffix
            url = "http://" + hostname
            res = requests.get(url,timeout=3)
            existing_domains.append(domain(1,hostname,url))
            log("SUCCESS " + url + " exists")
            return 0
        except:
            log("Failed")
            return 1



def check_redirecetion(sus_domain,driver):
    driver.get(sus_domain.url)
    if (driver.current_url != sus_domain.url) & (driver.current_url + "/" != sus_domain.url) & (driver.current_url != sus_domain.url + "/"):
        sus_domain.redirection = 1
        sus_domain.redirected_url = driver.current_url
        log(sus_domain.url + " REDIRECTS" + " to " + driver.current_url)
        ext = tldextract.extract(sus_domain.redirected_url)
        sus_domain.redirected_hostname = ext.domain + "." + ext.suffix
        if "https" in sus_domain.redirected_url:
            sus_domain.ssl = -1
        else:
            sus_domain.ssl = 1
    else:
        too_many_requests(sus_domain,sus_domain.url)
        log(sus_domain.url + " DOES NOT! REDIRECT")



def permutation(domain_name,suffix,level):
    if level == 4:
        return miniPermutation(domain_name,suffix)
    res = pm(level,domain_name,suffix)
    if level != 3:
        add_suffix = "." + suffix
        for perm in res:
            perm = perm + add_suffix

    return res  

def miniPermutation(domain_name,suffix):
    res = []
    abc = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    for letter in abc:
        res.append(domain_name + letter)
    return res    

def check_rank(sus_domain):   
    if sus_domain.redirection == 1:
        url = sus_domain.redirected_url
    else:
        url = sus_domain.url
    try:
        xml = urllib.request.urlopen('http://data.alexa.com/data?cli=10&dat=s&url={}'.format(url)).read()
 
        result= xmltodict.parse(xml)
 
        data = json.dumps(result).replace("@","")
        data_tojson = json.loads(data)
        url = data_tojson["ALEXA"]["SD"][1]["POPULARITY"]["URL"]
        rank= data_tojson["ALEXA"]["SD"][1]["POPULARITY"]["TEXT"]
 
        if rank > 100000:
            log(sus_domain.url + " Rank is above 10k")
            sus_domain.rank=1
        else:
            log(sus_domain.url + " Rank is fine")

    except:
        log(sus_domain.url + " Rank is none-exsistent")
        sus_domain.rank=1



def check_malicious_content(sus_domain):
    malicious_flag = False
    if sus_domain.redirection == 1:
        url = sus_domain.redirected_url
        if "mailto:" in url:
            sus_domain.mail=1
            malicious_flag = True
    else:
        url = sus_domain.url

    too_many_requests(sus_domain,url)
    res = requests.get(url)
    data = res.text
    soup = BeautifulSoup(data, 'html.parser')
    iframes = soup.findAll('iframe')
    for iframe in iframes:
        if 'frameBorder=\"0\"' in iframes:
            sus_domain.iframe = 1
            malicious_flag = True

    if malicious_flag == True:
        log(sus_domain.url + " Has malicious content")
    else:
        log(sus_domain.url + " Has safe content")

def check_url_length(sus_domain):
    if sus_domain.redirection == 1:
        if len(sus_domain.redirected_url) > 25:
            sus_domain.url_length = 1
            log(sus_domain.redirected_url + " Has a long url")
            return 0
    log(sus_domain.redirected_url + " Has normal size url") 



def ssl_duration_check(sus_domain):
    if sus_domain.redirection == -1:
        hostname = sus_domain.hostname
    else:
        hostname = sus_domain.redirected_hostname
    if sus_domain.ssl == -1: 
        ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
        context = ssl.create_default_context()
        conn = context.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=hostname,
        )
        conn.settimeout(3.0)
    
        conn.connect((hostname, 443))
        ssl_info = conn.getpeercert()

        ssl_start = datetime.datetime.strptime(ssl_info['notBefore'], ssl_date_fmt).date()
        today_date = date.today()
    
        if (today_date - ssl_start).days > 730:
            log("Checking: " + sus_domain.url + " SSL duration - TOO OLD")
            sus_domain.ssl = 1
        else:
            log("Checking: " + sus_domain.url + " SSL duration - Fine")
    else:
        log(sus_domain.url + " Does not have SSL encryption")


def check_https_token(sus_domain):
    if "https" in sus_domain.hostname:
        log("https is present in hostname")
        sus_domain.https_token=1
    else:
        log("https not present in hostname")


def check_dash(sus_domain):
    if "-" in sus_domain.hostname:
        log("\'-\' is present in hostname")
        sus_domain.dash_token=1
    else:
        log("\'-\' not present in hostname")


def too_many_requests(sus_domain,url):
    page = requests.get(url)
    if page.text == "Too many requests":
        sus_domain.too_many_requests = 1
        log("There is \'Too many requests\' for: " + sus_domain.url)    
    else:
        log("There is not \'Too many requests for\': " + sus_domain.url)

def check_working_proxy():
    proxy = next(proxy_pool)
    try:
        
        res = requests.get("https://google.com", proxies = proxy,timeout=10)
        print("got working proxy")
        return proxy
    except:
        print("checking another proxy")
        check_working_proxy()

def log(string):
    print(str(datetime.datetime.now()) + " " + string)

def check_report(sus_domain,proxy_tmp):   

    if sus_domain.redirection == -1:
        hostname = sus_domain.hostname
    else:
        hostname = sus_domain.redirected_hostname
    print("https://www.urlvoid.com/scan/" + hostname)
    try:
        res = requests.get("https://www.urlvoid.com/scan/" + hostname + "/" , proxies=proxy_tmp, timeout=5 )
    except:
        print("problem is in proxy")  
       
    soup = BeautifulSoup(res.content,features="lxml")
    danger = soup.findAll("span", {"class": "label label-danger"})
    if not danger:
        danger = soup.findAll("span", {"class": "label label-success"})
    try:
        
        danger = str(danger[0].text)
        danger = danger.split('/')
        danger = int(danger[0])
        if danger > 0:
            sus_domain.rank = 1
    except:
        print("problem i snot in proxy")

def form_message(sus_domain):
    message = {"DETECTED: " + sus_domain.url}
    return message

def run_on_suffix(domain_name, suffix):
    proxy = check_working_proxy()
    inputs = np.array([1,1,1,1,1,1,1,1])
    perm  = permutation(domain_name,suffix,4)
    for p in perm:
        check_ssl_and_exist(p, suffix)
    
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(options=options, executable_path="chromedriver.exe")
    for sus in existing_domains:
        try:
            check_redirecetion(sus,driver)
            print("")
        except:
            pass   
    driver.quit()
    
    for sus in existing_domains:
        try:
            ssl_duration_check(sus)
        except:
            sus.ssl=1
        try:
            check_malicious_content(sus)
        except:
            sus.mail=1
            sus.iframe=1
        while(True):
            try:
                proxy = check_working_proxy()
                check_report(sus,proxy)
                break
            except:
                print("problem with the connection")
                proxy = check_working_proxy()
        try:
            check_https_token(sus)
        except:
            sus.https_token=1
        try:
            check_dash(sus)
        except:
            sus.dash_token=1
        try:
            check_url_length(sus)
        except:
            sus.url_length=1
        try:
            get_dots(sus)
        except:
            sus.dots=1
        try:
            get_favicon(sus)
        except:
            sus.favicon=1
        tmp = np.array([sus.url_length,sus.dots,sus.ssl,sus.favicon,sus.mail,sus.redirection,sus.iframe,sus.rank])
        inputs = np.vstack((inputs,tmp))

        print("")
    results = decision_tree.check_phish(inputs)
    print(results)
    for index in range(1,len(results)):
        existing_domains[index-1].result = results[index] 
    
    for sus_domain in existing_domains:
        if sus_domain.result == 1:
            found_domains.append(sus_domain)
    
    message = ""

    for found in found_domains:
        if found.redirection == 1:
            url = found.redirected_url
        else:
            url = found.url
        found.dangerous = compare_doms(found)
        message += form_message(found)



    print(message)
    return message
    

    


def scan(url,email):
    original_url=url
    print(original_url)
    ext = tldextract.extract(url)
    message = run_on_suffix(ext.domain,ext.suffix)
    send_to_email(email,message)

def run(domain_name):
    try:
        suffix_list = ["com","net","org","ga","tk","ml","cf","gq","gdn"]
        for suffix in suffix_list:
            run_on_suffix(domain_name, suffix)
            return 0
    except:
        return 1





#scan("http://paypal.com","yoelvb5801@gmail.com")