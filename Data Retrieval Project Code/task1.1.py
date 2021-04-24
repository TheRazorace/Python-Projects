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
        sys.exit('Απέτυχε η σύνδεση με την ElasticSearch!')   
    
    return es

# Συνάρτηση αποθήκευσης ταινιών και δημιουργία βάσης δεδομένων στην Elasticsearch
def ReadMovies(es):
    
    #Διαγραφή προηγούμενης βάσης ταινιών
    es.indices.delete(index="movies", ignore=[404,400])     
    
    #Ανάγνωση csv αρχείου
    try:
        df = pd.read_csv('movies.csv')
    except IOError:
        #Έξοδος αν αποτύχει
        sys.exit('Δεν υπάρχει το αρχείο αυτό στον φάκελό σας!')
        
    #Για κάθε ταινία, προσθήκη στην βάση δεδομένων
    print("Αποθηκεύονται οι ταινίες στην Elasticsearch...")
    for index,row in df.iterrows():
        doc = {'title':row['title'], 'genres':row['genres']}
        es.index(index = "movies", id = int(row['movieId']), body = doc)
        
    print("Η αποθήκευση ολοκληρώθηκε!")

# Κύρια συνάρτηση
if __name__ == '__main__':                                  
    
    es = ConnectElastic()
    ReadMovies(es)