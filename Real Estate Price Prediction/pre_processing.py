import pandas as pd
import sys
import numpy as np

#Αποθήκευση αρχείου σε dataset
def ReadHousingData():
    
    #Ανάγνωση csv αρχείου
    try:
        df = pd.read_csv('housing.csv')
    except IOError:
        #Έξοδος αν αποτύχει
        sys.exit('Δεν υπάρχει το αρχείο αυτό στον φάκελό σας!')
        
    return df

def Preprocess(df):
    
    print("\n---------------Προ-Επεξεργασία Δεδομένων---------------\n")
    
    mul = 1
    
    columns = list(df)
    numeric_columns = []
    string_columns = []
    has_nan_columns = []

    for column in columns:
        if(isinstance(df[column][0], str)):
            string_columns.append(column)
            
            ohe_df = pd.get_dummies(df[column], prefix=column)
            del df[column]
            new_df = pd.concat([df, ohe_df], axis=1, join='inner')
            df = new_df
            
        else:
            numeric_columns.append(column)
            df[column] = (df[column] - df[column].min())/(df[column].max() - df[column].min()) * mul
            
            if(df[column].isnull().values.any()):
                has_nan_columns.append(column)
                for index, row in df.iterrows():
                    #Συμπλήρωση με τον μέσο όρο όλων των χρηστών
                    if np.isnan(row[column]):
                        df.at[index, column] = df[column].mean()
    
    if(len(numeric_columns)>0):
        print("Αριθμητικά Χαρακτηριστικά:")
        for i in numeric_columns:
            print(i)
    
    if(len(string_columns)>0):
        print("\nΚατηγορικά Χαρακτηριστικά:")
        for i in string_columns:
            print(i)
    
    if(len(has_nan_columns)>0):
        print("\nΧαρακτηριστικά με ελλιπείς τιμές:")
        for i in has_nan_columns:
            print(i)
    
    print("\nΤα αριθμητικά χαρακτηριστικάν μετατράπηκαν στην ίδια κλίμακα")
    print("\nTa κατηγορικά χαρακτηριστικά αντικαταστάθηκαν από στήλες σε μορφή One-Hot Encoding")
    print("\nΟι ελλιπείς αριθμητικές τιμές αντικαταστάθηκαν με τις μέσες τιμές της στήλης")
    #print(df)
    
    return (df)

if __name__ == '__main__': 
    
    df = ReadHousingData()
    new_df = Preprocess(df)
    

        
    