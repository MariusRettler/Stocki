"""
Fetch the stock prices from Quandl for stocks in S & P 500.
@author: Marius Rettler
"""
import click
import os
import pandas as pd
import random
import time

from urllib.request import urlopen
from urllib.error import HTTPError
from datetime import datetime

from config import DEFAULT_CONFIG

RANDOM_SLEEP_TIMES = (1, 5)

# This repo "github.com/datasets/s-and-p-500-companies" has additional other information about
# S & P 500 companies.

SP500_LIST_PATH = os.path.join(DEFAULT_CONFIG.data_dir, "constituents-financials.csv")

def download_sp500_list():

    if not os.path.exists(os.path.dirname(SP500_LIST_PATH)):
        try:
            os.makedirs(os.path.dirname(SP500_LIST_PATH))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    response = urlopen(DEFAULT_CONFIG.sp500_list_url)
    print("Downloading ...", DEFAULT_CONFIG.sp500_list_url)
    with open(SP500_LIST_PATH, 'w') as csvfile:
        content = response.read()
        encoding = response.headers.get_content_charset('utf-8')
        text = content.decode(encoding)
        print(text, file=csvfile)
    return


def load_symbols():
    download_sp500_list()
    df_sp500 = pd.read_csv(SP500_LIST_PATH)
    df_sp500.sort_values('Market Cap', ascending=False, inplace=True)
    print(df_sp500)
    stock_symbols = df_sp500['Symbol'].unique().tolist()
    print("Loaded %d stock symbols" % len(stock_symbols))
    return stock_symbols


def fetch_prices(symbol, outname, startdate=datetime(1980, 1, 1), enddate=None):
    """
    Fetch daily stock prices for stock `symbol`.

    Args:
        symbol (str): a stock abbr. symbol, like "GOOG" or "AAPL".
        startdate (date): the date where the downloaded stock data should start.

    Returns: a bool, whether the fetch is succeeded.
    """

    if not DEFAULT_CONFIG.quandl_api_key:
        raise Exception("Quandl api key is not set!")

    # Format dates to match quandl api.
    if not startdate:
        startdateformated = time.strftime("%Y-%m-%d")
    else:
        startdateformated = startdate.strftime("%Y-%m-%d")

    if not enddate:
        enddateformated = time.strftime("%Y-%m-%d")
    else:
        enddateformated = enddate.strftime("%Y-%m-%d")

    stock_url = "https://www.quandl.com/api/v3/datasets/WIKI/" + symbol + \
        ".csv?start_date=" + startdateformated + "&end_date=" + enddateformated + \
        "&order=asc&column_index=4&rows=10000&collapse=daily&transformation=rdiff&api_key=" + \
        DEFAULT_CONFIG.quandl_api_key


    print("Fetching {} ...".format(symbol))
    print(stock_url)

    try:
        response = urlopen(stock_url)
        with open(outname, 'w') as csvfile:
            content = response.read()
            encoding = response.headers.get_content_charset('utf-8')
            text = content.decode(encoding)
            print(text, file=csvfile)
    except HTTPError:
        print("Failed when fetching {}".format(symbol))
        return False

    data = pd.read_csv(outname)
    if data.empty:
        print("Remove {} because the data set is empty.".format(outname))
        os.remove(outname)
    else:
        dates = data.iloc[:, 0].tolist()
        print("# Fetched rows: %d [%s to %s]" %
              (data.shape[0], dates[-1], dates[0]))

    # Take a rest
    sleep_time = random.randint(*RANDOM_SLEEP_TIMES)
    print("Sleeping ... %ds" % sleep_time)
    time.sleep(sleep_time)
    return True


@click.command(help="Fetch stock prices data")
@click.option('--continued', is_flag=True)
def main(continued):
    random.seed(time.time())
    num_failure = 0

    symbols = load_symbols()
    for idx, sym in enumerate(symbols):
        out_name = os.path.join(DEFAULT_CONFIG.data_dir, sym + ".csv")
        if continued and os.path.exists(out_name):
            print("Fetched", sym)
            continue

        succeeded = fetch_prices(sym, out_name)
        num_failure += int(not succeeded)

        if idx % 10 == 0:
            print("# Failures so far [%d/%d]: %d" %
                  (idx + 1, len(symbols), num_failure))


if __name__ == "__main__":
    main()
