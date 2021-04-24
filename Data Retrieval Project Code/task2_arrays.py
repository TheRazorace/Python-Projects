# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
import sys
from csv import DictReader


def ConnectElastic():
    es = Elasticsearch(HOST="http://localhost", PORT=9200)   ##Σύνδεση με ElasticSearch
    es = Elasticsearch()

    if not es.ping():
        sys.exit('Απέτυχε η σύνδεση με την ElasticSearch')   ##Έξοδος αν αποτύχει
    
    return es


def FindMovies(es):
    
    user_in = input("Πληκτρολογήστε το αναγνωριστικό σας:")
    if not user_in.isdigit():
        sys.exit("Σφάλμα! Δεν πληκτρολογήσατε έγκυρο αναγνωριστικό.")
    
    movie_in = input("Επιλέξτε φράση προς αναζήτηση:")
    
    body = {
    "from":0,
    "size":8000,
    "query": {
        "match": {
            "title":movie_in
            }
        }
    }

    res = es.search(index="movies", body=body)
    total_results = res["hits"]["total"].get('value')
    
    if(total_results>0):
        
        elastic_score = [0]*total_results
        user_score = [0]*total_results
        avg_score = [0]*total_results
        number_of_ratings = [0]*total_results
        movie_ids = [0]*total_results
        
        total_score = [0]*total_results
        w1 = 1
        w2 = 2
        w3 = 1 
    
        i = 0
        for movie in res["hits"]["hits"]:
            elastic_score[i] = movie["_score"]
            movie_ids[i] = movie["_id"]
            i = i + 1
            
        with open('ratings.csv', 'r') as read_obj:
            ratings_dict_reader = DictReader(read_obj)
            for row in ratings_dict_reader:
                if row["movieId"] in movie_ids:
                    Id = row["movieId"]
                    Index = movie_ids.index(Id)
                    
                    number_of_ratings[Index] += 1 
                    avg_score[Index] += float(row["rating"])
                    
                    if user_in == row["userId"]:
                        user_score[Index] = float(row["rating"])
                    
        for i in range (0,total_results):
            if avg_score[i]>0:
                avg_score[i] = float(avg_score[i]/number_of_ratings[i])
                    
    
        for i in range (0,total_results):
            
            score = w1*elastic_score[i] + w2*user_score[i] + w3*avg_score[i]
            
            if(user_score[i]>0 and w3*avg_score[i]<0) or (user_score[i]<0 and w3*avg_score[i]>0):
                total_score[i] = score/2
            elif(user_score[i]>0 and w3*avg_score[i]>0):
                total_score[i] = score/3 
            else:
                total_score[i] = score
            
        
        sorted_movie_ids = [x for _,x in sorted(zip(total_score,movie_ids))][::-1]
        
        for i in range(0,len(sorted_movie_ids)):
            movie = es.get(index="movies", id=int(sorted_movie_ids[i]))
            print(movie["_source"].get("title"))
        
        
    else:
        print("Δεν βρέθηκαν ταινίες με αυτή την φράση")
        
    return



if __name__ == '__main__':                                  
    
    es = ConnectElastic()
    FindMovies(es)
    
    
    
    