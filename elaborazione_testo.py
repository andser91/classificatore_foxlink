from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import hashlib
from googletrans import Translator
import re, string

LANGUAGE_MAP = {
    "ar":"arabic",
    "az":"azerbaijani",
    "da":"danish",
    "nl":"dutch",
    "en":"english",
    "fi":"finnish",
    "fr":"french",
    "de":"german",
    "el":"greek",
    "hu":"hungarian",
    "id":"indonesian",
    "it":"italian",
    "kk":"kazakh",
    "ne":"nepali",
    "no":"norwegian",
    "pt":"portoguese",
    "ro":"romanian",
    "ru":"russian",
    "es":"spanish",
    "sv":"swedish",
    "tr":"turkish"
}


def tokenize(words):
    new_words = []
    for word in words:
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in word.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        new_words.append(word_tokenize(word))
    return  [val for sublist in new_words for val in sublist]


def stopping(words, language):
    try:
        stop_words = set(stopwords.words(LANGUAGE_MAP[language]))
        filtered_sentence = [w for w in words if not w in stop_words]
    except Exception as e:
        print(e)
        return words
    return filtered_sentence


def trasforma_in_minuscolo(words):
    result = []
    for w in words:
        result.append(w.lower())
    return result


def stemming(words, language):
    try:
        ps = SnowballStemmer(LANGUAGE_MAP[language])
        result = []
        for w in words:
            result.append(ps.stem(w))
        return result
    except Exception:
        return words

def hashing(words):
    result= []
    for w in words:
        hash_object = int(hashlib.md5(w.encode()).hexdigest(),16)
        result.append(hash_object)
    return result

def traduci(words):
    result = []
    translator = Translator()
    for text in words:
        translation = translator.translate(text, dest='en')
        result.append(translation.text)
    return result


def elimina_punteggiatura(words):
    result = []
    for word in words:
        text = re.sub('[% s]' % re.escape(string.punctuation), '', word)
        result.append(text)
    return result