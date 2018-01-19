"""
General configuration class
@author Marius Rettler
"""
class Config():
    data_dir = "data"
    log_dir = "logs"
    model_dir = "models"
    plots_dir="images"
    quandl_api_key = ""
    sp500_list_url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents-financials.csv"

DEFAULT_CONFIG = Config()
