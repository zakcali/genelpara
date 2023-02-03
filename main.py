# genelpara api V1.1, by Zafer Akçalı
from requests import Session #pip install requests
import certifi #pip install certifi, to be sure to pass ssl verification in every URL
import time

API_URL = 'https://api.genelpara.com/embed/borsa.json'
HEADERS={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
WHERE_CA= certifi.where()
session = Session()
while True:
    response = session.get (API_URL, headers=HEADERS, verify=WHERE_CA)
    if response.status_code != 200:
        print ("Connection error:", response.status_code)
        exit ()
    apiDict=response.json()
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print("Current Time =", current_time)
    print ("USD-sell", apiDict ['USD']['satis'])
    print ("EUR-sell", apiDict ['EUR']['satis'])
    print ("XU100", apiDict ['XU100']['satis'])
    print ("BTC-sell", apiDict ['BTC']['satis'])
    print ("ETH-sell", apiDict ['ETH']['satis'])
    time.sleep (60*60)
