# genelpara api V1.5, by Zafer Akçalı
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
TIME_DELAY = 60
SIGNIFICANT = 0.01


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
    if difUSD >= SIGNIFICANT:
        telegram_url = f"https://api.telegram.org/bot{MY_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=USD Alert: {round(difUSD,2)} {USD} {current_time}"
        requests.get(telegram_url).json()
    if difEUR >= SIGNIFICANT:
        telegram_url = f"https://api.telegram.org/bot{MY_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=EUR Alert: {round(difEUR,2)} {EUR} {current_time}"
        requests.get(telegram_url).json()
    if difXU100 >= SIGNIFICANT:
        telegram_url = f"https://api.telegram.org/bot{MY_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=XU100 Alert: {round(difXU100,2)} {XU100} {current_time}"
        requests.get(telegram_url).json()
    if difBTC >= SIGNIFICANT:
        telegram_url = f"https://api.telegram.org/bot{MY_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=BTC Alert: {round(difBTC,2)} {BTC} {current_time}"
        requests.get(telegram_url).json()
    if difETH >= SIGNIFICANT:
        telegram_url = f"https://api.telegram.org/bot{MY_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=ETH Alert: {round(difETH,2)} {ETH} {current_time}"
        requests.get(telegram_url).json()

    print("------ Current Time =", current_time, "------")
    print("USD-sell", USD, "% difference =", round(difUSD, 2))
    print("EUR-sell", EUR, "% difference =", round(difEUR, 2))
    print("XU100   ", XU100, "% difference =", round(difXU100, 2))
    print("BTC-sell", BTC, "% difference =", round(difBTC, 2))
    print("ETH-sell", ETH, "% difference =", round(difETH, 2))

    lastUSD = USD
    lastEUR = EUR
    lastXU100 = XU100
    lastBTC = BTC
    lastETH = ETH

    time.sleep(TIME_DELAY)
