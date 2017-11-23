# topic-analyzer
Group Project by Parvathy Mohan and Saranya Balaji for Python course
Dependency:
python -m nltk.downloader all

1. Step 1: Html Parsing:
a) BeautifulSoap4
Library: BeautifulSoap4
Reference : http://www.pythonforbeginners.com/python-on-the-web/web-scraping-with-beautifulsoup/
commands:
python -m pip install beautifulsoup4 


b) Content Extraction: 
Library name - NewsPaper
Reference: https://github.com/codelucas/newspaper
Command:
python -m pip install newspaper3k

2. Noun Chunker:
Library: Spacy, Wikipedia
For spacy, in windows, make sure that there Visual C++ 14 build tools installed.
If not, install from here http://landinghub.visualstudio.com/visual-cpp-build-tools

Commands:
python -m pip install -U spacy
python -m spacy download en
python -m pip install wikipedia

3. Kmeans Clustering:
Library: Numpy, Gensim
python -m pip install numpy
python -m pip install --upgrade gensim

Data Set: GoogleNews Pre-trained data set. Download from here:
https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit
Once you download it, give the path in the __init__.py of grouping package.

4. Ranking:
Library: requests, beautifulsoup4
commands: pip install beautifulsoup4
pip install requests
reference : http://www.pythonforbeginners.com/beautifulsoup/beautifulsoup-4-python






