import requests
import socket   
import sys
from urllib.request import Request, urlopen, ssl, socket
from urllib.error import URLError, HTTPError
import json
import ssl 
import datetime
from datetime import date
import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import xmltodict

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
            existing_domains.append(domain(1,hostname,url))
            log("SUCCESS " + url + " exists")
            return 0
        except:
            log("Failed")
            return 1



def check_redirecetion(sus_domain):
    res = requests.get(sus_domain.url,timeout=3)
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(options=options, executable_path="chromedriver.exe")
    driver.get(sus_domain.url)
  
    if (driver.current_url != res.url) & (driver.current_url + "/" != res.url) & (driver.current_url != res.url + "/") & (hostname not in driver.current_url):
        sus_domain.redirected = 1
        sus_domain.redirected_url = driver.current_url
        log(sus_domain.url + " REDIRECTS" + " to" + " " + driver.current_url)
    else:
        log(sus_domain.url + " DOES NOT! REDIRECTS")
    driver.quit()



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
 
        if rank > 10000:
            log(sus_domain.url + " Rank is above 10k")
            sus_domain.rank=1
        else:
            log(sus_domain.url + " Rank is fine")

    except:
        log(sus_domain.url + " Rank is none-exsistent")
        sus_domain.rank=1



def check_iframe(sus_domain):
    if sus_domain.redirection == 1:
        url = sus_domain.redirected_url
    else:
        url = sus_domain.url
    res = requests.get(url)
    data = res.text
    soup = BeautifulSoup(data, 'html.parser')
    print(soup.find('iframe'))



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



def log(string):
    print(str(datetime.datetime.now()) + " " + string)


def run_on_suffix(domain_name, suffix):
    perm  = permutation(domain_name)
    for p in perm:
        check_ssl_and_exist(p, suffix)
    
    for sus in existing_domains:
        check_redirecetion(sus)   
       # ssl_duration_check(sus)
       # check_rank(sus)
       # check_https_token(sus)
       # check_dash(sus)
        print("")


#run_on_suffix("paypal","com")
dom = domain(0,"google.com","http://peypal.com/")
check_redirecetion(dom)
check_iframe(dom)




# send a HTTP request to the URL of the webpage I want to access
#r = requests.get(url)
#print(r.history)
#data = r.text


#soup = BeautifulSoup(data, 'html.parser')
#print(r.url)
#print(soup.find('iframe'))


