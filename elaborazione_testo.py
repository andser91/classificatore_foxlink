from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import  nltk

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


def tokenize(text):
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return word_tokenize(text)


def stopping(words, language):
    try:
        stop_words = set(stopwords.words(LANGUAGE_MAP[language]))
    except Exception:
        stop_words = set(stopwords.words("english"))

    filtered_sentence = [w for w in words if not w in stop_words]
    return filtered_sentence


def trasforma_in_minuscolo(words):
    result = []
    for w in words:
        result.append(w.lower())
    return result