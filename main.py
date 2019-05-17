import file_parser as file_parser
import requests
from bs4 import BeautifulSoup
import elaborazione_testo as elaborazione_testo
import json
import goslate
from langdetect import detect
import pickle
from dizionarioFooter import dizionarioFooter
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
        page = requests.get(site)
        html_code = page.content
        soup = BeautifulSoup(html_code, 'html.parser')
        print("----------------- "+ site + " -------------")
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out
        text = soup.text
        try:
            language = soup.html["lang"]
            language = language[:2]
        except Exception:
            language = detect(text)
        try:
            cart = soup.select('*[id*='+data[language] +'], *[id*=' +data[language].title() +']*[class*=' +data[language]
                                   +'], *[class*=' +data[language].title() +']')
        except:
            cart = soup.select('*[id*=cart], *[id*=Cart],*[id*=basket], *[id*=Basket], *[class*=cart], *[class*=Cart], *[class*=basket], *[class*=Basket]')

        if cart == []:
            cart = soup.select('*[id*=cart], *[id*=Cart],*[id*=basket], *[id*=Basket], *[class*=cart], *[class*=Cart], *[class*=basket], *[class*=Basket]')

        if cart != [] and label[sites.index(site)] == "1":
            j = j + 1
            print("Ho trovato il carrello e la label è 1")
            print(j)

        trovato = False
        if cart == []:
            footer = soup.select('*[id*=footer], *[id*=Footer]')
            if footer == []:
                footer = soup.select('*[class*=Footer], *[class*=footer]')
                if footer == []:
                    footer = soup.find("footer")
            if footer == None:
                trovato = False
            else:
                footertext = []
                for el in footer:
                    footertext.append(el.text)
                # elimino punteggiatura
                footertext = elaborazione_testo.elimina_punteggiatura(footertext)
                # tokenizzazione
                footertext = elaborazione_testo.tokenize(footertext)
                # trasformo le parole in lettere miniscole
                footertext = elaborazione_testo.trasforma_in_minuscolo(footertext)
                for key in dizionarioFooter:
                    for el in footertext:
                        if dizionarioFooter[key].get("en") in el:
                            trovato = True
                            print(dizionarioFooter[key].get(language))
                        elif dizionarioFooter[key].get(language) in el:
                            print(dizionarioFooter[key].get("en"))
                            trovato = True


            if trovato == True and label[sites.index(site)] == "1":
                j = j + 1
                print("ho trovato una parola chiave nel footer e la label è 1")
                print(j)

            if trovato == False and label[sites.index(site)] == "0":
                j = j + 1
                print("non ho trovato nè carrello nè una parola chiave nel footer e la label è 0")
                print(j)
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
