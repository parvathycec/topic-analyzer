from crawler import content_extraction
from chunker import noun_extractor
from grouping import k_means
import operator

class WebTopicAnalyzer:
    """Analyzer to analyze the topics related to a web page"""
    def __init__(self, url):
        self.url = url;
    
    def process(self):
        #step 1: get content
        content = content_extraction.get_text(self.url);
        print(content);
        #step 2: get NOUN word or phrases
        nouns = noun_extractor.get_nouns(content);
        #step 3: grouping of similar phrases and  eliminating repetition
        clusters = k_means.get_clusters(nouns);
        print(clusters)
        #step 4: ranking
        #ranked_words = [];
        #for word_phrase in clusters:
        #    ranked_word = RankedWord.RankedWord(word_phrase);
        #    tester.count_of_occurence(ranked_word, content);
        #    ranked_words.append(ranked_word);
        #ranked_words.sort(key=operator.attrgetter('score'), reverse=True)
        #print("------------TOP 5--------------")
        #for ranked_word in ranked_words:
        #    print(ranked_word.word_phrase.upper());
        
        

website_url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
analyzer = WebTopicAnalyzer(website_url);
analyzer.process();
