# Manual

## Setup
* First make sure you install the requirements by running `pip install -r requirements.txt`
* inside the data folder you will find a `config.py` which will read your config file named `config.ini`
* Inside that file you will set your reddit api parameters and your iexcloud api parameters

## parameters
* `--get-data` this will retreive the latest data from IEXCloud
* `--train` will train the model using both the 'stock_data.csv' and 'stock_stats.csv'
* `--predict` will try and predict using the best models generated against the 'prediction_entries.csv' file

## Packages 

### Package & Version
-------------------------
* certifi         2020.11.8
* chardet         3.0.4
* idna            2.10
* joblib          0.17.0
* nltk            3.3
* numpy           1.19.4
* pandas          1.1.4
* pip             20.2.4
* python-dateutil 2.8.1
* pytz            2020.4
* requests        2.25.0
* scikit-learn    0.23.2
* scipy           1.5.4
* setuptools      50.3.2
* six             1.15.0
* threadpoolctl   2.1.0
* urllib3         1.26.1
* vim             0.0.1
* wheel           0.35.1