# -*- coding: utf-8 -*-

import sys
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer

# Συνάρτηση υπολογισμού νέων βαθμολογιών βάσει συσταδοποίησης
def CreateNewRatings():
    
    print("Υπολογισμός υπόλοιπων βαθμολογιών για κάθε χρήστη βάσει συσταδοποίησης...")
    print("Φόρτωση ταινιών και βαθμολογιών...")
    # Φόρτωση ταινιών και βαθμολογιών
    try:
        ratings = pd.read_csv('ratings.csv')
        movies = pd.read_csv('movies.csv')                                
    except IOError:
        sys.exit('Δεν υπάρχει το αρχείο αυτό στον φάκελό σας!')
        
    
    ratings = ratings[["userId", "movieId", "rating"]]
    
    print("Εύρεση όλων των κατηγοριών ταινίας που υπάρχουν...")
    #Εύρεση όλων των κατηγοριών ταινίας που υπάρχουν
    genres_list = FindGenresList(movies)
     
    print("Εύρεση μέσης βαθμολογίας κάθε κατηγορίας για κάθε χρήστη ...")
    #Εύρεση μέσης βαθμολογίας κάθε κατηγορίας για κάθε χρήστη     
    avg_df = FindCatecoriesAvg(genres_list, ratings, movies)
    
    print("Συσταδοποίηση χρηστών βάσει μέσης βαθμολογίας σε κάθε κατηγορία ...")
    #Συσταδοποίηση χρηστών βάσει μέσης βαθμολογίας σε κάθε κατηγορία
    #Επιλογή συσταδοποίησης σε 8 συστάδες
    labels = KmeansClustering(8, avg_df)
    
    print("Eύρεση μέσης βαθμολογίας κάθε συστάδας για κάθε ταινία ...")
    #Eύρεση μέσης βαθμολογίας κάθε συστάδας για κάθε ταινία
    clustered_avg_df = ClusteredAvgDf(ratings,labels)
    
    print("Δημιουργία νέου συνόλου δεδομένου, με βαθμολογία σε κάθε ταινία για κάθε χρήστη ...")
    #Δημιουργία νέου συνόλου δεδομένου, με βαθμολογία σε κάθε ταινία για κάθε χρήστη
    new_ratings = CreateNewRatingsDf(movies, ratings, clustered_avg_df, labels)
    
    print("Ο υπολογισμός των νέων δεδομένων αξιολόγησης ολοκληρώθηκε!")
    print(new_ratings)
    
    return

#Συνάρτηση εύρεσης όλων των κατηγοριών που υπάρχουν
def FindGenresList(movies):
    
    #Αριθμός ταινιών
    num_of_movies = movies['genres'].count()
    
    #Λίστα αποθήκευσης κατηγοριών
    genres_list = []
    
    #Για κάθε ταινία, ευρεση των κατηγοριών της
    for i in range(0,num_of_movies):
        genres = movies['genres'].values[i].split('|')
        #Για κάθε κατηγορία της ταινίας, προσθήκη στην λίστα, αν δεν υπάρχει ήδη
        for genre in genres:
            if genre not in genres_list:
                genres_list.append(genre)
    
    genres_list.sort()
    
    return genres_list


#Συνάρτηση εύρεσης μέσης βαθμολογίας κάθε κατηγορίας για κάθε χρήστη
def FindCatecoriesAvg(genres_list, ratings, movies):
    
    df = ratings
    
    #Προσθήκη μιας στήλης για κάθε κατηγορία, στο dataframe των ratings
    for genre in genres_list:
        #Αρχικοποίηση με NaN
        df[genre] = np.NaN
    
    #Για κάθε ταινία, εύρεση των κατηγοριών της   
    for index, row in df.iterrows():
        movie_id = row['movieId']
        categories = movies[movies['movieId'] == movie_id].iloc[0,2]
        categories = categories.split('|')
        
        #Αντιγραφή της βαθμολογίας στο πεδίο της κατηγορίας
        for genre in genres_list:
            if genre in categories:
                df.at[index, genre] = row['rating']
        
            
                
    columns = list(df.columns.values)
    #Διατήρηση μόνο user id και των βαθμολογιών κάθε κατηγορίας 
    df = df[[columns[0]] + columns[3:]]  
    
    #compression_opts = dict(method='zip', archive_name='df.csv') 
    #df.to_csv('df.zip', index=False, compression=compression_opts)    
    
    #Για κάθε user εύρεση μέσης βαθμολογίας κάθε κατηγορίας
    avg_df = df.groupby('userId').mean()
    
    #compression_opts = dict(method='zip', archive_name='avg_df.csv')
    #avg_df.to_csv('avg_df.zip', index=False, compression=compression_opts)   
    
    return avg_df    
    

#Συνάρτηση συσταδοποίησης χρηστών βάσει μέσης βαθμολογίας σε κάθε κατηγορία
def KmeansClustering(clusters, avg_df):
    
    #Χρήση Simple Imputer για την συμπλήρωση των κατηγοριών που δεν έχουν βαθμολογηθεί...
    #... με τη μέση βαθμολογία της κατηγορίας
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    imp.fit(avg_df)
    avg_ratings = imp.transform(avg_df)
    
    #Συσταδοποίηση με Kmeans
    kmeans = KMeans(n_clusters=clusters, random_state=0).fit(avg_ratings)   
    
    #Επιστροφή των labels για κάθε χρήστη
    return kmeans.labels_


#Συνάρτηση εύρεσης μέσης βαθμολογίας κάθε συστάδας για κάθε ταινία
def ClusteredAvgDf(ratings, labels):
    
    clustered_avg_df = ratings 
     
    #Συμπλήρωση στο dataframe των ratings το label κάθε χρήστη
    for index, row in clustered_avg_df.iterrows():
        clustered_avg_df.at[index, 'cluster'] = labels[int(row['userId']) - 1]
    
    #Εύρεση μέσου βαθμού κάθε ταινίας για κάθε συστάδα
    clustered_avg_df = clustered_avg_df[['movieId','rating','cluster']]
    clustered_avg_df = (clustered_avg_df.pivot_table('rating', ['movieId', 'cluster'],
                        aggfunc='mean', dropna = False).reset_index().round(5))
    
    avg_ratings = ratings.groupby('movieId').mean().round(5)['rating']
    
    #Για τις ταινίες που δεν έχουν βαθμολογηθεί από κανέναν user μιας συστάδας
    for index, row in clustered_avg_df.iterrows():
        #Συμπλήρωση με τον μέσο όρο όλων των χρηστών
        if np.isnan(row['rating']):
            clustered_avg_df.at[index, 'rating'] = avg_ratings[row['movieId']]
    
    #compression_opts = dict(method='zip', archive_name='clustered_avg_df.csv')
    #clustered_avg_df.to_csv('clustered_avg_df.zip', index=False, compression=compression_opts) 
    
    return clustered_avg_df


#Συνάρτηση δημιουργίας νέου συνόλου δεδομένου, με βαθμολογία σε κάθε ταινία για κάθε χρήστη
def CreateNewRatingsDf(movies, ratings, clustered_avg_df, labels):
    
    #Εύρεση όλων των χρηστών και όλων των ταινιών
    user_ids = ratings['userId'].unique()
    movie_ids = ratings['movieId'].unique()
    
    #Λεξικό αποθήκευσης
    ratings_dict = {}  

    i = 0
    #Για κάθε χρήστη
    for uid in user_ids:
        
        print("Υπολογισμός νέων βαθμολογιών για τον χρήστη " + str(uid)+" ...")
        
        #Εύρεση των ταινιών που έχει βαθμολογήσει και της συστάδας του
        user_rated = ratings.loc[ratings['userId']==uid]['movieId'].to_numpy()
        cluster = labels[uid - 1]
         
        #Για κάθε ταινία
        for mid in movie_ids:
             
            #Αν η ταινία έχει βαθμολογηθεί, αποθήκευση της βαθμολογίας χρήστη
            if mid in user_rated:
                 
                score = float(ratings.loc[(ratings["userId"] == uid)
                             & (ratings["movieId"] == mid), "rating"])
             
            #Αν η ταινία δεν έχει βαθμολογηθεί, αποθήκευση της βαθμολογίας συστάδας
            else:
                 
                score = float(clustered_avg_df.loc[(clustered_avg_df["movieId"] == mid)
                             & (clustered_avg_df["cluster"] == cluster), "rating"])
            
            #Προσθήκη στο λεξικό
            ratings_dict[i] = {"userId":uid, "movieId":mid, "rating":score} 
            i = i + 1
            
        print("Ο υπολογισμός για τον χρήστη " + str(uid)+" ολοκληρώθηκε!")
        print(" ")
    
    #Δημιουργία νέου dataframe         
    new_ratings = pd.DataFrame.from_dict(ratings_dict, "index")
    new_ratings = new_ratings.sort_values(["userId", "movieId"])

    #Αποθήκευση σε csv αρχείο για χρήση χωρίς ανάγκη υπολογισμού κάθε φορά
    compression_opts = dict(method='zip', archive_name='new_ratings3.csv')
    new_ratings.to_csv('new_ratings3.zip', index=False, compression=compression_opts)
    
    return new_ratings


if __name__ == '__main__':                              
    
    CreateNewRatings()
    