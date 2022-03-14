import pandas as pd
import sys
from sklearn.model_selection import KFold
from pre_processing import Preprocess

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
    
    lr = 0.1
    epochs = 1000
    x_values = 13
    
    folds = 10.0
    kfold = KFold(int(folds), shuffle = True)
    
    train_mae = 0
    train_mse = 0
    test_mae = 0
    test_mse = 0
    final_w = [0]*x_values
    final_c = 0
    
    fold_counter = 1
    for train_index, test_index in kfold.split(df):
        print("Fold ", fold_counter, "...")
        train_df = df.loc[train_index, :]
        test_df = df.loc[test_index, :]
        
        #train
        y_train = train_df.iloc[:, 8]
        x_train = train_df.drop(["median_house_value"], axis = 1)
        
        n = len(x_train)
        
        #y = w0x0 + w1x1 + w2x2 + w3x3 + w4x4 + w5x5 + w6x6 + w7x7 +
        #    w8x8 + w9x9 + w10x10 + w11x11 + w12x12 + w13x13 + c
        x = [0]*x_values
        for i in range(x_values):
            x[i] = x_train.iloc[:, i]
        w = [0]*x_values
        c = 0
        
        for i in range (epochs):
            y_pred = c
            for j in range (x_values):
                y_pred += w[j]*x[j] 
            
            for j in range(x_values):
                dw = (-2/n) * sum(x[j] * (y_train - y_pred))
                w[j] = w[j] - lr*dw
            
            dc = (-2/n) * sum(y_train - y_pred)  
            c = c - lr*dc
            
        y_pred = c
        for j in range (x_values):
            y_pred += w[j]*x[j] 
        
        for i in range(x_values):
            final_w[i] += w[i]
        final_c += c
        
        train_mae += (1/n) * sum(abs(y_train - y_pred))
        train_mse += (1/n) * sum((y_train - y_pred)**2)
        
        #test
        y_test = test_df.iloc[:, 8]
        x_test = test_df.drop(["median_house_value"], axis = 1)
        
        x = [0]*x_values
        for i in range(x_values):
            x[i] = x_test.iloc[:, i]
        
        y_pred = c
        for j in range (x_values):
            y_pred += w[j]*x[j] 
        
        n = len(x_test)
        test_mae += (1/n) * sum(abs(y_test - y_pred))
        test_mse += (1/n) * sum((y_test - y_pred)**2)
        
        fold_counter += 1
    
    for i in range(x_values): 
        final_w[i] = final_w[i]/folds
    final_c = final_c/folds
    
    print("\nΜέσο τετραγωνικό σφάλμα εκπαίδευσης =", train_mse/folds )
    print("Μέσο απόλυτο σφάλμα εκπαίδευσης =", train_mae/folds )
    print("Μέσο τετραγωνικό σφάλμα ελέγχου =", test_mse/folds )
    print("Μέσο απόλυτο σφάλμα ελέγχου =", test_mae/folds )
    print("Βάρη εξίσωσης μοντέλου γραμμικής παλινδρόμησης:", final_w, final_c)
            


