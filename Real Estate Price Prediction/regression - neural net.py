import pandas as pd
import sys
from sklearn.model_selection import KFold
from pre_processing import Preprocess
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

#Αποθήκευση αρχείου σε dataset
def ReadHousingData():
    
    #Ανάγνωση csv αρχείου
    try:
        df = pd.read_csv('housing.csv')
    except IOError:
        #Έξοδος αν αποτύχει
        sys.exit('Δεν υπάρχει το αρχείο αυτό στον φάκελό σας!')
        
    return df

if __name__ == '__main__': 
    
    df = ReadHousingData()
    df = Preprocess(df)
    
    print("\n---------------Εκπαίδευση και Έλεγχος---------------\n")
    
    lr = 0.001
    x_values = 13
    
    folds = 10.0
    kfold = KFold(int(folds), shuffle = True)
    
    train_mae = 0
    train_mse = 0
    test_mae = 0
    test_mse = 0
    final_w = [0]*x_values
    final_c = 0
    
    model = keras.Sequential([
            layers.Dense(64, input_dim= 13, activation='relu'),
            layers.Dense(32, activation='relu'),
            layers.Dense(1)])
    
    fold_counter = 1
    for train_index, test_index in kfold.split(df):
        print("Fold ", fold_counter, "...")
        train_df = df.loc[train_index, :]
        test_df = df.loc[test_index, :]
        
        #train
        y_train = train_df.iloc[:, 8]
        x_train = train_df.drop(["median_house_value"], axis = 1)
        
        model.compile(loss='mean_absolute_error',
                      optimizer=tf.keras.optimizers.Adam(lr), metrics = ['mae', 'mse'])
        
        #train
        history = model.fit(x_train, y_train,verbose=0, epochs=30)
        
        train_mae += history.history['mae'][-1]
        train_mse += history.history['mse'][-1]
        
        
        #test
        y_test = test_df.iloc[:, 8]
        x_test = test_df.drop(["median_house_value"], axis = 1)
        y_pred = model.predict(x_test).flatten()
        
        n = len(x_test)
        test_mae += (1/n) * sum(abs(y_test - y_pred))
        test_mse += (1/n) * sum((y_test - y_pred)**2)
        
        fold_counter += 1
    
    print("\nΜέσο τετραγωνικό σφάλμα εκπαίδευσης =", train_mse/folds )
    print("Μέσο απόλυτο σφάλμα εκπαίδευσης =", train_mae/folds )
    print("Μέσο τετραγωνικό σφάλμα ελέγχου =", test_mse/folds )
    print("Μέσο απόλυτο σφάλμα ελέγχου =", test_mae/folds )

