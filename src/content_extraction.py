from newspaper import Article
from newspaper.article import ArticleException

def get_text(url):
    """Gets the content text from the url"""
    article = Article(url)
    try:
        article.download();
    except ArticleException:
        raise Exception("Check your URL or network connection");
    else:
        article.parse();
        article.nlp();
        return article.title + " " +article.text;
