# genelpara api V1.2, by Zafer Akçalı
from requests import Session #pip install requests
import certifi #pip install certifi, to be sure to pass ssl verification in every URL
import time
from decimal import Decimal

API_URL = 'https://api.genelpara.com/embed/borsa.json'
HEADERS={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
WHERE_CA= certifi.where()
TIME_DELAY = 60
session = Session()
def get_response ():
    response = session.get (API_URL, headers=HEADERS, verify=WHERE_CA)
    if response.status_code != 200:
        print ("Connection error:", response.status_code)
        exit ()
    apiDict=response.json()
    USD=Decimal(apiDict ['USD']['satis'])
    EUR=Decimal(apiDict ['EUR']['satis'])
    XU100=Decimal(apiDict ['XU100']['satis'])
    BTC=Decimal(apiDict ['BTC']['satis'])
    ETH=Decimal(apiDict ['ETH']['satis'])
    return (USD,EUR,XU100,BTC,ETH)

last_usd,last_eur,last_xu100,last_btc,last_eth = get_response()
while True:
    usd, eur, xu100, btc, eth = get_response()

    dif_usd=(usd/last_usd-1)*100
    dif_eur=(eur/last_eur-1)*100
    dif_xu100=(xu100/last_xu100-1)*100
    dif_btc=(btc/last_btc-1)*100
    dif_eth=(eth/last_eth-1)*100
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    
    print("------Current Time =", current_time,"------")
    print ("USD-sell", usd, "difference % =", dif_usd)
    print ("EUR-sell", eur, "difference % =", dif_eur)
    print ("XU100   ", xu100, "difference % =", dif_xu100)    
    print ("BTC-sell", btc, "difference % =", dif_btc)
    print ("ETH-sell", eth, "difference % =", dif_eth)
    
    last_usd=usd
    last_eur=eur
    last_xu100=xu100
    last_btc=btc
    last_eth=eth
    
    time.sleep (TIME_DELAY)