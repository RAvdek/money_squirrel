# Design

Every application has a file `external.py` which has wrapper classes for external APIs. Each class should...
- have a `load` method which downloads data and sets a self.data attr.
- have a `store` method should dump the data to the DB using the django ORM.

# TODO

- Make a facade which will download all data. Should come with a command line interface for easy update.
- Download data. I'm thinking that hourly data information from a couple of years worth of data would work for a basic intro.
- Perform initial analysis. I'm thinking we should try to predict hourly close price and volume based on overall Google trend data and previous history.
- Will have to make custom methods for trends to handle data massaging as they hid the data.

# Useful help articles

## Postgres

- [postgres + django blog post](http://www.marinamele.com/taskbuster-django-tutorial/install-and-configure-posgresql-for-django)

## GDAX

- [official GDAX API docs](https://docs.gdax.com/)
- [python wrapper of the API on GitHub](https://github.com/danpaquin/GDAX-Python)

## GoogleTrends

- [Python API wrapper](https://github.com/GeneralMills/pytrends)