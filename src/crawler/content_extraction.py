from newspaper import Article

#TODO: Remove the content starting like Newspaper name
def get_text(url):
    """Gets the content text from the url"""
    article = Article(url)
    article.download();
    article.parse();
    article.nlp();
    return article.title + " " +article.text;
