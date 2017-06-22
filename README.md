# Money Squirrel

![](https://s-media-cache-ak0.pinimg.com/originals/e3/77/d5/e377d5d4c6e6dfeb0f775275277cbfbd.jpg)

- MS could also be "market sentiment"
- Squirrels also know when to save their nuts for later

## What is it???

Try algotrading on GDAX (supplemented with Google Trends data)!

- Phase 1: Create APIs for GDAX and Trends to dump data to a DB
- Phase 2: Build models on the data so you can predict price in the future
- Phase 3: Use the price predictions to develop a purchasing strategy
- Phase 4: Productionize model evaluation and purchasing with API integrations
- Phase 5: Sleep on a pile of money

## Installing and running the application

Start off in the root of the repo. 
I've only done this on one computer and am guessing it will be a pain setting up on a new one :)

- Get Postgres installed if you haven't already: `brew install postgres`.
- Configuring the DB may take a moment. I made this db name `ms`: Please consult [this blog post](http://www.marinamele.com/taskbuster-django-tutorial/install-and-configure-posgresql-for-django)
- You'll also want to checkout `config/postgres.json`
- Go to the root directory and run `pip install -e .` to get all the requirements (which you might not already have!).
- Start the database on you machine (in a separate terminal tab): `postgres -D /usr/local/var/postgres`
- `python manage.py migrate` will create an empty database
- `cd money_squirrel` to get into the guts of the code.
- To start a Jupyter notebook with access to the database, run `python manage.py shell_plus --notebook`.
- To be able to download your own Google trends data, you'll need to fill out `config/keys.json`. BE CAREFUL NOT TO PUT YOUR PASSWORD ON GITHUB!!! This should be solvable with gitignore (though maybe not the smartest way to do this). It should look like:
```
{
  "gmail": "my_address@gmail.com",
  "gpass": "my_password"
}

```

## Design

### Why Django?

- The ORM serves as a simple interface between JSON (eg. API payloads) and SQL DB (where we will store historical data).
- The built in `manage.py` commands make schema modification easy.
- The admin app which is built in makes modification of data by hand easy.

### Why Postgres?

- Postgres supports JSON data types, which is friendly for housing data pulled from APIs.
- You can also do CTEs which MySQL (the versions I know at least) and sqlite3 cannot.
- If I ever wanted to get fancy and run this on not-my-machine, it's scalable.

### Subfolders

- `gdax` and `trends` are django apps. A django app is just a DB interface.
- Every application has a file `external.py` which has wrapper classes for external APIs. Each class should have a run method.
- `etl` should store data-prep functions: When you download the raw data there will be lots of missing values and, for trends, some wonky formatting. 
- `ad_hod` is for Jupyter notebooks. For prototyping data cleaning and modeling.
- `money_squirrel` is all of the django-y things.
- `config` obv. has configs. 
  - `coins.json` is used to get coin prices from 


## Useful articles

### General django

- [Django tutorial (good reference for basics)](https://docs.djangoproject.com/en/1.11/intro/tutorial01/)
- [Django shell_plus (for making notebooks)](https://opensourcehacker.com/2014/08/13/turbocharge-your-python-prompt-and-django-shell-with-ipython-notebook/)
- ['Improperly configured' error when running scripts](http://stackoverflow.com/questions/15556499/django-db-settings-improperly-configured-error)

### Postgres

- [postgres + django blog post](http://www.marinamele.com/taskbuster-django-tutorial/install-and-configure-posgresql-for-django)

### External API

- [official GDAX API docs](https://docs.gdax.com/)
- [python wrapper of the GDAX API on GitHub](https://github.com/danpaquin/GDAX-Python)
- [Trends python API wrapper](https://github.com/GeneralMills/pytrends)

### Crypto + investing articles

- [CG taxation for virtual currency](https://www.forbes.com/sites/laurashin/2015/12/16/bitcoin-at-tax-time-what-you-need-to-know-about-trading-tipping-mining-and-more/#2492cf3d6bde)
- [Capital gains and losses overview](http://www.kiplinger.com/article/investing/T056-C000-S001-understanding-capital-gains-and-losses.html)

### Research papers on crypto pricing

I'm not a huge fan of any of these: Good for generating ideas, but backtesting evaluation methods are all super opaque.

- [Latent source model for price prediction](https://arxiv.org/pdf/1410.1231v1.pdf)
- [Uses sentiment analysis to predict bitcoin price swings](https://arxiv.org/abs/1506.01513)
- [Caltech paper with similar content](http://courses.cms.caltech.edu/cs145/2014/bitbot.pdf)
- [ARIMA models for price prediction](http://proceedings.mlr.press/v55/amjad16.pdf)
- [Correlating web query volume against NASDAQ prices](https://arxiv.org/abs/1110.4784)