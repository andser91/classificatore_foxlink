import file_parser as file_parser
import requests
from bs4 import BeautifulSoup
import elaborazione_testo as elaborazione_testo
import json
import goslate
from langdetect import detect
import pickle
#import training
import utils

# costruisco il training set
sites, label = file_parser.parse("dataset.txt")
gs = goslate.Goslate()
i = 0
x_training = []
x_test = []
y_training = []
y_test = []
with open("lang_file.json") as json_file:
    data = json.load(json_file)

print(data["it"])
j = 0
print("==================== Download Pages =====================")
for site in sites:
    try:
        i = i+1
        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'}

        page = requests.get("https://www.instant-gaming.com", headers=headers)
        html_code = page.content
        soup = BeautifulSoup(html_code, 'html.parser')
        words = []
        print("----------------- "+ site + " -------------")
        #words.append(soup.title.text)

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        text = soup.text

        try:
            language = soup.html["lang"]
            language = language[:2]
        except Exception:
            language = detect(text)

        cart = soup.select('*[id*=cart], *[id*=Cart],*[id*=basket], *[id*=Basket], *[id*='
                           +data[language] +'], *[id*=' +data[language].title() +']')
        if cart == []:
            cart = soup.select('*[class*=cart], *[class*=Cart], *[class*=basket], *[class*=Basket], *[class*=' +data[language]
                               +'], *[class*=' +data[language].title() +']')

        if cart == []:
            footer = soup.select('*[id*=footer], *[id*=Footer]')
            if footer == []:
                footer = soup.select('*[class*=Footer], *[class*=footer]')

        for el in footer:
            print (el.text)


       #if footer == []:



        # if (cart != [] and label[sites.index(site)] == "1") or cart == [] and label[sites.index(site)] == "0" :
        #     j = j + 1

        # if cart == []:
        #     cart = soup.select('*[class*='+ gs.translate('cart', language)+']')
        #     print(cart)

        # meta_list = soup.find_all("meta", attrs={"name" : "description"})
        #
        # for meta in meta_list:
        #      words.append(meta["content"])
        #
        # # link_list = soup.find_all('a', href=True)
        # # for link in link_list:
        # #     if not ("http" in link['href'] or "javascript" in link['href'] or "www." in link['href'] or link['href'] == "#"):
        # #         words.append(utils.getWordFromSite(site + link['href']))
        # #         print(words)
        #
        #
        # link_list = soup.find_all('a', href=True)
        # for link in link_list:
        #     if not ("http" in link['href'] or "javascript" in link['href'] or "www." in link['href']):
        #         if not (link.text == ""):
        #             words.append(link.text.strip("\n"))
        #
        # # elimino punteggiatura
        # words = elaborazione_testo.elimina_punteggiatura(words)
        #
        # # # traduco in inglese
        # # words = elaborazione_testo.traduci(words)
        #
        # # tokenizzazione
        # words = elaborazione_testo.tokenize(words)
        #
        # #Se la pagina ha meno di 10 parole non considerarla
        # if len(words) < 1:
        #     continue
        #
        # # trasformo le parole in lettere miniscole
        # words = elaborazione_testo.trasforma_in_minuscolo(words)
        #
        # # detect della lingua del sito


        # # stopping in base al linguaggio
        # words = elaborazione_testo.stopping(words, language)
        # #print(words)
        #
        # #stemming
        # words = elaborazione_testo.stemming(words, language)
        #
        # print(words)
        #
        # #hashing
        # words= elaborazione_testo.hashing(words)
        #
        # print(words)
        #
        # ## differenzio tra training e test set
        # x_training.append(words)
        # y_training.append(label[i])
        # i = i + 1
    except Exception as e:
        print(e)
print(j)

### Salvo il dataset su file
print("================== Creating dataset =====================")
pickle_out = open("x_train.pickle","wb")
pickle.dump(x_training, pickle_out)
pickle_out.close()

pickle_out = open("y_train.pickle","wb")
pickle.dump(y_training, pickle_out)
pickle_out.close()

# #training.train()
