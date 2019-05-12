import numpy as np
import requests
from bs4 import BeautifulSoup

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
    for i in dataset:
        if len(i) > max_length:
            max_length = len(i)
    print(max_length)
    max_length = 1000
    result = []
    i = 0
    for list in dataset:
        while len(list) < max_length:
            for i in range (0,len(list)):
                list.append(list[i])
        list = list[:max_length]
        result.append(list)
    return result


def ciao(dataset):
    lista = []
    for el in dataset:
        el = np.array(el)
        el = el.reshape(1000,1)
        lista.append(el)
    return lista

def getWordFromSite(site):
    try:
        page = requests.get(site)
        html_code = page.content
        soup = BeautifulSoup(html_code, 'html.parser')
        # text = soup.text
        print("----------------- " + site + " -------------")
        return soup.title.text
    except Exception as e:
        print(e)

