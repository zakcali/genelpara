# genelpara api V1.6, by Zafer Akçalı
import urllib.request
import urllib.error
import requests
import certifi  # pip install certifi, to be sure to pass ssl verification in every URL
import time
import ssl
import json
from decimal import Decimal


MY_TOKEN = 'enter your token here'
CHAT_ID = 'enter your chat group id here, including minus sign'
API_URL = 'https://api.genelpara.com/embed/borsa.json'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/59.0.3071.115 Safari/537.36'}
CA_WHERE = certifi.where()
SSL_CONTEXT = ssl.create_default_context(cafile=CA_WHERE)
TIME_DELAY = 10*60 # minuntes * seconds
SIGNIFICANT = 0.001 # significant percentage 


def get_response():
    try:
        req = urllib.request.Request(API_URL, headers=HEADERS)
        resp = urllib.request.urlopen(req, context=SSL_CONTEXT)
    except urllib.error.HTTPError as e:
        print("HTTPError:", e.reason)
        exit()
    except urllib.error.URLError as e:
        print("URLError:", e.reason)
        exit()
    byte_code = resp.read().decode()
    api_dict = json.loads(byte_code)
    usd = Decimal(api_dict['USD']['satis'])
    eur = Decimal(api_dict['EUR']['satis'])
    xu100 = Decimal(api_dict['XU100']['satis'])
    btc = Decimal(api_dict['BTC']['satis'])
    eth = Decimal(api_dict['ETH']['satis'])
    return usd, eur, xu100, btc, eth


lastUSD, lastEUR, lastXU100, lastBTC, lastETH = get_response()
while True:
    USD, EUR, XU100, BTC, ETH = get_response()

    difUSD = (USD / lastUSD - 1) * 100
    difEUR = (EUR / lastEUR - 1) * 100
    difXU100 = (XU100 / lastXU100 - 1) * 100
    difBTC = (BTC / lastBTC - 1) * 100
    difETH = (ETH / lastETH - 1) * 100
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    currencies = ["USD  ", difUSD, USD, "EUR  ", difEUR, EUR, "XU100", difXU100, XU100, "BTC  ", difBTC, BTC, "ETH  ", difETH, ETH]
    print("------ Current Time =", current_time, "------")
    for i in range(0, len(currencies), 3):
    	print (currencies[i],":", currencies[i+2], "% difference =", round(currencies[i+1], 2))
    for i in range(0, len(currencies), 3):
        if abs(currencies[i+1]) >= SIGNIFICANT:
            telegram_url = f"https://api.telegram.org/bot{MY_TOKEN}/sendMessage?chat_id={CHAT_ID}&text= {currencies[i]} Alert: {round(currencies[i+1], 2)} {currencies[i+2]} {current_time}"
            requests.get(telegram_url).json()
    lastUSD = USD
    lastEUR = EUR
    lastXU100 = XU100
    lastBTC = BTC
    lastETH = ETH

    time.sleep(TIME_DELAY)
