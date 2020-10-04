# -*- coding: utf-8 -*-
"""

@author: john-
"""
from __future__ import print_function
import keras
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense


##Όλα τα δεδομένα σε πίνακες train και test
(x_train, y_train), (x_test, y_test) = mnist.load_data()

##Training sets
##Φίλτρο για να απομονώσουμε τα 0 και τα 8
filter_08_train = np.where((y_train == 0 ) | (y_train == 8))

##Εφαρμογή φίλτρου
binary_x_train = x_train[filter_08_train]
binary_y_train =  y_train[filter_08_train]

##Διαίρεση με το 255 γιατι τα επίπεδα είναι μεταξύ οτυ [0,255]
binary_x_train = binary_x_train / 255

##Απόδοση της τιμής 1, όπου ο πίνακας πιθανοτήτων έχει 8
for i in range(len(binary_y_train)):
    if (binary_y_train[i] == 8): binary_y_train[i] = 1

##Μετασχηματισμός φωτογραφιών σε ένα διάνυσμα μεγέθους 784
binary_x_train = binary_x_train.reshape((-1, 784))


##Test sets
##Φίλτρο για να απομονώσουμε τα 0 και τα 8
filter_08_test = np.where((y_test == 0) | (y_test == 8))

binary_x_test = x_test[filter_08_test]
binary_y_test = y_test[filter_08_test]

binary_x_test =  binary_x_test / 255

##Απόδοση της τιμής 1, όπου ο πίνακας πιθανοτήτων έχει 8
for i in range(len(binary_y_test)):
    if (binary_y_test[i] == 8): binary_y_test[i] = 1

##Μετασχηματισμός φωτογραφιών σε ένα διάνυσμα μεγέθους 784
binary_x_test = binary_x_test.reshape((-1, 784))


#Κατασκευή νευρωνικού
model = Sequential()
model.add(Dense(300, input_shape=(784,), activation = 'relu'))
model.add(Dense(1, activation='sigmoid'))

##Παράμετροι
keras.optimizers.SGD(learning_rate = 0.0002)
model.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])

##Εκπαίδευση
history = model.fit(binary_x_train, binary_y_train,
          batch_size=128, epochs=50, verbose=2,
          validation_data=(binary_x_test, binary_y_test))


##Αξιολόγηση
loss, accuracy = model.evaluate(binary_x_test, binary_y_test, verbose=0)
print('Test loss:', loss)
print('Test accuracy:', accuracy)

##Αποθήκευση όλων των απωλειών
loss_log = history.history["loss"]
loss_data={"loss": loss_log}
frame = pd.DataFrame(loss_data)
last_20 = frame.rolling(window=20).mean()

##plots
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

plt.plot(history.history['loss']) 
plt.plot(history.history['val_loss']) 
plt.title('Model loss') 
plt.ylabel('Loss') 
plt.xlabel('Epoch') 
plt.legend(['Train', 'Test'], loc='upper left') 
plt.show()

