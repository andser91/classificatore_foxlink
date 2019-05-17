
from googletrans import Translator
from collections import defaultdict
import json

LANGUAGES = ['sq','ar','az','be','bs','bg','zh-cn','zh-tw','hr', 'cs','da','nl','en','et','tl','fi','fr','de', 'el','hu', 'is','id','ga','it', 'ja',
              'ko','no','pl', 'pt', 'ro', 'ru','sr','sk','sl','es', 'sv', 'tr', 'lt','zh-cn']

dictionary = defaultdict()

translator = Translator()
text="delivery"
for lan in LANGUAGES:
    translation = translator.translate(text, dest=lan)
    dictionary[lan] = translation.text


# with open('lang_file.json', 'w') as outfile:
#    json.dump(dictionary, outfile)


with open('lang_fileFooter.json', 'w') as outfile:
   json.dump(dictionary, outfile)