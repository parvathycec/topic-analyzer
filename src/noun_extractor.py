#Step 2 of the algorithm
#Uses third party library called Spacy and wikipedia
#Spacy identifies nouns as potential keywords from the content
#For each identified noun word, we do a search in 
#wikipedia to get some search results.
#If any of the search result is in article content, that phrase is 
#taken as a potential keyword too. 
import spacy
import wikipedia
from ranked_word import RankedWord
from time import sleep

def get_nouns(title, content):
    """Get all noun chunks from the text extracted from website
    and get related word phrases from wikipedia search"""
    nlp = spacy.load('en');#,vectors='en_google')
    content = title + " " + content;
    print(content);
    doc = nlp(content)
    dict_nouns = {};
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
          token.shape_, token.is_alpha, token.is_stop, token.ent_type_)
        #heuristics : Fine tuning candidates
        #Candidates are chosen with this algorithm:
        #1) If word is a proper noun and not too short word length 
        #2)If word is a noun that is not too short and not belonging to WH words like who, what, where.
        #3)We dont need Date nouns.
        #4)We dont want proper nouns who dont have a definite entity type.
        if (token.pos_ == 'PROPN' and len(token.text) > 2 and token.ent_type_ != "") or \
        (token.pos_ == 'NOUN' and token.tag_ != 'WP' and len(token.text) > 3):
            if(token.ent_type_ != 'DATE'):
                wr = RankedWord(token.text.lower(), (token.pos_ == 'PROPN'))
                if (wr.getword() not in dict_nouns):
                    dict_nouns [wr.getword()] = wr;
                    print("Putting from Spacy  : ", wr.getword());
            elif token.text.lower() in dict_nouns:
                print("Deleting from Spacy  2 : ", token.text.lower());
                del dict_nouns[token.text.lower()];
        elif token.text.lower() in dict_nouns:
            print("Deleting from Spacy  2 : ", token.text.lower());
            del dict_nouns[token.text.lower()];#remove if it is not a noun in another context
    
    #once we get noun candidates (individual words), we search wiki articles to 
    #see if there is any related word phrase results that is also 
    #present in our web-content
    wiki_results = {};
    for noun in dict_nouns.values():
        print("Noun Candidate : ", noun)
        #if(not noun.isPos):
        #    print("No wiki search for non-proper noun");
        #    continue;
        try:
            wiki_result = wikipedia.search(noun.getword(), results=20);
        except:#sometimes, connection is refused because our application exceeds maximum trys.
            #So sleep for 5 seconds before doing next search.
            sleep(5);
            continue;
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
            if len(topics) > 1  and (wiki_topic.lower() in content.lower() or wiki_topic.lower()+" " in content.lower()):
                if (wiki_topic == noun.getword()):#avoid duplicates
                    continue;
                #Dont want cases like "The Case" where we get a result as "The <existing_noun_candidate"
                if(len(topics) == 2 and topics[0] == "the"):
                    continue;
                wiki_results[wiki_topic.lower().rstrip().lstrip()] = RankedWord(wiki_topic.lower().rstrip().lstrip(), noun.isPos);
                print("Putting from Wiki : ", wiki_topic.lower().rstrip().lstrip());
            elif (',' in wiki_topic) and any(t in content.lower() for t in wiki_topic.lower().split(",")):
                phrases = wiki_topic.lower().split(",");
                for phrase in phrases:
                    if phrase in content.lower():
                        print(phrase, " ", all(t in dict_nouns.keys() for t in phrase.split()));
                        for ph in phrase.split():
                            if ph in dict_nouns and dict_nouns[ph].isPos:
                                wiki_results[phrase.lstrip().rstrip()] = RankedWord(phrase.lstrip().rstrip(), noun.isPos);
                                print("Putting from Wiki 2 : ", phrase.lstrip().rstrip());
                                break;
    #Removing nouns already in wiki:
    for wiki_val in wiki_results.keys():
        for val in wiki_val.split():
            for nn in list(dict_nouns):
                if val == nn:
                    del dict_nouns[nn];
                    print("Deleting from Spacy 3 : ", wr.getword());
    return list(dict_nouns.values())+list(wiki_results.values());
