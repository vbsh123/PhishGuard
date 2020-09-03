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
original_url = str(sys.argv[1])
hostname = str(sys.argv[2]) 

class domain:
    def __init__(self, ssl, hostname, url):
        self.ssl=ssl
        self.hostname=hostname
        self.url=url
        self.redirected_url = ""
        self.redirection=0
        self.ssl_duration=0
        self.rank=0   
        self.https_token=0
        self.dash_token=0
        self.iframe=0
        self.mail=0
        self.too_many_requests=0
        self.url_length=0

 

def compare_doms(sus_domain):
    if sus_domain.redirection == 1:
        sus_url = sus_domain.redirected_url
    else:
        sus_url = sus_domain.url
    
    sus_resp = requests.get(sus_url)
    resp = requests.get(original_url)
    return similiar(sus_resp.text,resp.text,0.15) * 100

def check_ssl_and_exist(domain_name, suffix):
    log("Checking if " + "https://" + domain_name + "." + suffix + " exists")
    try:
        hostname = domain_name + "." + suffix
        url = "https://" + hostname
        res = requests.get(url,timeout=3)
        existing_domains.append(domain(1,hostname,url))
        log("SUCCESS " + url + " exists")
        return 0
    except:
        log("Failed")
        log("Checking if " + "http://" + domain_name + "." + suffix + " exists")
        try:
            hostname = domain_name + "." + suffix
            url = "http://" + hostname
            res = requests.get(url,timeout=3)
            existing_domains.append(domain(0,hostname,url))
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
        log(sus_domain.url + " REDIRECTS" + " to" + " " + driver.current_url)
    else:
        too_many_requests(sus_domain,sus_domain.url)
        log(sus_domain.url + " DOES NOT! REDIRECT")



def permutation(domain_name):
    log("Using permutation on: " + domain_name)
    res = []
    for i in range(len(domain_name)):
        string = domain_name[0:i] + domain_name[i] + domain_name[i:]
        log(string + " added to the list")
        res.append(string)      
    res.append("peypal")
    log("peypal added to the list")    
    res.append("paypalk")
    log("paypalk added to the list")
    res.append("paypal")        
    log("paypal added to the list")



    return res  

def check_rank(sus_domain):   
    try:
        xml = urllib.request.urlopen('http://data.alexa.com/data?cli=10&dat=s&url={}'.format(sus_domain.url)).read()
 
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
    if sus_domain.ssl == 1: 
        ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
        context = ssl.create_default_context()
        conn = context.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=sus_domain.hostname,
        )
        conn.settimeout(3.0)
    
        conn.connect((sus_domain.hostname, 443))
        ssl_info = conn.getpeercert()

        ssl_start = datetime.datetime.strptime(ssl_info['notBefore'], ssl_date_fmt).date()
        today_date = date.today()
    
        if (today_date - ssl_start).days > 730:
            log("Checking: " + sus_domain.url + " SSL duration - TOO OLD")
            sus_domain.ssl_duration = 1
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


def log(string):
    print(str(datetime.datetime.now()) + " " + string)


def run_on_suffix(domain_name, suffix):
    perm  = permutation(domain_name)
    for p in perm:
        check_ssl_and_exist(p, suffix)
    
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(options=options, executable_path="chromedriver.exe")
    for sus in existing_domains:
        check_redirecetion(sus,driver)
        print("")   
    driver.quit()
    
    for sus in existing_domains:
        ssl_duration_check(sus)
        check_malicious_content(sus)
        check_rank(sus)
        check_https_token(sus)
        check_dash(sus)
        check_url_length(sus)
        print("")

run_on_suffix("paypal","com")



