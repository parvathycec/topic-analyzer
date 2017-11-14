import requests
from bs4 import BeautifulSoup
import RankedWord  #import the class file

url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'

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
    rank_obj = RankedWord.RankedWord(word,score)
    
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
           
    #check whether the word occurs in the meta data and assign rank
    meta_rank = check_all_cases_rank(word,meta_content,5)

    #get the total text and avoid the tags
    text = soup.text

    each_word = text.split(" ")
    
    
    #calculate the occurences of the word in the entire webpage
    
    no_of_occurences_lower_case = each_word.count(word.lower())
    no_of_occurences_upper_case = each_word.count(word.upper())
    no_of_occurences_title_case = each_word.count(word.title())
     
    #check for mixed cases
    if word.isupper ==  False:
        if word.islower == False:
            if word.istitle == False:
                no_of_occurences_mixed_case = text.count(word)

    
    
    no_of_occurences = no_of_occurences_lower_case + no_of_occurences_upper_case + no_of_occurences_title_case + no_of_occurences_mixed_case
    
    
    occurences_rank = no_of_occurences

    #check whether the word appears in the url and assign rank accordingly
    url_rank = check_all_cases_rank(word,url,5)
    
    #find the h1 content of the webpage

    for h1_tag in soup.find_all("h1"):
        h1_tag_content = h1_tag.string

    #if the word appears in the h1, then assign rank accordingly
    h1_tag_rank = check_all_cases_rank(word,h1_tag_content,10)

    #total rank
    total_rank = title_rank + meta_rank + url_rank + occurences_rank + h1_tag_rank
    
    
    rank_obj.score = total_rank

    return rank_obj


r = do_rank(url,"wiki")

print(r.getword())
print(r.getscore())
