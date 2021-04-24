# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
import sys
from csv import reader

def ConnectElastic():
    es = Elasticsearch(HOST="http://localhost", PORT=9200)   ##Σύνδεση με ElasticSearch
    es = Elasticsearch()

    if not es.ping():
        sys.exit('Απέτυχε η σύνδεση με την ElasticSearch')   ##Έξοδος αν αποτύχει
    
    return es
        

def ReadMovies(es):
    
    es.indices.delete(index="movies", ignore=[404,400])     ##Διαγραφή προηγούμενης βάσης ταινιών
    
    with open('movies.csv', encoding="utf8") as movies:     ##Άνοιγμα αρχείου
        csv_reader = reader(movies)                         ##Ανάγνωση ανά σειρά με reader
        categories = next(csv_reader)                       ##Ανάγνωση πρώτης σειράς
        
        for movie in csv_reader:                            ##Ανάγνωση υπόλοιπων σειρών
            full_title = ', '.join(movie[1:-1])
            doc = {categories[1]:full_title, categories[2]:movie[-1]}  ##Document που εισάγεται
            es.index(index="movies",id=int(movie[0]) ,body=doc)         ##Εισαγωγή στην βάση movies
            
    return
    
if __name__ == '__main__':                                  
    
    es = ConnectElastic()
    ReadMovies(es)
    
    

