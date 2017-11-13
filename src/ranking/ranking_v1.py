import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'

def check_all_cases_rank(key,content,total_rank):
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

    req= requests.get(url)
    soup = BeautifulSoup(req.text,"lxml")
    
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
    
    title_rank = check_all_cases_rank(word,title_content,5)
    
    meta_content = ""
    for meta_tag in soup.findAll("meta"):
       meta_con =  meta_tag.get("content",None)
       if meta_con != None:
           meta_content += meta_con + " "

    meta_rank = check_all_cases_rank(word,meta_content,5)
    
    text = soup.get_text()
    

    no_of_occurences_lower_case = text.count(word.lower())
    no_of_occurences_upper_case = text.count(word.upper())
    no_of_occurences_title_case = text.count(word.title())

    if word.isupper ==  False:
        if word.islower == False:
            if word.istitle == False:
                no_of_occurences_mixed_case = text.count(word())
    
    no_of_occurences = no_of_occurences_lower_case + no_of_occurences_upper_case + no_of_occurences_title_case + no_of_occurences_mixed_case
    
    
    occurences_rank = no_of_occurences

    url_rank = check_all_cases_rank(word,url,5)
    
    

    for h1_tag in soup.find_all("h1"):
        h1_tag_content = h1_tag.string

    h1_tag_rank = check_all_cases_rank(word,h1_tag_content,10)
    
    total_rank = title_rank + meta_rank + url_rank + occurences_rank + h1_tag_rank
    
    

    
    return word,title_rank,meta_rank,url_rank,occurences_rank,h1_tag_rank,total_rank


print(do_rank(url,"python"))


        
    
    
