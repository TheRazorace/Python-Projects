# -*- coding: utf-8 -*-

import sys
import pandas as pd
import numpy as np
import keras
from keras import layers
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

#Συνάρτηση υπολογισμού προβλέψεων για ταινίες που δεν έχουν βαθμολογηθεί
def FindRestOfRatings(movies, ratings, user_id, vector_size):
    
    #Εύρεση βαθμολογιών χρήστη
    user_ratings = ratings.loc[ratings.userId == user_id]
    
    #Δημιουργία one-hot encoding διανύσματος για κάθε ταινία που έχει βαθμολογηθεί
    user_ratings = AddRatingLabels(user_ratings, user_id)
    user_rated_movies = user_ratings['movieId'].to_numpy()
    
    #Δημιουργία δεδομένων εκπαίδευσης και αξιολόγησης
    x_train, y_train = GetTrainData(user_ratings, user_rated_movies, movies)
    x_test = GetTestData(user_rated_movies, movies)
    
    #Πρόβλεψη υπόλοιπων βαθμολογιών
    new_user_ratings = NeuralNet(x_train, y_train, x_test, vector_size, genres_list, user_id)
    
    return new_user_ratings


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


#Συνάρτηση ένωσης των word embeddings διανυσμάτων με τα διανύσματα που αφορούν...
#... τις κατηγορίες ταινιών (σε μορφή one-hot encoding) και αποθήκευση στο movies dataframe
def AddEmbeddings(movies, genres_list, titles_vector):
    
    embeddings_and_encodings = [] 
    ohe_genre = [0]*len(genres_list)
    
    #Για κάθε ταινία
    for index, row in movies.iterrows():
        #Εύρεση διανύσματος word embedding
        title2vec = titles_vector[index].tolist()
        #Εύρεση κατηγορίας ταινίας και δημιουργία one-hot encoding διανύσματος
        for i in row["genres"].split("|"):
            for j,k in enumerate(genres_list):
                if(i==k):
                    ohe_genre[j] = 1
        
        #Ένωση των 2 διανυσμάτων
        combination = title2vec + ohe_genre
        #Προσθήκη σε λίστα
        embeddings_and_encodings.append(combination)
        ohe_genre = [0]*len(genres_list)
    
    #Προσθήκη των ενωμένων διανυσμάτων στο movies dataframe
    movies.insert(3, "Embeddings + Encodings", embeddings_and_encodings, True)
    
    return movies

#Συνάρτηση δημιουργίας one-hot encoding διανύσματος για τις βαθμολογίες
def AddRatingLabels(user_ratings, user_id):
    
    ohe_ratings = []
    #Διάνυσμα 10 θέσεων
    #Κάθε θέση συμβολίζει μία βαθμολογία από το 0.5 έως το 5.0 με βήμα 0.5
    ohe_rating = [0]*10
    
    #Για κάθε βαθμολογία συμπλήρωση άσου στο αντίστοιχο πεδίο
    for index, row in user_ratings.iterrows():
        ohe_rating[int(2*float(row["rating"]) - 1)] = 1
        ohe_ratings.append(ohe_rating)
        ohe_rating = [0]*10
     
    #Προσθήκη των διανυσμάτων στο ratings dataframe
    user_ratings.insert(3, "One-Hot Encoding Ratings", ohe_ratings, True)
    
    return user_ratings
 
#Συνάρτηση υπολογισμού των δεδομένων εκπαίδευσης για κάθε χρήστη
def GetTrainData(user_ratings, user_rated_movies, movies):
    
    #Αποθήκευση ταινιών που έχουν βαθμολογηθεί από τον χρήστη
    train_df = movies.loc[movies.movieId.isin(user_rated_movies)]
    x_train = []
    y_train = []
    #Είσοδοι εκπαίδευσης νευρωνικού δικτύου τα διανύσματα των ταινιών (embedding vector + genres vector)
    for index, row in train_df.iterrows():
        array = row["Embeddings + Encodings"]
        x_train.append(array)
    #Επιθυμητές έξοδοι του δικτύου τα διανύσματα των βαθμολογιών
    for index, row in user_ratings.iterrows():   
        array = row["One-Hot Encoding Ratings"]
        y_train.append(array)
        
    return x_train, y_train

#Συνάρτηση υπολογισμού των δεδομένων αξιολόγησης για κάθε χρήστη
def GetTestData(user_rated_movies, movies):
    
    #Αποθήκευση ταινιών που δεν έχουν βαθμολογηθεί από τον χρήστη
    test_df = movies.loc[~movies.movieId.isin(user_rated_movies)]
    x_test = []
    #Είσοδοι αξιολόγησης νευρωνικού δικτύου τα διανύσματα των ταινιών (embedding vector + genres vector)
    for index, row in test_df.iterrows():
        array = row["Embeddings + Encodings"]
        x_test.append(array)
    
    return x_test

#Συνάρτηση δημιουργίας νευρωνικού δικτύου για κάθε χρήστη
def NeuralNet(x_train, y_train, x_test, vector_size, genres_list, user_id):
    
    #Νευρωνικό δίκτυο από ένα επίπεδο εισόδου με αριθμό νευρώνων εισόδου...
    #... ίσο με το μέγεθος του ενωμένου διανύσματος, 2 κρυφά επίπεδα...
    #... κι ένα επίπεδο εξόδου με 10 νευρώνες, όσες και οι πιθανές βαθμολογίες...
    #... χρησιμοποιώντας τη συνάρτηση ενεργοποίησης softmax για την...
    #... κατηγοριοποίηση πολλών labels
    model = keras.Sequential()
    model.add(layers.Dense(64, input_shape=(vector_size+len(genres_list),), activation='relu'))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(10, activation='softmax'))
    
    #Χρήση adam optimizer και συνάρτηση κόστους categorical crossentropy γιατί...
    #... γίνεται κατηγοριοποίηση μεταξύ πολλών κατηγοριών
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy', metrics=['accuracy'])
    
    #Εκπαίδευση δικτύου με τα δεδομένα εκπαίδευσης που υπολογίστηκαν για 100 εποχές
    model.fit(np.array(x_train), np.array(y_train),
          batch_size=40, epochs=100, verbose=0)
    
    #Υπολογισμός ακρίβειας εκπαίδευσης 
    loss, accuracy = model.evaluate(np.array(x_train), np.array(y_train), verbose=0)
    print('Ακρίβεια εκπαίδευσης για βαθμολογίες του χρήστη ' +str(user_id)+
          ': %f' % (accuracy*100) + '% (Εποχές: 100)')
    
    #Υπολογισμός προβλέψεων βαθμολογιών για τα δεδομένα αξιολόγησης που υπολογίστηκαν
    predictions = model.predict(np.array(x_test))
    
    #Μετατροπή των διανυσμάτων πρόβλεψης στις βαθμολογίες που τους αντιστοιχούν
    new_user_ratings = [0]*len(predictions)
    for i in range(len(predictions)):
        index = list(predictions[i]).index(max(list(predictions[i])))
        new_user_ratings[i] = (index/2) + 0.5        
        
    
    return new_user_ratings


#Συνάρτηση δημιουργίας νέου συνόλου δεδομένου, με βαθμολογία σε κάθε ταινία για κάθε χρήστη
def CreateNewRatingsDf(movies, ratings, vector_size):
    
    #Εύρεση όλων των χρηστών και όλων των ταινιών
    user_ids = ratings['userId'].unique()
    movie_ids = ratings['movieId'].unique()
    
    #Λεξικό αποθήκευσης
    ratings_dict = {}
    
    i = 0
    #Για κάθε χρήστη
    for uid in user_ids:
        print("Υπολογισμός υπόλοιπων βαθμολογιών για τον χρήστη: " +str(uid)+ " ...")
        #Πρόβλεψη των βαθμολογιών που λείπουν
        new_user_ratings = FindRestOfRatings(movies, ratings, uid, vector_size)
        print("Οι υπόλοιπες βαθμολογίες υπολογίστηκαν για τον χρήστη " +str(uid)+ ".")
        print(" ")
        
        #Εύρεση των ταινιών που έχει βαθμολογήσει
        user_rated = ratings.loc[ratings['userId']==uid]['movieId'].to_numpy()
    
        j = 0
        #Για κάθε ταινία
        for mid in movie_ids:
            
            #Αν η ταινία έχει βαθμολογηθεί, αποθήκευση της βαθμολογίας χρήστη
            if mid in user_rated:
                
                score = float(ratings.loc[(ratings["userId"] == uid)
                                 & (ratings["movieId"] == mid), "rating"])
             
            #Αν η ταινία δεν έχει βαθμολογηθεί, αποθήκευση της πρόβλεψης βαθμολογίας 
            else:
                
                score = float(new_user_ratings[j])
                j = j + 1
            
            #Προσθήκη στο λεξικό
            ratings_dict[i] = {"userId":uid, "movieId":mid, "rating":score} 
            i = i + 1
    
    #Δημιουργία νέου dataframe 
    new_ratings = pd.DataFrame.from_dict(ratings_dict, "index")
    new_ratings = new_ratings.sort_values(["userId", "movieId"])
    
    print("Ο υπολογισμός ολοκληρώθηκε!")
    
    #Αποθήκευση σε csv αρχείο για χρήση χωρίς ανάγκη υπολογισμού κάθε φορά
    compression_opts = dict(method='zip', archive_name='new_ratings4.csv')
    new_ratings.to_csv('new_ratings4.zip', index=False, compression=compression_opts)
    
    print("Όλες οι βαθμολογίες αποθηκεύτηκαν στον φάκελο: new_ratings4")
    
    return new_ratings
                
    
#Συνάρτηση φιλτραρίσματος τίτλων
def FilterText(string):
    
    #Αποκοπή ημερομηνίας από τον τίτλο
    string = string.split('(', 1)[0].lower()
    
    #Αποκοπή συμβόλων από τίτλους
    punctuations = r'''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for x in string.lower(): 
        if x in punctuations: 
            string = string.replace(x, "") 
            
    #Αφαίρεση stop words από τον τίτλο
    stop_words = (['the', 'a', 'and', 'is', 'be', 'will',
                  'can', 'could', 'would', 'was', 'to', 'of'])
    string = ' '.join([word for word in string.split() if word not in stop_words])
    
    #Tokenization του τίτλου που απέμεινε
    array_str = string.split(" ")
    
    return array_str

#Συνάρτηση δημιουργίας word embeddings 
def TitleEmbeddings(movies, vector_size):
    
    #Αποθήκευση όλων τίτλων αφού πρώτα φιλτραριστούν και υποστούν tokenization
    titles = []
    for i in movies['title']:
        titles.append(FilterText(i))
    
    #Δημιουργία μοντέλου Word Embeddings με την τεχνική Doc2Vec   
    tagged_data = [TaggedDocument(d, [i]) for i, d in enumerate(titles)]   
    d2v_model = Doc2Vec(tagged_data, vector_size = vector_size)
    
    #Αποθήκευση των διανυσμάτων για κάθε ταινία
    vectors = []
    for vector in d2v_model.docvecs.vectors_docs:
        vectors.append(vector)
        
    return vectors
    
#Κύρια συνάρτηση
if __name__ == '__main__': 
    
    print("Πρόγραμμα πρόβλεψης βαθμολογιών με την χρήση των Word Embedings.")
    print("Φόρτωση απαραίτητων αρχείων...")
    #Φόρτωση απαραίτητων αρχείων
    try:
        ratings = pd.read_csv('ratings.csv')
        movies = pd.read_csv('movies.csv') 
    except IOError:
        sys.exit('Δεν υπάρχει το αρχείο αυτό στον φάκελό σας!')
        
    ratings = ratings[["userId", "movieId", "rating"]]
    
    print("Υπολογισμός Word Embeddings ταινιών...")
    print(" ")
    
    #Υπολογισμός Word Embeddings για τις ταινίες
    vector_size = 100
    titles_vector = TitleEmbeddings(movies, vector_size)
    
    #Εύρεση όλων των κατηγοριών ταινίας που υπάρχουν 
    genres_list = FindGenresList(movies)
    
    #Πρόσθεση των διανυσμάτων των ταινιών στο dataframe ταινιών
    movies = AddEmbeddings(movies, genres_list, titles_vector)   
    
    #Υπολογισμός βαθμολογιών που λείπουν
    new_ratings = CreateNewRatingsDf(movies, ratings, vector_size)                          
    


