import file_parser as file_parser
import requests
from bs4 import BeautifulSoup
import elaborazione_testo as elaborazione_testo
from langdetect import detect
import re, string
import nltk

# costruisco il training set
sites, label = file_parser.parse("domini_negativi.txt")

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

        # detect della lingua del sito
        try:
            language = soup.html["lang"]
            language = language[:2]
        except Exception:
            language = detect(text)

        # tokenizzazione
        words = elaborazione_testo.tokenize(text)
        print(words)

        # trasformo le parole in lettere miniscole
        words = elaborazione_testo.trasforma_in_minuscolo(words)

        # stopping in base al linguaggio
        words = elaborazione_testo.stopping(words, language)
        #print(words)
    except requests.exceptions.RequestException as e:
        print(e)

