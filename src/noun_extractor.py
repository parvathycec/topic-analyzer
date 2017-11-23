'''
@summary: Step 2 of the algorithm:
Extracts nouns from the content of the article and get related
keywords from wikipedia.
Uses third party libraries Spacy and wikipedia.
Spacy identifies nouns from the content,
For each identified noun word, we do a search in wikipedia to 
get 20 search results.
If any of the search result is in article content, that phrase is 
taken as a potential keyword along with the noun.
@author: Parvathy 
'''

import copy
from itertools import combinations
from time import sleep

import spacy
import wikipedia

from ranked_word import RankedWord


nlp = spacy.load('en');

def get_nouns(title, content):
    """Get all noun chunks from the text extracted from website
    and get related word phrases from wikipedia search"""
    article_content = title + " " + content;
    #print(article_content);
    dict_nouns = extract_nouns(article_content);
    #once we get noun candidates (individual words), we search wiki articles to 
    #see if there is any related word phrase results that is also 
    #present in our web-content
    wiki_results = {};
    for noun in dict_nouns.values():
        print("Noun Candidate : ", noun)
        #if noun.isPos:
        print("Going for wiki");
        wiki_phrase = search_wiki(noun, article_content, dict_nouns);
        if wiki_phrase is not None:
            wiki_results[wiki_phrase.rstrip().lstrip()] = RankedWord(wiki_phrase.rstrip().lstrip(), noun.isPos);
  #  noun_chunks = extract_title_nouns(title);
    #To merge two dictionaries
    #Reference: https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression
   # wiki_results.update(noun_chunks);
    #Removing nouns already in wiki:
    remove_duplicates(dict_nouns, wiki_results);
    wiki_results_copy = copy.deepcopy(wiki_results)
    remove_duplicates(wiki_results, wiki_results_copy);
    
    return list(dict_nouns.values())+list(wiki_results.values());

def extract_title_nouns(title):
    noun_chunks = {};
    doc_title = nlp(title.replace("'", ' '));
    for chunk in list(doc_title.noun_chunks):
        chunk = chunk.text.rstrip().lstrip().lower();
        noun_chunk = RankedWord(chunk, False);
        noun_chunks[chunk] = noun_chunk;
    #print("Noun Chunk ", list(doc_title.noun_chunks));
    return noun_chunks;



def extract_nouns(article_content):
    """Gets nouns in the article content using Spacy"""
    #load spacy for English
    doc = nlp(article_content)
    dict_nouns = {};
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
          token.shape_, token.is_alpha, token.is_stop, token.ent_type_)
        isCapitalToken = token.text.isupper();
        #heuristics : Fine tuning candidates
        #Candidates are chosen with this algorithm:
        #1) If word is a proper noun and not too short word length 
        #2)If word is a noun that is not too short and not belonging to WH words like who, what, where.
        #3)We don't need Date nouns.
        #4)We don't want proper nouns who don't have a definite entity type.
        if (token.pos_ == 'PROPN' and len(token.text) > 2 and token.ent_type_ != "") or \
        (token.pos_ == 'NOUN' and token.tag_ != 'WP' and len(token.text) > 3):
            if(token.ent_type_ != 'DATE' and token.ent_type_ != 'TIME'):
                wr = RankedWord(token.text.rstrip().lstrip().lower(), (token.pos_ == 'PROPN'), isUpper = isCapitalToken)
                if (wr.getword() not in dict_nouns):
                    dict_nouns [wr.getword()] = wr;
            elif token.text.rstrip().lstrip().lower() in dict_nouns:
                del dict_nouns[token.text.rstrip().lstrip().lower()];
        elif token.text.rstrip().lstrip().lower() in dict_nouns:
            del dict_nouns[token.text.rstrip().lstrip().lower()];#remove if it is not a noun in another context
    return dict_nouns;


def search_wiki(noun, article_content, dict_nouns):
    """Search wikipedia for articles with noun keyword in title"""
    try:
        wiki_result = wikipedia.search(noun.getword(), results=50);
    except Exception as e:#sometimes, connection is refused because our application exceeds maximum trys.
        #So sleep for 5 seconds before doing next search.
        sleep(5);
        print(e);
        return None;
    else:
        #print("Wiki : ", wiki_result);
        for wiki_topic in wiki_result:
            wiki_topic = wiki_topic.lower();
           # print("wiki_topic ", wiki_topic);
            topics = wiki_topic.split();
            #for easier comparison, converting to lower case
            #We need only phrases here, don't need words as it would be duplicate
            #Checking if the phrase is in the web content.
            #Ex: We will have words Statue and Liberty in noun array, 
            #Wiki results will get the phrase Statue of Liberty and if it is in web page, 
            #this phrase is a potential candidate
            #https://en.wikipedia.org/wiki/Wikipedia:Article_titles#Deciding_on_an_article_title
            if len(topics) > 1  and (" "+wiki_topic.lower() in article_content.lower() or " "+wiki_topic.lower()+" " in article_content.lower()):
                if (wiki_topic == noun.getword()):#avoid duplicates
                    return None;
                #Dont want cases like "The Case" where we get a result as "The <existing_noun_candidate"
                if(len(topics) == 2 and topics[0] == "the"):
                    return None;
                return wiki_topic.lower().rstrip().lstrip();
            elif (',' in wiki_topic) and any(t in article_content.lower() for t in wiki_topic.lower().split(",")):
                phrases = wiki_topic.lower().split(",");
                for phrase in phrases:
                    if phrase.lstrip().rstrip() in article_content.lower().split():
                        for ph in phrase.split():
                            if ph in dict_nouns and dict_nouns[ph].isPos and (len(ph.split()) > 1):
                                return phrase.lstrip().rstrip();
                    
        
                            

def remove_duplicates(dict_nouns, wiki_results):
    """Remove nouns which are added as wiki phrases"""
    for wiki_val in wiki_results.keys():
        arr = wiki_val.split();
        for i in range(0,len(arr)):
            wiki_val_arr = wiki_val.split()[i:len(arr)];
            for i in range(1, len(wiki_val_arr)+1):
                iter_k = combinations(wiki_val_arr, i)
                curr_combination = ' '.join(iter_k.__next__());
                for nn in list(dict_nouns):
                    if curr_combination.rstrip().lstrip() == nn.rstrip().lstrip() and (curr_combination.rstrip().lstrip() != wiki_val.rstrip().lstrip()):
                        del dict_nouns[nn.rstrip().lstrip()];
