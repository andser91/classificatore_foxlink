import numpy as np


def normalize(dataset):
    x_training = []
    for i in dataset:
        massimo = np.max(i)
        normalized_list = []
        for el in i:
            normalized_list.append(el/massimo)
        x_training.append(normalized_list)
    return x_training


def normalize_list_len(dataset):
    max_length = 0
    for list in dataset:
        if (len(list) > max_length):
            max_length = len(list)
    print(max_length)
    for list in dataset:
        elementi_mancanti = max_length - len(list)
        for i in range(elementi_mancanti):
            list.append(0)


def ciao(dataset):
    lista = []
    for el in dataset:
        el = np.array(el)
        el = el.reshape(10546,1)
        lista.append(el)
    return np.array(lista)

