import urllib.request
import requests
from bs4 import BeautifulSoup

def htmlParser(website_url):
    
    url = urllib.request.urlopen(website_url)
    html = url.read()
    soup = BeautifulSoup(html)
    for script in soup(["script","style"]):
        script.extract()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ''.join(chunk for chunk in chunks if chunk)
    return text
     

def parse_html(url):
    req= requests.get(url)  #get the url request
    soup = BeautifulSoup(req.text,"lxml") #parse it through BeautifulSoup
    #1. get title
    title_content = soup.title.string
    #2. get metatags
    meta_content = ""
    for meta_tag in soup.findAll("meta"):
       meta_con =  meta_tag.get("content",None)
       if meta_con != None:
           meta_content += meta_con + " "
    #3. Get h1 tags
    h1_tag_content = None
    for h1_tag in soup.find_all("h1"):
        h1_tag_content = h1_tag.string
    return title_content, meta_content, h1_tag_content;       
    
