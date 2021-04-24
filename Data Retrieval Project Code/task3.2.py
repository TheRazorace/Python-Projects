# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
import sys
import pandas as pd


# Συνάρτηση σύνδεσης με την Elasticsearch
def ConnectElastic():
    #Σύνδεση με ElasticSearch
    print("Γίνεται σύνδεση με την Elasticsearch...")
    es = Elasticsearch(HOST="http://localhost", PORT=9200)  
    es = Elasticsearch()
    
    #Έξοδος αν αποτύχει
    if not es.ping():
        sys.exit('Απέτυχε η σύνδεση με την ElasticSearch')   
        
    
    return es

# Συνάρτηση αναζήτησης ταινιών
def FindMovies(es):
    
    #Είσοδος user Id
    user_in = input("Πληκτρολογήστε το αναγνωριστικό σας:")
    if not user_in.isdigit():
        sys.exit("Σφάλμα! Δεν πληκτρολογήσατε έγκυρο αναγνωριστικό.")
     
    # Είσοδος φράσης προς αναζήτηση
    movie_in = input("Επιλέξτε φράση προς αναζήτηση:")
    print("")
      
    
    #Σώμα αναζήτησης
    body = {
    "from":0,
    "size":8000,
    "query": {
        "match": {
            "title":movie_in
            }
        }
    }
    
    #Αναζήτηση φράσης στην elasticsearch
    res = es.search(index="movies", body=body)
    
    #Αριθμός αποτελεσμάτων
    total_results = res["hits"]["total"].get('value')
    
    #Αν υπάρχουν αποτελέσματα
    if(total_results>0):
        print("Εύρεση σκορ χρήστη, σκορ συστάδας και μέσου σκορ...")
        
        #Αποθήκευση score της elasticsearch και movieIds των ταινιών
        elastic_score, movie_ids = ElasticData(res, total_results)
          
        #Αποθήκευση ratings dataframe για τις ταινίες-αποτελέσματα
        ratings, new_ratings3 = CreateRatingsratings(movie_ids)
        
        #Εύρεση σκορ χρήστη (αν υπάρχει), σκορ συστάδας και μέσο σκορ
        user_score, avg_score, cluster_score = RatingBasedScores(total_results,
                                movie_ids, ratings, user_in, new_ratings3)
         
        #Υπολογισμός συνολικού σκορ
        total_score = TotalScore(total_results, elastic_score, user_score, avg_score, cluster_score) 
           
        #Εκτύπωση βάσει σκορ
        ShowMovies(es, total_score, movie_ids)
     
    #Αν δεν υπάρχουν αποτελέσματα
    else:
        print("Δεν βρέθηκαν ταινίες με αυτή την φράση")
        
    return


#Συνάρτηση αποθήκευσης score της elasticsearch και movieIds των ταινιών 
def ElasticData(res, total_results):
    
    elastic_score = [0]*total_results
    movie_ids = [0]*total_results
        
    #Για κάθε ταινία, αποθήκευση σκορ της elasticsearch και movieId             
    i = 0
    for movie in res["hits"]["hits"]:
        elastic_score[i] = movie["_score"]
        movie_ids[i] = movie["_id"]
        i = i + 1
        
    return elastic_score, movie_ids
    

#Συνάρτηση αποθήκευσης ratings dataframe για τις ταινίες-αποτελέσματα
def CreateRatingsratings(movie_ids):
    
    #Αποθήκευση αρχείου ratings σε pandas dataframe
    try:
        ratings = pd.read_csv('ratings.csv')
        new_ratings3 = pd.read_csv('new_ratings3.csv')
    except IOError:
        sys.exit('Δεν υπάρχει το αρχείο αυτό στον φάκελό σας!')
    
    #Αποκοπή των ταινιών που δεν έχουν επιστραφεί ως αποτέλεσμα της elasticsearch             
    ratings = ratings.loc[ratings['movieId'].isin(movie_ids)]
    ratings = ratings[['userId','movieId','rating']].reset_index()
    new_ratings3 = new_ratings3.loc[new_ratings3['movieId'].isin(movie_ids)]
    new_ratings3 = new_ratings3[['userId','movieId','rating']].reset_index()
    
    return ratings, new_ratings3
    

#Συνάρτηση εύρεσης σκορ χρήστη (αν υπάρχει) και μέσο σκορ
def RatingBasedScores(total_results, movie_ids, ratings, user_in, new_ratings3):
    
    #Πίνακες αποθήκευσης σκορ
    user_score = [0]*total_results
    avg_score = [0]*total_results
    cluster_score = [0]*total_results
    
    i = 0
    #Για κάθε ταινία
    for movie_id in movie_ids:
            
        #Διατήρηση βαθμολογιών ταινίας
        ratings_avg = ratings[ratings['movieId'] == int(movie_id)]
        #Εύρεση μέσου όρου
        avg_score[i] = ratings_avg['rating'].mean()
          
        #Διατήρηση βαθμολογίας χρήστη για την ταινία
        ratings_user = ratings_avg[ratings_avg['userId'] == int(user_in)]
        if(ratings_user.empty == False):
            user_score[i] = ratings_user.iloc[0,3]
        
        #Αποθήκευση βαθμολογίας συστάδα χρήστη για την ταινία
        cluster_score[i] = new_ratings3.loc[(new_ratings3["movieId"] == int(movie_id))
                            & (new_ratings3['userId'] == int(user_in))]["rating"].to_numpy()[0]
        
        i = i + 1
        
    return user_score, avg_score, cluster_score
    
#Συνάρτηση υπολογισμού συνολικού score
def TotalScore(total_results, elastic_score, user_score, avg_score, cluster_score):
    
    total_score = [0]*total_results
    #Βάρη score elasticsearch, χρήστη, μέσου score και score συστάδας αντίστοιχα
    w1 = 1
    w2 = 2
    w3 = 1
    w4 = 1.5
    
    #Για κάθε ταινία που επέστρεψε η elasticsearch
    for i in range (0,total_results):
        
        #Aν δεν έχει βαθμολογηθεί από κανέναν, μετράει μόνο το score της elasticsearch
        if(avg_score[i] == 0):
            score = w1*elastic_score[i]
            total_score[i] = score
         
        #Αν έχει βαθμολογηθεί από τον χρήστη, δεν λαμβάνεται υπόψη το score της συστάδας
        elif(user_score[i]>0):
            score = w1*elastic_score[i] + w2*user_score[i] + w3*avg_score[i]
            total_score[i] = score/3
          
        #Αν δεν έχει βαθμολογηθεί από τον χρήστη, λαμβάνεται υπόψη το score της συστάδας
        else:
            score = w1*elastic_score[i] + w3*avg_score[i] + w4*cluster_score[i]
            total_score[i] = score/3
            
            
    return total_score


#Συνάρτηση εκτύπωσης βάσει score
def ShowMovies(es, total_score, movie_ids):
    
    #Δημιουργία λίστας movieId βάσει των συνολικών σκορ, με φθίνουσα σειρά
    sorted_movie_ids = [x for _,x in sorted(zip(total_score,movie_ids))][::-1]
    
    #Εκτύπωση ταινιών με την συνάρτηση get της elasticsearch...
    #... χρησιμοποιώντας τα movieIds
    print("Οι ταινίες που βρέθηκαν:")
    for i in range(0,len(sorted_movie_ids)):
        movie = es.get(index="movies", id=int(sorted_movie_ids[i]))
        print(movie["_source"].get("title"))
        
    return
  

#Κύρια συνάρτηση 
if __name__ == '__main__':                                  
    
    es = ConnectElastic()
    FindMovies(es)


