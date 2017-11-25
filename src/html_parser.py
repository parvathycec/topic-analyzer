import urllib.request
import requests
from bs4 import BeautifulSoup


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

if __name__ == '__main__':
    print("This file can only be imported!")
 
    
