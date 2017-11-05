import urllib.request

from bs4 import BeautifulSoup
website_url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
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
     
