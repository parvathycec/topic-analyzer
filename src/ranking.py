'''This py is to implement the ranking algorithm '''
import ranked_word  #import the class file

#score values
URL_SCORE = 100 #if the word/phrase is found in the URL of the webpage
TITLE_SCORE = 100 #if the word/phrase is found in the title of the webpage
H1_SCORE = 100#if the word/phrase is found in the h1 tag of the webpage
META_SCORE = 100 #if it is found in the meta tag of the webpage
OCCURENCE_SCORE = 5# total number of occurences
POS_SCORE = 100 # if it is phrase
NO_OF_TOKENS =100 #total number of words




def check_for_consecutive_numbers(List):
    ''' helper function to check if the numbers in the list are consecutive or not'''
    ''' used the formula, if the numbers are consecutive: then len(list ) == max - min + 1 and no duplicates'''
    if len(List) == (max(List) - min(List) + 1):
        if len(List) == len(set(List)):
            return True
        else:
            return False
    else:
        return False

def calculate_rank(key,content,total_rank):
'''helper function which used to find whether the given word is in the given content or not; Accordinly it assigns a rsnk to the given word '''
    rank =0
    content = content.split(" ") #the given content is split 
    content = [x.lower() for x in content] #convert all the words into lower case
    content = [x.replace(",","") for x in content] # remove the , and .
    content = [x.replace(".","") for x in content]
    
    indices = []
    if " " in key: #if it is a phrase 
        phrases = key.split(" ") #split the phrase
        for p in phrases:  #for all the words in the phrase, convert to lower and get its index
            if p.lower() in content: #check whether the lower case word of the phrase is in the content
                indices.append(content.index(p.lower())) #if it is there, append its index

            
            else: #if any one of the word in the phrase is not in the content, then rank == 0
                return 0
        #check if it is a consecutive number
        # two conditions to be checked, n(len of the list) == max(list) - min(list) + 1 and no duplicates
        #this is mainly to avoid the following kind of cases: the given phrase : dual challenges, but in the content we have: induvidual challenges. 
        if (check_for_consecutive_numbers(indices) == True): #the indices returned should be consecutive
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
    #print("TITLE : ", title_content);
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
    #print(no_of_token_score)
    
    if rank_obj.isPos == True:
        pos_score = POS_SCORE

    additional_meta_score = 0

    if pos_score != 0 and title_score != 0:
        additional_meta_score = 50
    #total rank
    
    
    total_rank = url_score + additional_meta_score + no_of_token_score +title_score + meta_score + h1_score + occurances_score + pos_score
    rank_obj.score = total_rank;

    #print("url_score,additional_meta_score,no_of_token_score,title_score,meta_score,h1_score,occurances_score,pos_score")
    #print(url_score,additional_meta_score,no_of_token_score,title_score,meta_score,h1_score,occurances_score,pos_score)
    #print(word, " : url : ", url_score, ", title : ", title_score, ", meta : ", meta_score, ", h1 : ", h1_score, ", occurence : ", occurances_score,
     #     ", pos : ", pos_score, ", additional : ", additional_meta_score, " no_of_token_score : ", no_of_token_score);
    #print("Total ", total_rank);
    
    #rank_obj.score = total_rank

    return rank_obj

if __name__ == '__main__':
    print("This file can only be imported!")

