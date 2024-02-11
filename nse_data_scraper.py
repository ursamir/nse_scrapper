import pandas as pd
import requests
from io import StringIO
import os
import json

root_path = "root_data/"
nseraw_path = "nseraw_data/"
url_nifty50_list = "https://nsearchives.nseindia.com/content/indices/ind_nifty50list.csv"

headers = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'en-US,en;q=0.9',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest',
}

def _create_directory(path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except:
            pass
    
def read_symbol(symbol_list : list,session,path):
    _create_directory(root_path + nseraw_path + path)

    for symbol in symbol_list:
        print(symbol)
        url_symbol = symbol.replace('&','%26')

        response = session.get(f"https://www.nseindia.com/get-quotes/equity?symbol={url_symbol}",headers=headers)
        response.raise_for_status()

        j = {}

        response = session.get(f"https://www.nseindia.com/api/quote-equity?symbol={url_symbol}",headers=headers)
        response.raise_for_status()

        j['companyName'] = response.json()['info']['companyName']
        j['metadata'] = response.json()['metadata']
        j['priceInfo'] = response.json()['priceInfo']
        j['industryInfo'] = response.json()['industryInfo']

        response = session.get(f"https://www.nseindia.com/api/quote-equity?symbol={url_symbol}&section=trade_info",headers=headers)
        response.raise_for_status()

        j['tradeInfo'] = response.json()['marketDeptOrderBook']['tradeInfo']
        j['valueAtRisk'] = response.json()['marketDeptOrderBook']['valueAtRisk']

        response = session.get(f"https://www.nseindia.com/api/chart-databyindex?index={url_symbol}EQN&preopen=true",headers=headers)
        response.raise_for_status()

        j['preopen'] = response.json()['grapthData']

        response = session.get(f"https://www.nseindia.com/api/chart-databyindex?index={url_symbol}EQN",headers=headers)
        response.raise_for_status()

        j['raw'] = response.json()['grapthData']

        with open(root_path + nseraw_path + path + f'{symbol}.json', 'w') as out_file:
            json.dump(j, out_file,indent=4)

def read_index(index,session):
    print(index)
    url_index = index.replace(' ','%20')
    file_index = index.replace(' ','_')

    response = session.get(f"https://www.nseindia.com/market-data/live-equity-market?symbol={url_index}",headers=headers)
    response.raise_for_status()

    response = session.get(f"https://www.nseindia.com/api/equity-stockIndices?index={url_index}",headers=headers)
    response.raise_for_status()

    try:
        if response.json()['data'] != None:
            with open(root_path + nseraw_path + f'{file_index}.json', 'w') as out_file:
                json.dump(response.json()['data'], out_file,indent=4)
            
                df = pd.DataFrame(response.json()['data'])
                symbol_list = df['symbol'].to_list()

                read_symbol(symbol_list[1:],session,f'{file_index}/')

    except:
        pass
    
def read_index_list():
    _create_directory(root_path + nseraw_path)

    response = requests.get("https://www.nseindia.com",headers=headers)
    response.raise_for_status()
    session = requests.Session()

    response = session.get("https://www.nseindia.com/market-data/live-market-indices",headers=headers)
    response.raise_for_status()

    response = session.get("https://www.nseindia.com/api/allIndices",headers=headers)
    response.raise_for_status()

    with open(root_path + nseraw_path + 'index_list.json', 'w') as out_file:
        json.dump(response.json()['data'], out_file,indent=4)

    df = pd.DataFrame(response.json()['data'])
    index_list = df['indexSymbol'].to_list()

    for index in index_list:
        read_index(index,session)


def main():
    read_index_list()

if __name__ == "__main__":
    main()