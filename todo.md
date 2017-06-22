# TODO

### Dev

- Switch all indicies to timestamps
- Redownload trends data as timezone info is pain in the ass
- Will have to make custom methods for trends to handle data massaging as they hid the data. Perhaps we can compress data prior to storage.
- What other data resources should I be downloading data from? I'd like to do some sentiment analysis on news headlines or summaries.
- Create an "ETL" application for doing cleaning dumps of data. Can just do db to pandas to db.
- Create command line applications for ease of use and process automation. These should be runnable from local env using `manage.py`

### Benchmarks
 
- Have enough data downloaded to prototype a data pipeline. This could include understanding distributions of data after proposed cleaning + clustering. Developing methods for filling in NAs and performing data validation.
- Build command line applications for data ingestion and cleaning pipeline. Should provide enough flexibility to be varied at execution time.
- Prototype model(s) to run on cleaned dta with enough functionality to make training and backtesting of price prediction easy.
- Decide on 2-3 models which perform the best and productionize. Create an abstraction for execution so it is easy to produce different models. Ideally models will product different results or perform better or worse under different conditions.
- Contemplate trading strategies and backtest.
