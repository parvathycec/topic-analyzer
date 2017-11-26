Requirement:
Python 3.6
In Windows: Microsoft C++ 15 build tools
Link: http://landinghub.visualstudio.com/visual-cpp-build-tools

Commands to install libraries (tested in Windows 10):

python -m pip install beautifulsoup4
python -m pip install newspaper3k
python -m pip install -U spacy
python -m spacy download en
(It is okay if an error for shortcut link appears).
python -m pip install wikipedia
python -m pip install numpy
(If not there already) 
python -m pip install --upgrade gensim
python -m nltk.downloader punkt

DataSet to be downloaded:

Download from the github link below and put it in the same directory as python files.

https://github.com/parvathycec/topic-analyzer/blob/master/src/GoogleNews-vectors-gensim-normed.bin

Run project:
python project_gui.py

Notes:
Analyzer might take upto a few minutes to get the output based on the length of the article.
This is because a lot of HTTP calls are occurring.
We have tested mainly the articles in http://news.google.com
Some of the test links we tested are:
http://thehill.com/policy/cybersecurity/361583-4-legal-dimensions-of-the-uber-data-breach
http://news.bbc.co.uk/2/hi/health/2284783.stm
http://www.latimes.com/business/hiltzik/la-fi-hiltzik-net-neutrality-20171122-story.html 
