import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
import numpy as np
import sys

def ReadHealthcareData():
    
    #Ανάγνωση csv αρχείου
    try:
        df = pd.read_csv('healthcare-dataset-stroke-data.csv')
    except IOError:
        #Έξοδος αν αποτύχει
        sys.exit('Δεν υπάρχει το αρχείο αυτό στον φάκελό σας!')
        
    return df

def Method1(df):
    
    df1 = df.copy()
    df1 = df1.dropna(axis=1)
    return df1

def Method2(df):
    
    df2 = df.copy()
    bmi_avg = round(df2['bmi'].mean(), 1)

    for index, row in df2.iterrows():
        #Συμπλήρωση με τον μέσο όρο όλων των χρηστών
        if np.isnan(row['bmi']):
            df2.at[index, 'bmi'] = bmi_avg

    return df2

def Method3(df):
    
    #Υποθέτουμε ότι το bmi εξαρτάται από τα επίπεδα γλυκόζης
    #Εναλλακτικά, μπορεί να θεωρηθεί ότι εξαρτάται από την ηλικία
    #x:bmi
    #y:glucose
    # y = x*slope + bias
    
    df3 = df.copy()
    df_dropna = df3.dropna(axis=0)
    glu_avg = round(df_dropna['avg_glucose_level'].mean(), 2)
    bmi_avg = round(df_dropna['bmi'].mean(), 1)
    
    df_regression = df_dropna.copy()
    df_regression['glu_difference'] = df_dropna['avg_glucose_level'] - glu_avg
    df_regression['bmi_difference'] = df_dropna['bmi'] - bmi_avg
    df_regression['bmi_difference_squared'] = df_regression['bmi_difference']**2
    df_regression['diffs_mult'] = df_dropna['avg_glucose_level']*df_dropna['bmi']
    
    slope = round((df_regression['diffs_mult'].sum()/df_regression['bmi_difference_squared'].sum()) , 2)
    bias = round(glu_avg - bmi_avg*slope, 2)
    
    for index, row in df3.iterrows():
        #Συμπλήρωση με linear regression
        if np.isnan(row['bmi']):
            df3.at[index, 'bmi'] = round((df3.at[index, 'avg_glucose_level'] - bias) / slope,1)
            
    return df3

def Method4(df):
    
    df4 = df.copy()
    df_dropna = df4.dropna(axis=0)
    
    x_element = []
    X = []
    y = []
    for index, row in df_dropna.iterrows():
        x_element.append(row['avg_glucose_level'])
        X.append(x_element)
        x_element = []
        y.append(row['bmi'])
        
    neigh = KNeighborsRegressor(n_neighbors=6)
    neigh.fit(X, y)
    
    for index, row in df4.iterrows():
        #Συμπλήρωση με K-Nearest Neighbors
        if np.isnan(row['bmi']):
            df4.at[index, 'bmi'] = round( float(neigh.predict([[row['avg_glucose_level']]])), 1)
    
    return df4


if __name__ == '__main__': 
    
    df = ReadHealthcareData()
    
    df1 = Method1(df)
    df2 = Method2(df)
    df3 = Method3(df)
    df4 = Method4(df)
    

    
    
    
    
