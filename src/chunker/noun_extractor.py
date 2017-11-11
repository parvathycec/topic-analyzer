import spacy
import wikipedia

#TODO:
#1. More fine tuning of candidates
#2. Change the spacy default loading to vector loading     
#3. How to remove similar candidates like "Donald" and "Donald Trump"       
def get_nouns(content):
    """Get all noun chunks from the text extracted from website
    and get related values from wiki"""
    nlp = spacy.load('en');#,vectors='en_google')
    doc = nlp(content)
    noun_candidates = []
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
          token.shape_, token.is_alpha, token.is_stop, token.ent_type_)
        #heuristics : Fine tuning candidates
        if (token.pos_ == 'PROPN' and len(token.text) > 2) or \
        (token.pos_ == 'NOUN' and token.tag_ != 'WP' and len(token.text) > 3):
            if(token.ent_type_ != 'DATE'):
                #short nouns does not make sense, we can remove them.
                #Date words like November does not make sense
                noun_candidates.append(token.text.lower());
    #once we get noun candidates (individual words), we search wiki articles to 
    #see if there is any relates word phrase results that is also 
    #present in our web-content
    wiki_results = [];
    for noun in noun_candidates:
        print("Noun Candidate : ", noun)
        wiki_result = wikipedia.search(noun, results=20);
        #print("Wiki : ", wiki_result);
        for topic in wiki_result:
            #TODO: Look for a combination of words in topic
            if len(topic.split()) > 0 and len(topic) > 3 and (topic.lower() in content.lower()):
                if topic.lower() == noun.lower():
                    continue;
                print("Wiki Candidate >> ", topic);
                wiki_results.append(topic.lower());
    return set(noun_candidates+wiki_results);
