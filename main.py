import file_parser as file_parser
import requests
from bs4 import BeautifulSoup
import elaborazione_testo as elaborazione_testo
from langdetect import detect
import re, string
import pickle
#import training

# costruisco il training set
sites, label = file_parser.parse("dataset.txt")
i = 0
x_training = []
x_test = []
y_training = []
y_test = []

print("==================== Download Pages =====================")
for site in sites:
    try:
        page = requests.get(site)
        html_code = page.content
        soup = BeautifulSoup(html_code, 'html.parser')
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out
        # get text
        text = soup.get_text()
        text = re.sub('[% s]' % re.escape(string.punctuation), '', text)

        # tokenizzazione
        words = elaborazione_testo.tokenize(text)

        #Se la pagina ha meno di 10 parole non considerarla
        if len(words) < 10:
            continue

        # trasformo le parole in lettere miniscole
        words = elaborazione_testo.trasforma_in_minuscolo(words)

        # detect della lingua del sito
        try:
            language = soup.html["lang"]
            language = language[:2]
        except Exception:
            language = detect(text)

        # stopping in base al linguaggio
        words = elaborazione_testo.stopping(words, language)
        #print(words)

        #stemming
        words = elaborazione_testo.stemming(words, language)

        #hashing
        words= elaborazione_testo.hashing(words)
        print(len(words), site)

        ## differenzio tra training e test set
        if i < 260:
            x_training.append(words)
            y_training.append(label[i])
        else:
            x_test.append(words)
            y_test.append(label[i])
        i = i + 1
    except Exception as e:
        print(e)


### Salvo il dataset su file
print("================== Creating dataset =====================")
pickle_out = open("x_train.pickle","wb")
pickle.dump(x_training, pickle_out)
pickle_out.close()

pickle_out = open("y_train.pickle","wb")
pickle.dump(y_training, pickle_out)
pickle_out.close()

#Salva test set
pickle_out = open("x_test.pickle","wb")
pickle.dump(x_test, pickle_out)
pickle_out.close()

pickle_out = open("y_test.pickle","wb")
pickle.dump(y_test, pickle_out)
pickle_out.close()

#training.train()
