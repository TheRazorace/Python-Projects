import pandas as pd
import sys
from sklearn.model_selection import train_test_split
#pip install gensim==3.8.3
#pip install smart_open==2.0.0
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import sklearn.metrics as skmetrics
from sklearn.preprocessing import StandardScaler
from nltk.tokenize import word_tokenize

#Διαχωρισμός παραδδειγμάτων
def GetTrainTestData(df):
    X = df.drop(['label', 'email'],axis='columns')
    y = df.label
    
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25)
    
    return X_train, X_test, y_train, y_test

#Πρόσθεση των Doc2Vec διανυσμάτων στο dataframe
def AddEmbeddings(df, vector):
    
    embeddings = [] 
    
    for index, row in df.iterrows():
        mail2vec = vector[index]
        embeddings.append(mail2vec)
        
    df.insert(1, "vector", embeddings, True)
    
    return df
    
#Συνάρτηση δημιουργίας word embeddings 
def MailEmbeddings(df, vector_size):
    
    #Αποθήκευση όλων τίτλων 
    mails = []
    for mail in df['email']:
        mails.append([mail])
    
    #Δημιουργία μοντέλου Word Embeddings με την τεχνική Doc2Vec   
    tagged_data = [TaggedDocument(words=word_tokenize(str(d).lower()), tags=[str(i)]) for i, d in enumerate(mails)]  
    d2v_model = Doc2Vec(vector_size = vector_size)
    d2v_model.build_vocab(tagged_data)
    
    #Εκπαίδευση μοντέλου
    print("Doc2Vec model training initiated...")
    for epoch in range(10):
        print("Iteration: ", epoch+1)
        d2v_model.train(tagged_data,
                    total_examples=d2v_model.corpus_count,
                    epochs=d2v_model.iter)
        # Μείωση του learning rate
        d2v_model.alpha -= 0.0002
        # Διόρθωση learning rate
        d2v_model.min_alpha = d2v_model.alpha
     
    #Εξαγωγή διανυσμάτων
    vectors = []
    for vector in d2v_model.docvecs.vectors_docs:
        vectors.append(vector)
    sc = StandardScaler()
    vectors = sc.fit_transform(vectors)
       
    return vectors

#Μοντέλο νευρωνικού δικτύου
def NeuralNet(X_train, y_train, vector_size):
    
    model = Sequential()
    model.add(Dense(120, input_dim=vector_size, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    model.fit(np.array(X_train["vector"].to_list()), np.array(y_train.to_list()), epochs=300,
              verbose=1, batch_size = 64)
    
    return model
    


if __name__ == '__main__': 
    
    #Ανάγνωση csv αρχείου
    try:
        mails = pd.read_csv('spam_or_not_spam.csv')
    except IOError:
        #Έξοδος αν αποτύχει
        sys.exit('Δεν υπάρχει το αρχείο αυτό στον φάκελό σας!')
        
    vector_size = 300
    mails_vector = MailEmbeddings(mails, vector_size)

    mails = AddEmbeddings(mails, mails_vector)
    
    #Διαχωρισμός παραδειγμάτων και εκπαίδευση 
    X_train, X_test, y_train, y_test = GetTrainTestData(mails)
    model = NeuralNet(X_train, y_train, vector_size)
    
    #Αξιολόγηση παραδειγμάτων
    predictions = model.predict_classes(np.array(X_test["vector"].to_list()), verbose=0)[:, 0]
    accuracy = skmetrics.accuracy_score(y_test, predictions)
    print('\nAccuracy: %f' % accuracy)
    # precision tp / (tp + fp)
    precision = skmetrics.precision_score(y_test, predictions)
    print('Precision: %f' % precision)
    # recall: tp / (tp + fn)
    recall = skmetrics.recall_score(y_test, predictions)
    print('Recall: %f' % recall)
    # f1: 2 tp / (2 tp + fp + fn)
    f1 = skmetrics.f1_score(y_test, predictions)
    print('F1 score: %f' % f1)
    
    
    
