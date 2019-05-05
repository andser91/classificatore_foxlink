import keras
import tensorflow as tf
import numpy as np
import  pickle
import utils

NUMERO_CLASSI = 2

def train():

    ## Carico il dataset
    pickle_in = open("x_train.pickle", "rb")
    x_train = np.array(pickle.load(pickle_in))
    pickle_in = open("y_train.pickle", "rb")
    y_train = np.array(pickle.load(pickle_in))

    pickle_in = open("x_test.pickle", "rb")
    x_test = np.array(pickle.load(pickle_in))
    pickle_in = open("y_test.pickle", "rb")
    y_test = np.array(pickle.load(pickle_in))

    ## Normalizzo i dati
    x_train = np.array(utils.normalize(x_train))
    x_test = np.array(utils.normalize(x_test))

    for i in range(len(x_train)):
        print(len(x_train[i]))

    ## Normalizzo la lunghezza dell'input
    utils.normalize_list_len(x_train)
    utils.normalize_list_len(x_test)


    # Uso codifica onehot: abbiamo 2 classi
    y_train = np.array(y_train)
    y_test = np.array(y_test)

    y_train = keras.utils.to_categorical(y_train, NUMERO_CLASSI)
    y_test = keras.utils.to_categorical(y_test, NUMERO_CLASSI)



    # for i in range(len(x_train)):
    #     x_train[i] = np.array(x_train[i])
    #
    # for i in range(len(x_test)):
    #     x_test[i] = np.array(x_test[i])

    x_train = utils.ciao(x_train)

    ## Creo il modello
    model = tf.keras.models.Sequential()

    # hidden layer:
    model.add(tf.keras.layers.Dense(128,activation=tf.nn.softmax))

    model.add(tf.keras.layers.Dense(128, activation=tf.nn.softmax))

    # output layer:
    model.add(tf.keras.layers.Dense(2, activation=tf.nn.softmax))

    # parametri per training modello:
    model.compile(optimizer='sgd',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'],
                  lr=0.1)

    # training:
    model.fit(x_train, y_train, epochs=3, batch_size=1)

    # valuto modello con il test set e lo salvo
    val_loss, val_acc = model.evaluate(x_test, y_test)
    print("Valutazione modello su test set:")

    print("Loss: " + str(val_loss))
    print("Accuratezza: " + str(val_acc))
    model.save('modello.model')

train()