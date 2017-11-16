from newspaper import Article
from newspaper.article import ArticleException


#TODO: Remove the content starting like Newspaper name
def get_text(url):
    """Gets the content text from the url"""
    article = Article(url)
    try:
        article.download();
    except ArticleException:
        print("Check your URL or network connection");
        return None;
    else:
        article.parse();
        article.nlp();
        return article.title + " " +article.text;
