# genelpara api V1.4, by Zafer Akçalı
import urllib.request
import urllib.error
import certifi #pip install certifi, to be sure to pass ssl verification in every URL
import time
import ssl
import json
from decimal import Decimal

API_URL = 'https://api.genelpara.com/embed/borsa.json'
HEADERS={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
TIME_DELAY = 10*60
CA_WHERE=certifi.where()
SSL_CONTEXT = ssl.create_default_context(cafile=CA_WHERE)
def get_response ():
    try:
        req=urllib.request.Request (API_URL, headers=HEADERS)
        resp=urllib.request.urlopen(req, context=SSL_CONTEXT)
    except urllib.error.HTTPError as e:
        print ("HTTPError:", e)
        exit()
    except urllib.error.URLError as e:
        print ("URLError:", e)
        exit()
    byte_code=resp.read().decode()
    api_dict=json.loads(byte_code)
    USD=Decimal(api_dict ['USD']['satis'])
    EUR=Decimal(api_dict ['EUR']['satis'])
    XU100=Decimal(api_dict ['XU100']['satis'])
    BTC=Decimal(api_dict ['BTC']['satis'])
    ETH=Decimal(api_dict ['ETH']['satis'])
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
    print ("USD-sell", usd, "difference % =", round(dif_usd,2))
    print ("EUR-sell", eur, "difference % =", round(dif_eur,2))
    print ("XU100   ", xu100, "difference % =", round(dif_xu100,2))    
    print ("BTC-sell", btc, "difference % =", round(dif_btc,2))
    print ("ETH-sell", eth, "difference % =", round(dif_eth,2))
    
    last_usd=usd
    last_eur=eur
    last_xu100=xu100
    last_btc=btc
    last_eth=eth
    
    time.sleep (TIME_DELAY)