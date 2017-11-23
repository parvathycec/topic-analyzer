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
from nltk.tokenize import word_tokenize


class WebTopicAnalyzer:
    """Analyzer to analyze the topics related to a web page"""
    def __init__(self, url):
        self.__url = url;
    
    def process(self):   
        try:
            #step 1: get text content and title
            print("INFO: Getting the text content of web page.");
            title, content = content_extraction.get_text(self.__url);
            if (title == None or content == None):
                raise ValueError("Could not retrieve text data.");
            #gen_docs = [w.lower() for w in word_tokenize(content)] 
            #token_relevance = k_means_grouper.get_relevance(gen_docs);
            #step 2: Get all title, h1, meta tags of the web page.
            print("INFO: Getting the title, meta and h1 tag content of web page.");
            title_content, meta_content, h1_tag_content = html_parser.parse_html(self.__url);
            #step 3: get noun words and phrases (from wiki search)
            print("INFO: Extracting single word nouns from text content and searching related phrases from wikipedia articles.");
            print("INFO: This might take a few seconds.");
            nouns = noun_extractor.get_nouns(title, content);
            #step 4: ranking - giving scores to each word based on several factors.
            print("INFO: Ranking words and phrases based on factors like occurence, frequency etc.");
            ranked_words = [];
            for w in nouns:
                ranked_word = ranking.do_rank(self.__url, w, content, title_content, meta_content, h1_tag_content);
                ranked_words.append(ranked_word);
            #step 4: grouping of similar phrases and  eliminating repetition for more diverse keywords
            print("INFO: Grouping similar words to clusters and getting the most ranked words from each cluster");
            print("INFO: This might take a few seconds.");
            words, clusters = k_means_grouper.get_clusters(ranked_words);
            cluster_count = 0;
            final_ranked_words = [];
            #Add all keywords that did not have a match in dataset and hence cannot be grouped.
            final_ranked_words.extend(words)
            #sort each data clused based on ranks and get the highest ranked data from a cluster
            for data_cluster in clusters:
                data_cluster.sort(key=operator.attrgetter('score'), reverse=True)
                #Taking the most ranked word of the cluster
                final_ranked_words.append(data_cluster[0]);
            #for k in final_ranked_words:
            #    sum = 0;
            #    for each_k in k.getword().split():
            #        print("each_k ", each_k);
            #        count_tokens = 0;
            #        if each_k in token_relevance:
            #            print('Token relevance ', token_relevance[each_k]);
            #            sum += token_relevance[each_k];
            #            print("sum ", sum)
            #            count_tokens += 1;
            #    if count_tokens != 0:
            #        sum = sum/count_tokens;
            #    k.score += sum;
            #    print("word ", k.getword(), " ", k.getscore())
            print("INFO: Sorting all the words and phrases based on the ranking scores and getting Top 15 words.");
            #sort the final list of ranked words
            final_ranked_words.sort(key=operator.attrgetter('score'), reverse=True)
            count = 0;
            key_words = [];
            #Will show first 15 ranked keywords
            for rw in final_ranked_words:
                count += 1;
                print(rw.getword(), " ", rw.getscore());
                if len(key_words) == 15:
                    break;
                else:
                    if rw.isUpper:
                        key_words.append(rw.getword().upper());
                    else:
                        key_words.append(rw.getword().title());
            print("INFO: Success, check your words in the UI.");
            return {'words' : key_words};
        except Exception as e:
            print("ERROR: Some error occurred.");
            print(e);
            return {"error": "Sorry, something went wrong! Please verify the URL."};
        else:
            return {"words" : key_words};