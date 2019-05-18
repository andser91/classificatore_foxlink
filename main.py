import file_parser as file_parser
import requests
from bs4 import BeautifulSoup
import json
import goslate
from langdetect import detect

sites, label = file_parser.parse("dataset.txt")
gs = goslate.Goslate()
i = 0
x_training = []
x_test = []
y_training = []
y_test = []
with open("lang_file.json",encoding="utf8") as json_file:
    data = json.load(json_file)

print(data["it"])
j = 0
print("==================== Download Pages =====================")
e_commerce = []
for site in sites:
    try:
        i = i+1
        if "amazon" in site:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
            page = requests.get(site, headers=headers)
            soup = BeautifulSoup(page.content, 'lxml')

        else:
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

        # if (cart != [] and label[sites.index(site)] == "1") or (cart == [] and label[sites.index(site)] == "0"):
        #     j = j + 1
        #     print(j)

        if cart != []:
            e_commerce.append(site)
    except Exception as e:
        print(e)

file = open("e_commerce.txt","w")
for url in e_commerce:
    file.write(url+"\n")
file.close()
