# genelpara api V1.0, by Zafer Akçalı
from requests import Session #pip install requests
import certifi #pip install certifi, to be sure to pass ssl verification in every URL

API_URL = 'https://api.genelpara.com/embed/borsa.json'
HEADERS={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
WHERE_CA= certifi.where()
session = Session()
response = session.get (API_URL, headers=HEADERS, verify=WHERE_CA)
if response.status_code != 200:
    print ("Connection error:", response.status_code)
    exit ()
apiDict=eval(response.content)
print ("USD-sell", apiDict ['USD']['satis'])
print ("EUR-sell", apiDict ['EUR']['satis'])
print ("XU100", apiDict ['XU100']['satis'])
print ("BTC-sell", apiDict ['BTC']['satis'])
print ("ETH-sell", apiDict ['ETH']['satis'])

