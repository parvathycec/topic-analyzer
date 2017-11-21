import ranked_word  #import the class file

URL_SCORE = 100
TITLE_SCORE = 100
H1_SCORE = 100
META_SCORE = 100
OCCURENCE_SCORE = 5
POS_SCORE = 100
NO_OF_TOKENS =100




def check_for_consecutive_numbers(List):
    if len(List) == (max(List) - min(List) + 1):
        if len(List) == len(set(List)):
            return True
        else:
            return False
    else:
        return False

def calculate_rank(key,content,total_rank):

    rank =0
    content = content.split(" ")
    content = [x.lower() for x in content]
    content = [x.replace(",","") for x in content]
    content = [x.replace(".","") for x in content]
    
    indices = []
    if " " in key: #if it is a phrase
        phrases = key.split(" ")
        for p in phrases:
            if p.lower() in content:
                indices.append(content.index(p.lower()))

            
            else:
                return 0
        #check if it is a consecutive number
        # two conditions to be checked, n(len of the list) == max(list) - min(list) + 1 and no duplicates

        if (check_for_consecutive_numbers(indices) == True):
            return total_rank
        else:
            return 0
        
       
    else: #if it is not a phrase
        if key in content: 
            return total_rank
        else:
            return 0

     

        
        
                

        
def calculate_url_score(url,word):
    #checks whether the word/phrase appears in the url,if it appears, then calculate a score accordingly
    first_split = url.split("/")
    second_split = first_split[ len(first_split)- 1]
    url_content = second_split.split(".")
    url_content = str(url_content[0])
    url_content = url_content.replace("-"," ")
    url_rank = calculate_rank(word,url_content,URL_SCORE)
    return url_rank


def calculate_nof_token(word):
    if " " in word: #if it is a phrase give additional rank score
        nof_token_score = NO_OF_TOKENS

    else:
        nof_token_score = 0

    return nof_token_score

   

def calculate_title_score(word, title_content):
    #title_content = soup.title.string
    print("TITLE : ", title_content);
    return calculate_rank(word,title_content,TITLE_SCORE)

    
def calculate_meta_score(word, meta_content):
    #meta_content = ""
    #for meta_tag in soup.findAll("meta"):
    #   meta_con =  meta_tag.get("content",None)
    #   if meta_con != None:
    #       meta_content += meta_con + " "
    #check whether the word occurs in the meta data and assign rank
    if meta_content != "":
        return calculate_rank(word,meta_content,META_SCORE)
        
    else:
        return 0

def calculate_h1_score(word, h1_tag_content):
    #h1_tag_content = None
    #for h1_tag in soup.find_all("h1"):
    #    h1_tag_content = h1_tag.string
    #if the word appears in the h1, then assign rank accordingly
    if h1_tag_content != None:
        h1_tag_rank = calculate_rank(word,h1_tag_content,H1_SCORE)
    else:
        h1_tag_rank = 0
        
    return h1_tag_rank
        
def calculate_occurances_score(word,article_content):
    #article = Article(url)
    #try:
    #    article.download()
    #except ArticleException:
    #    print("Check your URL or network connection");
    #    return None;
    #else:
    #    article.parse();
        #article.nlp();
    #    article_content = article.title

        
    if " " in word: #if there is a space in between the word, then it is considered as a phrase
        score = article_content.lower().count(word)
        
        
        #score = check_all_cases_rank(word,article_content,OCCURENCE_SCORE)

    else:

        article_content_words = article_content.lower().split(" ")
        article_content_words

        score_1 = article_content_words.count(word)
        score_2 = article_content_words.count(word.lower())
        score_3 = article_content_words.count(word.upper())
        score_4 = article_content_words.count(word.title())

        score = score_1 + score_2 + score_3 + score_4

    return (score * OCCURENCE_SCORE)

        
            
        
    
    
def do_rank(url,rank_obj, content, title_content, meta_tag_content, h1_tag_content):
   # rank_obj = RankedWord.RankedWord(word,isPos,score)

    word = rank_obj.getword()

    #req= requests.get(url)  #get the url request
    #soup = BeautifulSoup(req.text,"lxml") #parse it through BeautifulSoup
    #initialise the variables to hold the rank values
    url_score = 0
    title_score = 0
    meta_score = 0
    h1_score = 0
    occurances_score = 0
    pos_score = 0
    
    url_score = calculate_url_score(url,word)

    title_score = calculate_title_score(word, title_content)
    
    meta_score =  calculate_meta_score(word, meta_tag_content)

    h1_score = calculate_h1_score(word, h1_tag_content)

    occurances_score = calculate_occurances_score(word,content)
    
    no_of_token_score = 0
    no_of_token_score = calculate_nof_token(word)
    print(no_of_token_score)
    
    if rank_obj.isPos == True:
        pos_score = POS_SCORE

    additional_meta_score = 0

    if pos_score != 0 and title_score != 0:
        additional_meta_score = 50
    #total rank
    
    
    total_rank = url_score + additional_meta_score + no_of_token_score +title_score + meta_score + h1_score + occurances_score + pos_score
    rank_obj.score = total_rank;
    """ if((pos_score > 0) and (title_score > 0) and occurances_score > 10):
        rank_obj.score = 10;
    elif((pos_score > 0) and (title_score > 0)):
        rank_obj.score = 9;
    elif((pos_score == 0) and (title_score > 0)):
        rank_obj.score = 9;
    elif((pos_score > 0) and (h1_score > 0 or meta_score > 0)):
        rank_obj.score = 9;
    elif((pos_score > 0) and (additional_meta_score > 0)):
        rank_obj.score = 8;
    elif((pos_score > 0) and (occurances_score > 10)):
        rank_obj.score = 7;
    elif((pos_score > 0) and (no_of_token_score > 0)):
        rank_obj.score = 6;
    elif((pos_score == 0) and (h1_score > 0 or meta_score > 0)):
        rank_obj.score = 5;
    elif((pos_score == 0) and (additional_meta_score > 0)):
        rank_obj.score = 4;
    elif((pos_score > 0) and (occurances_score >10)):
        rank_obj.score = 3;
    elif((pos_score == 0) and (no_of_token_score > 0)):
        rank_obj.score = 2;
    elif((pos_score == 0) and (occurances_score >10)):
        rank_obj.score = 1;"""
    #print("url_score,additional_meta_score,no_of_token_score,title_score,meta_score,h1_score,occurances_score,pos_score")
    #print(url_score,additional_meta_score,no_of_token_score,title_score,meta_score,h1_score,occurances_score,pos_score)
    print(word, " : url : ", url_score, ", title : ", title_score, ", meta : ", meta_score, ", h1 : ", h1_score, ", occurence : ", occurances_score,
          ", pos : ", pos_score, ", additional : ", additional_meta_score, " no_of_token_score : ", no_of_token_score);
    print("Total ", total_rank);
    
    #rank_obj.score = total_rank

    return rank_obj


#url = "https://www.nytimes.com/2017/11/16/nyregion/senator-robert-menendez-corruption.html"#
#rank_obj = RankedWord.RankedWord("menendez corruption",True)
#do_rank(url,rank_obj)
#print(rank_obj.score)
