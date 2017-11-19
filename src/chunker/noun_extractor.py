import spacy
import wikipedia
from ranking.RankedWord import RankedWord

def get_nouns(content):
    """Get all noun chunks from the text extracted from website
    and get related word phrases from wikipedia search"""
    nlp = spacy.load('en');#,vectors='en_google')
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
        if (token.pos_ == 'PROPN' and len(token.text) > 2) or \
        (token.pos_ == 'NOUN' and token.tag_ != 'WP' and len(token.text) > 3):
            if(token.ent_type_ != 'DATE'):
                wr = RankedWord(token.text.lower(), (token.pos_ == 'PROPN'))
                if (wr.getword() not in dict_nouns):
                    dict_nouns [wr.getword()] = wr;
        elif token.text.lower() in dict_nouns:
            del dict_nouns[token.text.lower()];#remove if it is not a noun in another context
    
    #once we get noun candidates (individual words), we search wiki articles to 
    #see if there is any related word phrase results that is also 
    #present in our web-content
    wiki_results = {};
    for noun in dict_nouns.values():
        print("Noun Candidate : ", noun)
        wiki_result = wikipedia.search(noun.getword(), results=20);
        #print("Wiki : ", wiki_result);
        for wiki_topic in wiki_result:
            wiki_topic = wiki_topic.lower();
            print("wiki_topic ", wiki_topic);
            topics = wiki_topic.split();
            #for easier comparison, converting to lower case
            #We need only phrases here, don't need words as it would be duplicate
            #Checking if the phrase is in the web content.
            #Ex: We will have words Statue and Liberty in noun array, 
            #Wiki results will get the phrase Statue of Liberty and if it is in web page, 
            #this phrase is a potential candidate
            #https://en.wikipedia.org/wiki/Wikipedia:Article_titles#Deciding_on_an_article_title
            if len(topics) > 0  and (wiki_topic.lower() in content.lower()):
                if (wiki_topic == noun.getword()):#avoid duplicates
                    continue;
                #Dont want cases like "The Case" where we get a result as "The <existing_noun_candidate"
                if(len(topics) == 2 and topics[0] == "the"):
                    continue;
                #IF first word and last word are both proper nouns, consider it a candidate
                #We don't need cases like "by chance" coming up.
                #Need to revist
                first_w = None;
                last_w = None;
                if(topics[0] in dict_nouns):
                    first_w = dict_nouns[topics[0]]
                if(topics[-1] in dict_nouns):
                    last_w = dict_nouns[topics[-1]]
                if (first_w and last_w):
                    if (first_w.isPos and  last_w.isPos):
                        print("Wiki Candidate >> ", wiki_topic);
                        #Need to revist : Pos True or give separate variable wiki true
                        wiki_results[wiki_topic.lower()] = RankedWord(wiki_topic.lower(), True);
            elif (',' in wiki_topic) and any(t in content.lower() for t in wiki_topic.lower().split(",")):
                phrases = wiki_topic.lower().split(",");
                for phrase in phrases:
                    if phrase in content.lower():
                        print(phrase, " ", all(t in dict_nouns.keys() for t in phrase.split()));
                        for ph in phrase.split():
                            if ph in dict_nouns and dict_nouns[ph].isPos:
                                wiki_results[phrase.lstrip().rstrip()] = RankedWord(phrase.lstrip().rstrip(), True);
                                break;
    #Removing nouns already in wiki:
    for wiki_val in wiki_results.keys():
        for val in wiki_val.split():
            for nn in list(dict_nouns):
                if val == nn:
                    del dict_nouns[nn];
    return list(dict_nouns.values())+list(wiki_results.values());
