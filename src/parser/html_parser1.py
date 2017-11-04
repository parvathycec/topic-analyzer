import urllib.request


url = urllib.request.urlopen("http://news.bbc.co.uk/2/hi/health/2284783.stm")
html = url.read()
soup = BeautifulSoup(html)
for script in soup(["script","style"]):
    script.extract()

text = soup.get_text()
lines = (line.strip() for line in text.splitlines())
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
text = '\n'.join(chunk for chunk in chunks if chunk)
print(text)
 
