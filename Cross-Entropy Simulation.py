# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Απαραίτητες βιβλιοθήκες
import numpy as np
import keras as keras
from keras.models import Sequential
from keras.layers import Dense

##Μεγέθη σετ δεδομένων τεστ και εκπαίδευσης αντίστοιχα
pair_number = 1000000
training_number = 200

##Δημιουργία του πίνακα τεστ δεδομένων όπως στο Bayes πρόβλημα
f0_data = np.random.multivariate_normal([0, 0] , [[1 , 0],[0 , 1]] ,pair_number)
f1_data = np.random.multivariate_normal([-1, 1] , [[1 , 0],[0 , 1]] ,pair_number)

##Ένωση τεστ δεδομένων σε κοινό πίνακα μεγέθους 2.000.000
test_table = np.concatenate((f0_data, f1_data))

##Δημιουργία πίνακα τεστ πιαθανοτήτων μεγέθους 2.000.000
##Ο μισός αποτελείται από 0, ο άλλος μισός από 1
test_possibilities = [0 for q in range(pair_number*2)]
for i in range(pair_number):
    test_possibilities[i + pair_number] = 1

##Δημιουργία του πίνακα δεδομένων εκπαίδευσης όπως στο Bayes πρόβλημα
f0_training = np.random.multivariate_normal([0, 0] , [[1 , 0],[0 , 1]] ,training_number)
f1_training = np.random.multivariate_normal([-1, 1] , [[1 , 0],[0 , 1]] ,training_number)

##Ένωση δεδομένων εκπαίδευσης σε κοινό πίνακα μεγέθους 400
training_table = np.concatenate((f0_training, f1_training))

##Δημιουργία πίνακα πιθαανοτήτων εκπαίδευσης μεγέθους 400
##Ο μισός αποτελείται από 0, ο άλλος μισός από 1
training_possibilities = [0 for q in range(training_number*2)]
for i in range(training_number):
    training_possibilities[i + training_number] = 1

##Δημιουργία νευρωνικού δικτύου
keras.initializers.RandomNormal(mean=0.0, stddev=(1/20), seed=None)
model = Sequential()
model.add(Dense(20, input_dim=2, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

##Compile
keras.optimizers.SGD(learning_rate = 0.0002)
model.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])

##Εκπαίδευση
history = model.fit(training_table, training_possibilities,
                    epochs=500, batch_size=20)


loss, accuracy = model.evaluate(test_table, test_possibilities)

print('Accuracy: %.2f' % (accuracy*100)+'%')
print('Loss: %.2f' % (loss*100)+'%')

loss_log = history.history["loss"]
loss_data={"loss": loss_log}
frame = pd.DataFrame(loss_data)
last_20 = df.rolling(window=20).mean()




