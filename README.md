# Design

Every application has a file `external.py` which has wrapper classes for external APIs. Each class should...
- have a `load` method which downloads data and sets a self.data attr.
- have a `store` method should dump the data to the DB using the django ORM.

# TODO

## Dev
- Will have to make custom methods for trends to handle data massaging as they hid the data.
- What other data resources should I be downloading data from? I'd like to do some sentiment analysis on news headlines or summaries.
- Create an "ETL" application for doing cleaning dumps of data. Can just do db to pandas to db.

## Analysis
- Mean interest over time is not correlating to next day trade delta. This is part due to the way I'm calculating, but also because there is no baseline of comparison for the search interest. Everything will just be "how popular compared to the most popular item".
- Should pick an easy "anchoring" search term to include when pulling from trends API

## Data thoughts

Need to make choices for initial data
- GDAX price data with 20sec granularity. Limited to 200 return values per request, so break up requests into hour chunks. Even if we don't seek to trade at that frequency, we can use the values to quantify variability over wider intervals.
- InterestOverTime with day level granularity for a years worth of data for all search terms.
- InterestOverTime data points for each day. This can be normalized using the interest over time per day. We can also aggregate as incoming data should be sparse.
- (Lower priority) InterestByRegion for each day. This can also be normalized.

# Useful help articles

## General django

- ['Improperly configured' error when running scripts](http://stackoverflow.com/questions/15556499/django-db-settings-improperly-configured-error)

## Postgres

- [postgres + django blog post](http://www.marinamele.com/taskbuster-django-tutorial/install-and-configure-posgresql-for-django)

## GDAX

- [official GDAX API docs](https://docs.gdax.com/)
- [python wrapper of the API on GitHub](https://github.com/danpaquin/GDAX-Python)

## GoogleTrends

- [Python API wrapper](https://github.com/GeneralMills/pytrends)