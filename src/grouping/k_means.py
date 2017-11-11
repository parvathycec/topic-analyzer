#TODO: scatter plot
#TODO: How to find K
#TODO: Clean and rename some variables in this file
from math import sqrt
import os
import random
from gensim import models
from gensim.models.keyedvectors import KeyedVectors
from numpy import float32
import numpy as np
from grouping import model_path

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
        
        
def get_clusters(nouns):

    #need array of sentences (array of array of words)
    noun_arr = list(nouns);
    model = models.KeyedVectors.load_word2vec_format(os.path.join(os.path.dirname(__file__), model_path), binary=True, limit=50000)
    model.init_sims(replace=True)
    model.save('GoogleNews-vectors-gensim-normed.bin');
    word2vec_dict = {}
    #words = model.wv.index2word  # order from model.wv.syn0
    final_words = [];
    for i in noun_arr:
        if i in model.wv.vocab:
            word2vec_dict[i] = model.wv[i]
            #print('vector : ', word2vec_dict[i].T );
        #print("word2vec_dict[i] is ", word2vec_dict[i])
    #list of vectors
    X = [];
    words = [];
    for i in noun_arr:
        if i in word2vec_dict:
            X.append(word2vec_dict[i].T);
            words.append(i);
        else:
            final_words.append(i);#Can use numpy array
    
    #step 1: pick K random points as cluster
    #print(X);
    k=round(sqrt(len(X)/2));#randomly choose k elements
    print("*******************", k)
    centroid_list = random.sample(X, k);
    final_centroid_map = get_centroid(centroid_list, X);
    dt=np.dtype('float32')
    model = KeyedVectors.load('GoogleNews-vectors-gensim-normed.bin', mmap='r')
    model.syn0norm = model.syn0  # prevent recalc of normed vectors
    centroid_words = [];
    centroid_data_list = [];
    counter = 0;
    for word_vec in final_centroid_map.keys():
        counter += 1;
        centroid_word, centroid_vector = model.most_similar(positive=[np.array(tuple(word_vec),dtype=dt)], topn=1)[0];
        print("Centroid : ", centroid_word);
        centroid_data_list.append(np.column_stack(([np.array(tuple(word_vec),dtype=dt)])))
        centroid_words.append(centroid_word);
        for val_vec in final_centroid_map[word_vec]:
            data_word, data_vector = model.most_similar(positive=[np.array(tuple(val_vec),dtype=dt)], topn=1)[0];
    centroids = np.array(centroid_data_list);
    final_words.extend(centroid_words);
    return final_words;