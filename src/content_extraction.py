'''
@summary: Step 1 of the algorithm: Extracts content of the article 
using third party library newspaper article.
@author: Parvathy
'''

from newspaper import Article
from newspaper.article import ArticleException

def get_text(url):
    """Gets the content text from the url"""
    article = Article(url)
    try:
        article.download();
    except ArticleException:
        raise Exception("Error: Check your URL or network connection!");
    else:
        article.parse();
        article.nlp();
        #Returns title and content of the website
        return (article.title, article.text);
