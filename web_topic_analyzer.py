from crawler import content_extraction
from chunker import noun_extractor
from grouping import k_means
import operator
from ranking import ranking_v2, RankedWord

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
        #step 3: ranking
        ranked_words = [];
        for w in nouns:
            ranked_word = ranking_v2.do_rank(self.url, w);
            ranked_words.append(ranked_word);
        #step 4: grouping of similar phrases and  eliminating repetition
        words, clusters = k_means.get_clusters(ranked_words);
        print("CLUSTERS >> ", clusters)
        final_ranked_words = [];
        final_ranked_words.extend(words)
        for data_cluster in clusters:
            data_cluster.sort(key=operator.attrgetter('score'), reverse=True)
            #Taking the most ranked word of the cluster
            final_ranked_words.append(data_cluster[0]);
        print("------------TOP 5--------------")
        final_ranked_words.sort(key=operator.attrgetter('score'), reverse=True)
        for rw in final_ranked_words:
            print(rw.getword().upper(), " ", rw.getscore());
        
        

website_url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
analyzer = WebTopicAnalyzer(website_url);
analyzer.process();
