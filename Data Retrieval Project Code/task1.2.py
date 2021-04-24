# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
import sys

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

# Συνάρτηση εύρεσης ταινιών δοσμένης φράσης από τον χρήστη
def FindString(es):
    
    #Φράση αναζήτητησης
    string = input("Επιλέξτε φράση προς αναζήτηση:")
    
    #Σώμα αναζήτησης 
    body = {
    "from":0,
    "size":8000,
    "query": {
        "match": {
            "title":string
            }
        }
    }
    
    #Αποθήκευση και φιλτράρισμα αποτελεσμάτων για να κρατηθούν οι τίτλοι
    res = es.search(index="movies", filter_path='hits.hits._source.title', body=body)
    
    #Αν υπάρχουν αποτελέσματα
    if(res):
        #Εκτύπωση αποτελεσμάτων
        print("Ταινίες που βρέθηκαν:")
        for movie in res["hits"]["hits"]:
            print(movie["_source"]["title"])
    
    #Αν δεν υπάρχουν αποτελέσματα
    else:
        print("Δεν βρέθηκαν ταινίες με αυτή την φράση!")
    return
    
#Κύρια συνάρτηση
if __name__ == '__main__':                                  
    
    es = ConnectElastic()
    FindString(es)
    
    
    
    