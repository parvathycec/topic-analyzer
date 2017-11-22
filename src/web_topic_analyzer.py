"""
@summary: Controller class which calls all functions to 
execute steps of the algorithm
This class object is called from project_ui.py to
run the analyzer for the given input.
@author: Parvathy
"""
import content_extraction, html_parser
import noun_extractor
import k_means_grouper
import operator
import ranking

class WebTopicAnalyzer:
    """Analyzer to analyze the topics related to a web page"""
    def __init__(self, url):
        self.__url = url;
    
    def process(self):
        #step 1: get text content and title
        title, content = content_extraction.get_text(self.__url);
        print(content);
        #step 2: Get all title, h1, meta tags of the web page.
        title_content, meta_content, h1_tag_content = html_parser.parse_html(self.__url);
        print("Title content : ", title_content);
        print("Meta Content : ", meta_content);
        print("H1 Tag content : ", h1_tag_content);
        #step 3: get noun words and phrases (from wiki search)
        nouns = noun_extractor.get_nouns(title, content);
        #step 4: ranking - giving scores to each word based on several factors.
        ranked_words = [];
        for w in nouns:
            ranked_word = ranking.do_rank(self.__url, w, content, title_content, meta_content, h1_tag_content);
            ranked_words.append(ranked_word);
        #print("Lets see before grouping : ");
        #step 4: grouping of similar phrases and  eliminating repetition for more diverse keywords
        words, clusters = k_means_grouper.get_clusters(ranked_words);
        #print("CLUSTERS >> ", clusters)
        #print("After grouping : ");
        #for w in words:
        #    print("Not in Cluster : ", w.getword());
        cluster_count = 0;
        #for cluster in clusters:
        #    cluster_count += 1;
        #    for data in cluster:
        #        print("In cluster ", cluster_count, " Data : ", data.getword());
        final_ranked_words = [];
        #Add all keywords that did not have a match in dataset and hence cannot be grouped.
        final_ranked_words.extend(words)
        #sort each data clused based on ranks and get the highest ranked data from a cluster
        for data_cluster in clusters:
            data_cluster.sort(key=operator.attrgetter('score'), reverse=True)
            #Taking the most ranked word of the cluster
            final_ranked_words.append(data_cluster[0]);
        print("------------TOP 15--------------")
        #sort the final list of ranked words
        final_ranked_words.sort(key=operator.attrgetter('score'), reverse=True)
        count = 0;
        key_words = [];
        #Will show first 15 ranked keywords
        for rw in final_ranked_words:
            count += 1;
            print(rw.getword().title(), " ", rw.getscore());
            if len(key_words) == 15:
                break;
            else:
                key_words.append(rw.getword().upper());
        return key_words;