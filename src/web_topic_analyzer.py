from crawler import content_extraction, html_parser1
from chunker import noun_extractor
from grouping import k_means
import operator
from ranking import ranking_v2
import datetime

class WebTopicAnalyzer:
    """Analyzer to analyze the topics related to a web page"""
    def __init__(self, url):
        self.__url = url;
    
    def process(self):
        #step 1: get content
        content = content_extraction.get_text(self.__url);
        print(content);
        #step 2: Get all title, h1, meta tags of the web page.
        title_content, meta_content, h1_tag_content = html_parser1.parse_html(self.__url);
        print("Title content : ", title_content);
        print("Meta Content : ", meta_content);
        print("H1 Tag content : ", h1_tag_content);
        #step 3: get NOUN word or phrases
        nouns = noun_extractor.get_nouns(content);
        #step 4: ranking - giving scores to each word based on several factors.
        ranked_words = [];
        for w in nouns:
            ranked_word = ranking_v2.do_rank(self.__url, w, content, title_content, meta_content, h1_tag_content);
            ranked_words.append(ranked_word);
        #print("Lets see before grouping : ");
        for w in ranked_words:
            print(w.getword());
        #step 4: grouping of similar phrases and  eliminating repetition
        words, clusters = k_means.get_clusters(ranked_words);
        #print("CLUSTERS >> ", clusters)
        #print("After grouping : ");
        #for w in words:
        #    print("Not in Cluster : ", w.getword());
        cluster_count = 0;
        for cluster in clusters:
            cluster_count += 1;
            for data in cluster:
                print("In cluster ", cluster_count, " Data : ", data.getword());
        final_ranked_words = [];
        final_ranked_words.extend(words)
        for data_cluster in clusters:
            data_cluster.sort(key=operator.attrgetter('score'), reverse=True)
            #Taking the most ranked word of the cluster
            final_ranked_words.append(data_cluster[0]);
        print("------------TOP 15--------------")
        final_ranked_words.sort(key=operator.attrgetter('score'), reverse=True)
        count = 0;
        #Will show first 15 for now
        for rw in final_ranked_words:
            count += 1;
            print(rw.getword().title(), " ", rw.getscore());
            if count == 15:
                break;

a = datetime.datetime.now()
website_url = "http://www.foxnews.com/politics/2017/11/18/trump-calls-clinton-biggest-loser-all-time-after-contests-election-loss.html"

analyzer = WebTopicAnalyzer(website_url);
try:
    analyzer.process();
except Exception as ex:
    print(ex);
    #TODO: How to show error message in ui
    
b = datetime.datetime.now()
c = b - a
print("Total time taken : ", c.seconds, " seconds")
