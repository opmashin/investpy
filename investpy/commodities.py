#!/usr/bin/python3

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

from datetime import datetime, date
import json
from random import randint

import pandas as pd
import pkg_resources
import requests
import unidecode
from lxml.html import fromstring

from investpy.utils.user_agent import get_random
from investpy.utils.data import Data

from investpy.data.commodities_data import commodities_as_df, commodities_as_list, commodities_as_dict
from investpy.data.commodities_data import commodity_groups_list


def get_commodities(group=None):
    """
    """

    return commodities_as_df(group=group)


def get_commodities_list(group=None):
    """
    """

    return commodities_as_list(group=group)


def get_commodities_dict(group=None, columns=None, as_json=False):
    """
    """

    return commodities_as_dict(group=group, columns=columns, as_json=as_json)


def get_commodity_groups():
    """
    """

    return commodity_groups_list()


# def get_commodity_recent_data(stock, country, as_json=False, order='ascending', interval='Daily'):
#     """
#     """

#     if not stock:
#         raise ValueError("ERR#0013: stock parameter is mandatory and must be a valid stock name.")

#     if not isinstance(stock, str):
#         raise ValueError("ERR#0027: stock argument needs to be a str.")

#     if country is None:
#         raise ValueError("ERR#0039: country can not be None, it should be a str.")

#     if country is not None and not isinstance(country, str):
#         raise ValueError("ERR#0025: specified country value not valid.")

#     if not isinstance(as_json, bool):
#         raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

#     if order not in ['ascending', 'asc', 'descending', 'desc']:
#         raise ValueError("ERR#0003: order argument can just be ascending (asc) or descending (desc), str type.")

#     if not interval:
#         raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")

#     if not isinstance(interval, str):
#         raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")

#     if interval not in ['Daily', 'Weekly', 'Monthly']:
#         raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")

#     resource_package = 'investpy'
#     resource_path = '/'.join(('resources', 'stocks', 'stocks.csv'))
#     if pkg_resources.resource_exists(resource_package, resource_path):
#         stocks = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
#     else:
#         raise FileNotFoundError("ERR#0056: stocks file not found or errored.")

#     if stocks is None:
#         raise IOError("ERR#0001: stocks object not found or unable to retrieve.")

#     if unidecode.unidecode(country.lower()) not in get_stock_countries():
#         raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

#     stocks = stocks[stocks['country'] == unidecode.unidecode(country.lower())]

#     stock = stock.strip()
#     stock = stock.lower()

#     if unidecode.unidecode(stock) not in [unidecode.unidecode(value.lower()) for value in stocks['symbol'].tolist()]:
#         raise RuntimeError("ERR#0018: stock " + stock + " not found, check if it is correct.")

#     symbol = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'symbol']
#     id_ = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'id']
#     name = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'name']

#     stock_currency = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'currency']

#     header = symbol + ' Historical Data'

#     params = {
#         "curr_id": id_,
#         "smlID": str(randint(1000000, 99999999)),
#         "header": header,
#         "interval_sec": interval,
#         "sort_col": "date",
#         "sort_ord": "DESC",
#         "action": "historical_data"
#     }

#     head = {
#         "User-Agent": get_random(),
#         "X-Requested-With": "XMLHttpRequest",
#         "Accept": "text/html",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Connection": "keep-alive",
#     }

#     url = "https://www.investing.com/instruments/HistoricalDataAjax"

#     req = requests.post(url, headers=head, data=params)

#     if req.status_code != 200:
#         raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

#     root_ = fromstring(req.text)
#     path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
#     result = list()

#     if path_:
#         for elements_ in path_:
#             if elements_.xpath(".//td")[0].text_content() == 'No results found':
#                 raise IndexError("ERR#0007: stock information unavailable or not found.")

#             info = []

#             for nested_ in elements_.xpath(".//td"):
#                 info.append(nested_.get('data-real-value'))

#             stock_date = datetime.fromtimestamp(int(info[0]))
#             stock_date = date(stock_date.year, stock_date.month, stock_date.day)
            
#             stock_close = float(info[1].replace(',', ''))
#             stock_open = float(info[2].replace(',', ''))
#             stock_high = float(info[3].replace(',', ''))
#             stock_low = float(info[4].replace(',', ''))

#             stock_volume = 0

#             if info[5].__contains__('K'):
#                 stock_volume = int(float(info[5].replace('K', '').replace(',', '')) * 1e3)
#             elif info[5].__contains__('M'):
#                 stock_volume = int(float(info[5].replace('M', '').replace(',', '')) * 1e6)
#             elif info[5].__contains__('B'):
#                 stock_volume = int(float(info[5].replace('B', '').replace(',', '')) * 1e9)

#             result.insert(len(result),
#                           Data(stock_date, stock_open, stock_high, stock_low,
#                                stock_close, stock_volume, stock_currency))

#         if order in ['ascending', 'asc']:
#             result = result[::-1]
#         elif order in ['descending', 'desc']:
#             result = result

#         if as_json is True:
#             json_ = {'name': name,
#                         'recent':
#                             [value.stock_as_json() for value in result]
#                         }

#             return json.dumps(json_, sort_keys=False)
#         elif as_json is False:
#             df = pd.DataFrame.from_records([value.stock_to_dict() for value in result])
#             df.set_index('Date', inplace=True)

#             return df
#     else:
#         raise RuntimeError("ERR#0004: data retrieval error while scraping.")


# def get_commodity_historical_data(stock, country, from_date, to_date, as_json=False, order='ascending', interval='Daily'):
#     """

#     """

#     if not stock:
#         raise ValueError("ERR#0013: stock parameter is mandatory and must be a valid stock name.")

#     if not isinstance(stock, str):
#         raise ValueError("ERR#0027: stock argument needs to be a str.")

#     if country is None:
#         raise ValueError("ERR#0039: country can not be None, it should be a str.")

#     if country is not None and not isinstance(country, str):
#         raise ValueError("ERR#0025: specified country value not valid.")

#     if not isinstance(as_json, bool):
#         raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

#     if order not in ['ascending', 'asc', 'descending', 'desc']:
#         raise ValueError("ERR#0003: order argument can just be ascending (asc) or descending (desc), str type.")

#     if not interval:
#         raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")

#     if not isinstance(interval, str):
#         raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")

#     if interval not in ['Daily', 'Weekly', 'Monthly']:
#         raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")

#     try:
#         datetime.strptime(from_date, '%d/%m/%Y')
#     except ValueError:
#         raise ValueError("ERR#0011: incorrect from_date date format, it should be 'dd/mm/yyyy'.")

#     try:
#         datetime.strptime(to_date, '%d/%m/%Y')
#     except ValueError:
#         raise ValueError("ERR#0012: incorrect to_date format, it should be 'dd/mm/yyyy'.")

#     start_date = datetime.strptime(from_date, '%d/%m/%Y')
#     end_date = datetime.strptime(to_date, '%d/%m/%Y')

#     if start_date >= end_date:
#         raise ValueError("ERR#0032: to_date should be greater than from_date, both formatted as 'dd/mm/yyyy'.")

#     date_interval = {
#         'intervals': [],
#     }

#     flag = True

#     while flag is True:
#         diff = end_date.year - start_date.year

#         if diff > 20:
#             obj = {
#                 'start': start_date.strftime('%d/%m/%Y'),
#                 'end': start_date.replace(year=start_date.year + 20).strftime('%d/%m/%Y'),
#             }

#             date_interval['intervals'].append(obj)

#             start_date = start_date.replace(year=start_date.year + 20)
#         else:
#             obj = {
#                 'start': start_date.strftime('%d/%m/%Y'),
#                 'end': end_date.strftime('%d/%m/%Y'),
#             }

#             date_interval['intervals'].append(obj)

#             flag = False

#     interval_limit = len(date_interval['intervals'])
#     interval_counter = 0

#     data_flag = False

#     resource_package = 'investpy'
#     resource_path = '/'.join(('resources', 'stocks', 'stocks.csv'))
#     if pkg_resources.resource_exists(resource_package, resource_path):
#         stocks = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
#     else:
#         raise FileNotFoundError("ERR#0056: stocks file not found or errored.")

#     if stocks is None:
#         raise IOError("ERR#0001: stocks object not found or unable to retrieve.")

#     if unidecode.unidecode(country.lower()) not in get_stock_countries():
#         raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

#     stocks = stocks[stocks['country'] == unidecode.unidecode(country.lower())]

#     stock = stock.strip()
#     stock = stock.lower()

#     if unidecode.unidecode(stock) not in [unidecode.unidecode(value.lower()) for value in stocks['symbol'].tolist()]:
#         raise RuntimeError("ERR#0018: stock " + stock + " not found, check if it is correct.")

#     symbol = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'symbol']
#     id_ = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'id']
#     name = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'name']

#     stock_currency = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'currency']

#     final = list()

#     header = symbol + ' Historical Data'

#     for index in range(len(date_interval['intervals'])):
#         interval_counter += 1

#         params = {
#             "curr_id": id_,
#             "smlID": str(randint(1000000, 99999999)),
#             "header": header,
#             "st_date": date_interval['intervals'][index]['start'],
#             "end_date": date_interval['intervals'][index]['end'],
#             "interval_sec": interval,
#             "sort_col": "date",
#             "sort_ord": "DESC",
#             "action": "historical_data"
#         }

#         head = {
#             "User-Agent": get_random(),
#             "X-Requested-With": "XMLHttpRequest",
#             "Accept": "text/html",
#             "Accept-Encoding": "gzip, deflate, br",
#             "Connection": "keep-alive",
#         }

#         url = "https://www.investing.com/instruments/HistoricalDataAjax"

#         req = requests.post(url, headers=head, data=params)

#         if req.status_code != 200:
#             raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

#         if not req.text:
#             continue

#         root_ = fromstring(req.text)
#         path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")

#         result = list()

#         if path_:
#             for elements_ in path_:
#                 if elements_.xpath(".//td")[0].text_content() == 'No results found':
#                     if interval_counter < interval_limit:
#                         data_flag = False
#                     else:
#                         raise IndexError("ERR#0007: stock information unavailable or not found.")
#                 else:
#                     data_flag = True
                
#                 info = []
            
#                 for nested_ in elements_.xpath(".//td"):
#                     info.append(nested_.get('data-real-value'))

#                 if data_flag is True:
#                     stock_date = datetime.fromtimestamp(int(info[0]))
#                     stock_date = date(stock_date.year, stock_date.month, stock_date.day)
                    
#                     stock_close = float(info[1].replace(',', ''))
#                     stock_open = float(info[2].replace(',', ''))
#                     stock_high = float(info[3].replace(',', ''))
#                     stock_low = float(info[4].replace(',', ''))

#                     stock_volume = 0

#                     if info[5].__contains__('K'):
#                         stock_volume = int(float(info[5].replace('K', '').replace(',', '')) * 1e3)
#                     elif info[5].__contains__('M'):
#                         stock_volume = int(float(info[5].replace('M', '').replace(',', '')) * 1e6)
#                     elif info[5].__contains__('B'):
#                         stock_volume = int(float(info[5].replace('B', '').replace(',', '')) * 1e9)

#                     result.insert(len(result),
#                                   Data(stock_date, stock_open, stock_high, stock_low,
#                                        stock_close, stock_volume, stock_currency))

#             if data_flag is True:
#                 if order in ['ascending', 'asc']:
#                     result = result[::-1]
#                 elif order in ['descending', 'desc']:
#                     result = result

#                 if as_json is True:
#                     json_ = {'name': name,
#                              'historical':
#                                  [value.stock_as_json() for value in result]
#                              }
#                     final.append(json_)
#                 elif as_json is False:
#                     df = pd.DataFrame.from_records([value.stock_to_dict() for value in result])
#                     df.set_index('Date', inplace=True)

#                     final.append(df)

#         else:
#             raise RuntimeError("ERR#0004: data retrieval error while scraping.")

#     if as_json is True:
#         return json.dumps(final[0], sort_keys=False)
#     elif as_json is False:
#         return pd.concat(final)


def search_commodities(by, value):
    """
    """

    available_search_fields = ['name', 'full_name', 'title']

    if not by:
        raise ValueError('ERR#0006: the introduced field to search is mandatory and should be a str.')

    if not isinstance(by, str):
        raise ValueError('ERR#0006: the introduced field to search is mandatory and should be a str.')

    if isinstance(by, str) and by not in available_search_fields:
        raise ValueError('ERR#0026: the introduced field to search can either just be '
                         + ' or '.join(available_search_fields))

    if not value:
        raise ValueError('ERR#0017: the introduced value to search is mandatory and should be a str.')

    if not isinstance(value, str):
        raise ValueError('ERR#0017: the introduced value to search is mandatory and should be a str.')

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'commodities', 'commodities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        commodities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0075: commodities file not found or errored.")

    if commodities is None:
        raise IOError("ERR#0076: commodities not found or unable to retrieve.")

    commodities['matches'] = commodities[by].str.contains(value, case=False)

    search_result = commodities.loc[commodities['matches'] == True].copy()

    if len(search_result) == 0:
        raise RuntimeError('ERR#0043: no results were found for the introduced ' + str(by) + '.')

    search_result.drop(columns=['tag', 'id', 'matches'], inplace=True)
    search_result.reset_index(drop=True, inplace=True)

    return search_result
