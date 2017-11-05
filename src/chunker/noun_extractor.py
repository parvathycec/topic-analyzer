import spacy
import wikipedia
from crawler import content_extraction

website_url = "https://www.yahoo.com/news/sister-york-attack-suspect-says-may-brainwashed-appeals-162102000.html"#"http://news.bbc.co.uk/2/hi/health/2284783.stm"

def get_nouns():
    """Get all noun chunks from the text extracted from website"""
    nlp = spacy.load('en')
    handle = content_extraction.get_text(website_url);#htmlParser(website_url);
    sentence = "";
    for line in handle:
        sentence += line
    doc = nlp(sentence)
    noun_chunks = []
    for word in doc:
        print(word.text, word.lemma, word.lemma_, word.tag, word.tag_, word.pos, word.pos_)
    print(doc.noun_chunks)
    for noun_word in doc.noun_chunks:
        #no need for pronouns like he,him,her etc
        if noun_word.lemma_ == '-PRON-':
            continue;
        #print(noun_word.text);
        noun_chunks.append(noun_word.text);
            
    noun_chunks_extension = [];
    for noun in noun_chunks:
        print("For noun : ", noun)
        related_topics = wikipedia.search(noun, results=3);
        #print("Noun : ", noun);
        for topic in related_topics:
            if topic in sentence:
                #print("Topic >> ", topic);
                noun_chunks_extension.append(topic);
    return set(noun_chunks+noun_chunks_extension);

for val in get_nouns():
    print(val)
            