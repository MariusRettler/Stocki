# Stocki

Stocki is an stock prediction AI based on phyton3 and tensorflow.
Stocki provides: 
- normalized plotted graphs
- automated data fetching from quandl
- parameterized start

## Getting Started

Before you can start, you have to get an api-key from quandl [here](https://www.quandl.com/).
Copy the key in the config.py.

After that, check the config.py and modify as you prefer.
Then fetch the data with data_fetcher.py.

When did all the preparation, start run the main.py like this:
python3 main.py --stock_symbol=AAPL --train --input_size=1 --lstm_size=128 --max_epoch=50

Have a look at the main.py and pass different parameter for test purposes.

## Authors

* **Marius Rettler** - *Initial work* - [MariusRettler](https://github.com/MariusRettler)

## Acknowledgments

* Special thanks to [lilianweng](https://github.com/lilianweng)

