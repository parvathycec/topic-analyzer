import requests
from bs4 import BeautifulSoup
import RankedWord  #import the class file
from newspaper import Article
from newspaper.article import ArticleException


from __init__ import META_SCORE , NO_OF_TOKENS ,OCCURENCE_SCORE, POS_SCORE ,URL_SCORE, TITLE_SCORE ,H1_SCORE 

def calculate_rank(key,content,total_rank,freq = 0):

    if freq != 0:
        rank =0
        content = content.split(" ")
        content = [x.lower() for x in content]
        indices = []
        if " " in key: #if it is a phrase
            phrases = key.split(" ")
            for p in phrases:
                if p.lower() in content:
                    indices.append(content.index(p.lower()))
                else:
                    return 0
        else:
            if key in content:
                rank = total_rank
                return rank

    else: #no of occurences

        rank
        
                

        
def calculate_url_score(url,word):
    #checks whether the word/phrase appears in the url,if it appears, then calculate a score accordingly
    if " " in word: #if it is a phrase
        word = word.replace(" ","-")   #replace the space in the word with -, because the url text is seperated by -
    print("url")
    print(check_all_cases_rank(word,url,URL_SCORE))
    return check_all_cases_rank(word,url,URL_SCORE)

def calculate_nof_token(word):
    if " " in word:
        nof_token_score = NO_OF_TOKENS

    else:
        nof_token_score = 0

    return nof_token_score

    return nof_token_score

def calculate_title_score(soup,word):
    
    title_content = soup.title.string

    return calculate_rank(word,title_content,TITLE_SCORE)

    
def calculate_meta_score(soup,word):
    meta_content = None
    for meta_tag in soup.findAll("meta"):
       meta_con =  meta_tag.get("content",None)
       if meta_con != None:
           meta_content += meta_con + " "

    print("meta")      
    #check whether the word occurs in the meta data and assign rank
    if meta_content != None:

        return calculate_rank(word,meta_content,META_SCORE)
        
    else:
        return 0

def calculate_h1_score(soup,word):
    h1_tag_content = None
    for h1_tag in soup.find_all("h1"):
        h1_tag_content = h1_tag.string
        
   
    

    #if the word appears in the h1, then assign rank accordingly
    if h1_tag_content != None:
        h1_tag_rank = calculate_rank(word,h1_tag_content,H1_SCORE)
    else:
        h1_tag_rank = 0
        
    return h1_tag_rank
        
def calculate_occurances_score(word,url):
    article = Article(url)
    try:
        article.download()
    except ArticleException:
        print("Check your URL or network connection");
        return None;
    else:
        article.parse();
        #article.nlp();
        article_content = article.title

    if " " in word:
        
        
    if " " in word: #if there is a space in between the word, then it is considered as a phrase
        score = article_content.count(word)
        
        
        #score = check_all_cases_rank(word,article_content,OCCURENCE_SCORE)

    else:

        article_content_words = article_content.split(" ")
        article_content_words

        score_1 = article_content_words.count(word)
        score_2 = article_content_words.count(word.lower())
        score_3 = article_content_words.count(word.upper())
        score_4 = article_content_words.count(word.title())

        score = score_1 + score_2 + score_3 + score_4

    print("freq")
    print(score * OCCURENCE_SCORE)
    return (score * OCCURENCE_SCORE)

        
            
        
    
    
def do_rank(url,rank_obj):
   # rank_obj = RankedWord.RankedWord(word,isPos,score)

    word = rank_obj.getword()

    req= requests.get(url)  #get the url request
    soup = BeautifulSoup(req.text,"lxml") #parse it through BeautifulSoup
    #initialise the variables to hold the rank values
    url_score = 0
    title_score = 0
    meta_score = 0
    h1_score = 0
    occurances_score = 0
    pos_score = 0
    
    url_score = calculate_url_score(url,word)

    title_score = calculate_title_score(soup,word)
    
    meta_score =  calculate_meta_score(soup,word)

    h1_score = calculate_h1_score(soup,word)

    occurances_score = calculate_occurances_score(word,url)
    
    no_of_token_score = 0
    no_of_token_score = calculate_nof_token(word)
    
    if rank_obj.isPos == True:
        pos_score = POS_SCORE

    additional_meta_score = 0

    if pos_score!= 0 and title_score != 0:
        additional_meta_score = 50
    #total rank
    
    total_rank = url_score + additional_meta_score + no_of_token_score +title_score + meta_score + h1_score + occurances_score + pos_score
    
    rank_obj.score = total_rank

    return rank_obj

'''
url = "https://www.washingtonpost.com/investigations/two-more-women-describe-unwanted-overtures-by-roy-moore-at-alabama-mall/2017/11/15/2a1da432-ca24-11e7-b0cf-7689a9f2d84e_story.html?utm_term=.e749f39597da"
rank_obj = RankedWord.RankedWord("investigations",True)
do_rank(url,rank_obj)
print(rank_obj.score)
'''
