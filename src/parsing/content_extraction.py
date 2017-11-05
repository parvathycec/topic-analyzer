from newspaper import Article

def get_text(url):
    """Gets the content text from the url"""
    article = Article(url)
    article.download();
    article.parse();
    article.nlp();
    return article.text;
