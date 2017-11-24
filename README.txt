Requirement:
Python 3.6
In Windows: Microsoft C++ 15 build tools
Link: http://landinghub.visualstudio.com/visual-cpp-build-tools

Third Party Libraries to be installed:
1) BeautifulSoup
2) Newspaper Article
3) Numpy
4) Spacy
5) Gensim

Commands to install libraries (tested in Windows 10):

python -m pip install beautifulsoup4
python -m pip install newspaper3k
python -m pip install -U spacy
python -m spacy download en_core_web_sm
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
python project_ui.py
