import requests
from bs4 import BeautifulSoup
import RankedWord  #import the class file
from __init__ import URL_SCORE 

#url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
url = "https://stackoverflow.com/questions/23238352/create-object-from-class-in-separate-file"
url1 = "https://stackoverflow.com/questions/33176278/beautifulsoup-find-all-occurrences-of-specific-text"
url2 = "https://www.nytimes.com/2017/11/14/us/politics/jeff-sessions-congress-russia.html"

def check_all_cases_rank(key,content,total_rank):

    #this function checks for the key in the respective content across all the cases and assigns the rank
    rank = 0
    if key in content:
        rank = total_rank
    elif key.lower() in content:
        rank = total_rank
    elif key.upper() in content:
        rank = total_rank
    elif key.title() in content:
        rank = total_rank

    return rank
        

def do_rank(url,word):
    score = 0
    isPos = True 
    rank_obj = RankedWord.RankedWord(word,isPos,score)

    print(URL_SCORE)
    
    req= requests.get(url)  #get the url request
    soup = BeautifulSoup(req.text,"lxml") #parse it through BeautifulSoup
    #initialise the variables to hold the rank values
    
    title_rank = 0
    meta_rank = 0
    url_rank = 0
    occurences_rank = 0
    no_of_occurences = 0
    no_of_occurences_lower_case = 0
    no_of_occurences_upper_case = 0
    no_of_occurences_title_case = 0
    no_of_occurences_mixed_case = 0
    h1_tag_rank = 0

    #get the title content
    title_content = soup.title.string

    #check whether the word occurs in the title and assign rank
    title_rank = check_all_cases_rank(word,title_content,5)

    
    meta_content = ""
    for meta_tag in soup.findAll("meta"):
       meta_con =  meta_tag.get("content",None)
       if meta_con != None:
           meta_content += meta_con + " "

    print(meta_content)
           
    #check whether the word occurs in the meta data and assign rank
    meta_rank = check_all_cases_rank(word,meta_content,5)

    #get the total text and avoid the tags
    text = soup.text

    each_word = text.split(" ")
    
    #print(each_word)
    
    #calculate the occurences of the word in the entire webpage
    
    no_of_occurences_lower_case = each_word.count(word.lower())
    print(no_of_occurences_lower_case)
    no_of_occurences_upper_case = each_word.count(word.upper())
    no_of_occurences_title_case = each_word.count(word.title())
    print(no_of_occurences_title_case)
    #check for mixed cases
    if word.isupper() ==  False:
        if word.islower() == False:
            if word.istitle() == False:
                no_of_occurences_mixed_case = each_word.count(word)

    
    
    no_of_occurences = no_of_occurences_lower_case + no_of_occurences_upper_case + no_of_occurences_title_case + no_of_occurences_mixed_case
    
    
    occurences_rank = no_of_occurences

    #check whether the word appears in the url and assign rank accordingly
    url_rank = check_all_cases_rank(word,url,5)
    print(url_rank)
    
    #find the h1 content of the webpage
    h1_tag_content = None
    for h1_tag in soup.find_all("h1"):
        h1_tag_content = h1_tag.string
        
    print(h1_tag_content)
    

    #if the word appears in the h1, then assign rank accordingly
    if h1_tag_content != None:
        h1_tag_rank = check_all_cases_rank(word,h1_tag_content,10)
        
    pos_score = 0
    if rank_obj.isPos == "True":
        pos_score = 50
        
    #total rank
    total_rank = title_rank + meta_rank + url_rank + occurences_rank + h1_tag_rank + pos_score
    print(occurences_rank)
    
    rank_obj.score = total_rank

    return rank_obj


r = do_rank(url2,"jeff")

print(r.getword())
print(r.getscore())
