'''
@summary: Step 4: To remove keywords that are similar
This is to bring more diversity to the top ranked keywords
We use an algorithm called k-means for this.
The K-means algorithm is implemented using numpy arrays for computation
We use GoogleNews pre-trained dataset to compute word2vec.
MODEL_PATH should point to the dataset location. Tested only in Windows.
@author: Parvathy
'''

from math import sqrt
import os
import random
from gensim import corpora, models, similarities
from gensim.corpora import TextCorpus, MmCorpus, Dictionary
from gensim.models.keyedvectors import KeyedVectors
from numpy import float32
import numpy as np

MODEL_PATH = 'C:/Users/parvathy/Documents/UNH/Fall 2017/Python/Project/data.model/GoogleNews-vectors-negative300.bin'

def euclidian_distance(vector1, vector2):
    """Find euclidian distance between two vectors"""
    #Reference: http://www.codehamster.com/2015/03/09/different-ways-to-calculate-the-euclidean-distance-in-python/
    distance_square = 0;
    if len(vector1) == len(vector2):
        zip_vector = zip(vector1, vector2);
        for member in zip_vector:
            distance_square += (member[1] - member[0]) ** 2;
    euclidean_distance = sqrt(distance_square);    
    return euclidean_distance;
   
def find_closest_centroid(centroid_vector_distance_map):
    """Find the shortest euclidian distance 
    input: {centroid:euclidian distance of the vector to this centroid
    output: centroid with the shortest distance"""
    shortest_dist = 0;
    closest_centroid = 0;
    count = 0;
    #For all centroids
    for centroid_key in centroid_vector_distance_map.keys():
        #if first time or if current shortest distance greater than current distance from the map 
        if (count == 0) or (shortest_dist > centroid_vector_distance_map[centroid_key]):
            shortest_dist = centroid_vector_distance_map[centroid_key];
            closest_centroid = centroid_key;
        count += 1;
    return closest_centroid;


def find_distance(centroid_map, word_vectors):
    """Find the closest centroid for each word_vector"""
    #TODO: 0
    centroid_vector_distance_map = {k:0 for k in centroid_map.keys()};
    for word_vector in word_vectors:
        for centroid in centroid_map.keys():
            #calculate distance of current vec from each centroid
            distance = euclidian_distance(centroid, word_vector);
            centroid_vector_distance_map[centroid] = distance;
            #shorted distance
        closest_centroid = find_closest_centroid(centroid_vector_distance_map);
        centroid_map[closest_centroid].append(word_vector);
    return centroid_map;


def get_centroid(centroid_list, X): 
    """Get centroids recursively until no more changes are needed"""
    #We use Euclidean distance here
    #This is a map of centroid and list of vectors
    #key is current centroid and list of vectors is the value
    centroid_map = {tuple(k):[] for k in centroid_list};#converting to tuple because key cannot be an array
    centroid_map = find_distance(centroid_map, X);
    #print("After clustering : ", centroid_map);
    #step 3: find average of each cluster and assign it as new centroid
    old_centroid_list = centroid_list;
    #print("old_centroid_list : ", old_centroid_list);
    centroid_list = [np.mean(arr, axis=0, dtype=float32) for arr in centroid_map.values()]
    #print("centroid_list : ", centroid_list)
    if (np.array_equal(old_centroid_list, centroid_list)): 
        print("Finally no more change");
        return centroid_map;
    return get_centroid(centroid_list, X);
        
        
def get_clusters(ranked_words):

    model = models.KeyedVectors.load_word2vec_format(os.path.join(os.path.dirname(__file__), MODEL_PATH), binary=True, limit=50000)
    model.init_sims(replace=True)
    model.save('GoogleNews-vectors-gensim-normed.bin');
    word2vec_dict = {}
    #words = model.wv.index2word  # order from model.wv.syn0
    final_words = [];
    words = [];
    
    for i in ranked_words:
        if i.getword() in model.wv.vocab:
            word2vec_dict[i.getword()] = model.wv[i.getword()]
            #print('vector : ', word2vec_dict[i].T );
        #print("word2vec_dict[i] is ", word2vec_dict[i])
    #list of vectors
    X = [];
    words = [];
    for i in ranked_words:
        if i.getword() in word2vec_dict:
            X.append(word2vec_dict[i.getword()].T);
            words.append(i.getword());
        else:
            final_words.append(i);#Can use numpy array
    
    #step 1: pick K random points as cluster
    #print(X);
   # K=range(10);#round(sqrt(len(X)/2));#randomly choose k elements
    sum_distance_arr = [];
    for k in range(1, 10):
        print("*******************", k)
        centroid_list = random.sample(X, k);
        final_centroid_map = get_centroid(centroid_list, X);
        sum_distance = 0;
        for centroid_key in final_centroid_map.keys():
            for data_value in final_centroid_map[centroid_key]:
               sum_distance += euclidian_distance(centroid_key, data_value)
        print(sum_distance);
        sum_distance_arr.append(sum_distance);
        if(sum_distance == 0):
            break;
    k = 1;
    if len(sum_distance_arr) > 1:
        list_val = [abs(t - s) for s, t in zip(sum_distance_arr, sum_distance_arr[1:])];
        print(list_val);
        k = list_val.index(min(list_val))+1;
    print("Final *******************", k)
    centroid_list = random.sample(X, k);
    final_centroid_map = get_centroid(centroid_list, X);
    sum_distance = 0;
    for centroid_key in final_centroid_map.keys():
        for data_value in final_centroid_map[centroid_key]:
           sum_distance += euclidian_distance(centroid_key, data_value)
    print(sum_distance);
    sum_distance_arr.append(sum_distance);
    dt=np.dtype('float32')
    model = KeyedVectors.load('GoogleNews-vectors-gensim-normed.bin', mmap='r')
    model.syn0norm = model.syn0  # prevent recalc of normed vectors
    centroid_words = [];
    centroid_data_list = [];
    counter = 0;
    data_cluster_list = [];
    for word_vec in final_centroid_map.keys():
        counter += 1;
        centroid_word, centroid_vector = model.most_similar(positive=[np.array(tuple(word_vec),dtype=dt)], topn=1)[0];
        print("Centroid : ", centroid_word);
        centroid_data_list.append(np.column_stack(([np.array(tuple(word_vec),dtype=dt)])))
        centroid_words.append(centroid_word);
        data_clusters = [];
        for val_vec in final_centroid_map[word_vec]:
            data_word, data_vector = model.most_similar(positive=[np.array(tuple(val_vec),dtype=dt)], topn=1)[0];
            data_clusters.append(get_ranked_word(ranked_words, data_word));
        data_cluster_list.append(data_clusters);
    return final_words, data_cluster_list;


def get_ranked_word(ranked_word_list, word):
    """Get RankedWord object containing the given word"""
    for rw in ranked_word_list:
        if word == rw.getword():
            return rw;
        
def get_relevance(words):
    texts = [[word for word in rw.lower().split()] for rw in words]
    print(texts)
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    d = {}
    for doc in corpus_tfidf:
        for id, value in doc:
            word = dictionary.get(id)
            print('Word : ', word)
            print('Value : ',value)
            d[word] = value;
    #sorted(d, key=lambda k: d[k][1])
    return d;
                