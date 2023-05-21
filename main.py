import ipaddress
import re
import urllib.request
from bs4 import BeautifulSoup
import requests
from googlesearch import search
import whois
from datetime import date, datetime
from urllib.parse import urlparse
import numpy as np
import pickle

model = pickle.load(open('TrainedModel_SurfGuard','rb'))

from fastapi import FastAPI
app = FastAPI()

# [1] UsingIp
def UsingIp(url):
    try:
        ipaddress.ip_address(url)
        return -1
    except:
        return 1
    
# [2] LongUrl
def LongUrl(url):
    if len(url) < 54:
        return -1
    elif len(url) >= 54 and len(url) <= 75:
        return 0
    else:
        return 1
    
# [3] ShortiningService
def shortUrl(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net', url)
    if match:
        return -1
    return 1

# [4] Having@Symbol
def HavingAtSymbol(url):
    if "@" in url:
        return 1
    return -1

# [5] DoubleSlashRedirecting
def DoubleSlashRedirecting(url):
    if url.rfind('//')>6:
        return -1
    return 1

# [6] PrefixSuffix
def PrefixSuffix(url):
    if '-' in urlparse(url).netloc:
        return 1
    else:
        return -1
    
# [7] HavingSubDomain
def HavingSubDomain(url):
    if url.count('.') == 1:
        return 1
    elif url.count('.') == 2:
        return 0
    else:
        return -1

# [8] Https
def HttpsToken(url):
    if urlparse(url).scheme == "https":
        return 1
    return -1

# [9] DomainRegistrationLength
def DomainRegistrationLength(url):
    try:
        w = whois.whois(url)
        creation = w.creation_date
        exp = w.expiration_date
        length = (exp[0]-creation[0]).days
        if length <= 365:
            return 1
        else:
            return -1
    except:
        return -1
    
# [10] Favicon
def Favicon(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        icon_link = soup.find("link", rel="shortcut icon")
        if icon_link != None:
            return 1
        else:
            return -1
    except:
        return -1
    
# [11] UsingNonStandardPort
def UsingNonStandardPort(url):
    try:
        domain = urlparse(url).netloc
        port = domain.split(':')
        if len(port)>1:
            return 1
        else:
            return -1
    except:
        return -1
    
# [12] UsingHttpsDomain
def UsingHttpsDomain(url):
    try:
        domain = urlparse(url).netloc
        if 'https' in domain:
            return -1
        return 1
    except:
        return -1
    
# [13] RequestUrl
def RequestUrl(url):
    try:
        domain = urlparse(url).netloc
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        for img in soup.find_all('img', src=True):
            dots = [x.start(0) for x in re.finditer('\.', img['src'])]
            if url in img['src'] or domain in img['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for audio in soup.find_all('audio', src=True):
            dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
            if url in audio['src'] or domain in audio['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for embed in soup.find_all('embed', src=True):
            dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
            if url in embed['src'] or domain in embed['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for iframe in soup.find_all('iframe', src=True):
            dots = [x.start(0) for x in re.finditer('\.', iframe['src'])]
            if url in iframe['src'] or domain in iframe['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        try:
            percentage = success/float(i) * 100
            if percentage < 22.0:
                return 1
            elif((percentage >= 22.0) and (percentage < 61.0)):
                return 0
            else:
                return -1
        except:
            return 0
        
    except:
        return -1
    
# [14] AnchorUrl
def AnchorURL(url):
    try:
        domain = urlparse(url).netloc
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        i,unsafe = 0,0

        for a in soup.find_all('a', href=True):
            if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (url in a['href'] or domain in a['href']):
                unsafe = unsafe + 1
            i = i + 1

        try:
            percentage = unsafe / float(i) * 100
            if percentage < 31.0:
                return 1
            elif ((percentage >= 31.0) and (percentage < 67.0)):
                return 0
            else:
                return -1
        except:
            return -1

    except:
        return -1

# [15] Links In Script Tags
def LinksInScriptTags(url):
    try:
        domain = urlparse(url).netloc
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        i,success = 0,0
        
        for link in soup.find_all('link', href=True):
            dots = [x.start(0) for x in re.finditer('\.', link['href'])]
            if url in link['href'] or domain in link['href'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for script in soup.find_all('script', src=True):
            dots = [x.start(0) for x in re.finditer('\.', script['src'])]
            if url in script['src'] or domain in script['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        try:
            percentage = success / float(i) * 100
            if percentage < 17.0:
                return 1
            elif((percentage >= 17.0) and (percentage < 81.0)):
                return 0
            else:
                return -1
        except:
            return 0
        
    except:
        return -1

# [16] ServerFormHandler
def ServerFormHandler(url):
    try:
        domain = urlparse(url).netloc
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        if len(soup.find_all('form', action=True))==0:
            return 1
        else :
            for form in soup.find_all('form', action=True):
                if form['action'] == "" or form['action'] == "about:blank":
                    return -1
                elif url not in form['action'] and domain not in form['action']:
                    return 0
                else:
                    return 1
                
    except:
        return -1

# [17] SubmittingToEmail
def SubmittingToEmail(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        if re.findall(r"[mail\(\)|mailto:?]", soup):
            return -1
        else:
            return 1
    except:
        return -1
    
# [18] AbnormalUrl
def AbnormalUrl(url):
    try:
        domain = urlparse(url).netloc
        r = requests.get(url)
        whois_r = whois.whois(domain)
        domain = urlparse(url).netloc
        if r.text == whois_r:
            return 1
        else:
            return -1
    except:
        return -1
    
# [19] Website Forwarding
def WebsiteForwarding(url):
    try:
        r = requests.get(url)
        if len(r.history) <= 1:
            return 1
        elif len(r.history) <= 4:
            return 0
        else:
            return -1
    except:
        return -1
    
# [20] Status Bar Customization
def StatusBarCustomization(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        if re.findall("<script>.+onmouseover.+</script>", r.text):
            return 1
        else:
            return -1
    except:
        return -1
    
# [21] Disabling Right Click
def DisablingRightClick(url):
    try:
        r = requests.get(url)
        if re.findall(r"event.button ?== ?2", r.text):
            return 1
        else:
            return -1
    except:
        return -1
    
# [22] Using Pop-up Window
def UsingPopupWindow(url):
    try:
        r = requests.get(url)
        if re.findall(r"alert\(", r.text):
            return 1
        else:
            return -1
    except:
        return -1
    
# [23] Iframe Redirection
def IframeRedirection(url):
    try:
        r = requests.get(url)
        if re.findall(r"[<iframe>|<frameBorder>]", r.text):
            return 1
        else:
            return -1
    except:
        return -1
    
# [24] Age of Domain
def AgeOfDomain(url):
    try:
        domain = urlparse(url).netloc
        whois_domain = whois.whois(domain)
        start_date = whois_domain.creation_date
        current_date = datetime.now()
        age =(current_date-start_date[0]).days
        if age >= 180:
            return 1
        return -1
    except:
        return -1
    
# [25] DNS Record
def DNSRecord(url):
    try:
        domain = urlparse(url).netloc
        dns = whois.whois(domain)
        if dns == None:
            return -1
        return 1
    except:
        return -1
    
# [26] Web Traffic
def WebTraffic(url):
    try:
        rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url="+url).read(), "xml").find("REACH")['RANK']
        rank = int(rank)
        if rank < 100000:
            return 1
        return 0
    except:
        return -1
    
# [27] PageRank
def PageRank(url):
    try:
        domain = urlparse(url).netloc
        pageRank = requests.post("https://www.checkpagerank.net/index.php", {"name": domain})
        globalRank = int(re.findall(r"Global Rank: ([0-9]+)", pageRank.text)[0])
        if globalRank > 0 and globalRank < 100000:
            return 1
        return -1
    except:
        return -1
    
# [28] Google Index
def GoogleIndex(url):
    try:
        site = search(url, 5)
        if site:
            return 1
        return -1
    except:
        return -1
    
# [29] Number of Links Pointing to Page
def LinksPointingToPage(url):
    try:
        r = requests.get(url)
        pointers = len(re.findall(r"<a href=", r.text))
        if pointers == 0:
                return 1
        elif pointers <= 2:
            return 0
        else:
            return -1
    except:
        return -1
    
# [30] Statistical Reports Based Feature
def StatisticalReportsBasedFeature(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        if re.findall(r"click|here|link|free|cash|video|visit|website|limited|time|offer|instant|download|win|winner|award|reward|prize|won|claim|now", soup.text):
            return -1
        return 1
    except:
        return 1

@app.get("/getStatus")

def extract(url: str):

  urlFeatures = [] 
  urlFeatures.append(UsingIp(url))
  urlFeatures.append(LongUrl(url))
  urlFeatures.append(shortUrl(url))
  urlFeatures.append(HavingAtSymbol(url))
  urlFeatures.append(DoubleSlashRedirecting(url))
  urlFeatures.append(PrefixSuffix(url))
  urlFeatures.append(HavingSubDomain(url))
  urlFeatures.append(HttpsToken(url))
  urlFeatures.append(DomainRegistrationLength(url))
  urlFeatures.append(Favicon(url))
  urlFeatures.append(UsingNonStandardPort(url))
  urlFeatures.append(UsingHttpsDomain(url))
  urlFeatures.append(RequestUrl(url))
  urlFeatures.append(AnchorURL(url))
  urlFeatures.append(LinksInScriptTags(url))
  urlFeatures.append(ServerFormHandler(url))
  urlFeatures.append(SubmittingToEmail(url))
  urlFeatures.append(AbnormalUrl(url))
  urlFeatures.append(WebsiteForwarding(url))
  urlFeatures.append(StatusBarCustomization(url))
  urlFeatures.append(DisablingRightClick(url))
  urlFeatures.append(UsingPopupWindow(url))
  urlFeatures.append(IframeRedirection(url))
  urlFeatures.append(AgeOfDomain(url))
  urlFeatures.append(DNSRecord(url))
  urlFeatures.append(WebTraffic(url))
  urlFeatures.append(PageRank(url))
  urlFeatures.append(GoogleIndex(url))
  urlFeatures.append(LinksPointingToPage(url))
  urlFeatures.append(StatisticalReportsBasedFeature(url))

  inputArray = np.asarray(urlFeatures).reshape(1,-1)
  prediction = model.predict(inputArray)

  print(urlFeatures)
  print(str(prediction))

  return str(prediction[0])