# Data thoughts

Need to make choices for initial data

- GDAX price data with 20sec granularity. Limited to 200 return values per request, so break up requests into hour chunks. Even if we don't seek to trade at that frequency, we can use the values to quantify variability over wider intervals.
- InterestOverTime with hour level granularity for a years worth of data for all search terms. This is what is returned when setting a 7 day time frame. Google fudges volumes, but we can correct this by normalizing data by volume of most recent period of search traffic. This means using now as a point of reference rather than previous times. From this we can still infer trends.
- (Lower priority) InterestByRegion for each day. This can also be normalized.

Our model should be:
```
FP = FuturePrice = F(previous pricing data, market sentiment, environmental factors) + N(0, sigma)
S = sigma = sigma(ppd, ms, ev)
```
This would be different than usual trading where assets would have a more well defined intrinsic value which would contribute to the equations. Our goal would be to model both `FP` and `S` and then develop trading strategies like "buy when 95% confident future price is higher" or "buy a lot when we're confident prices will raise in the future, sell a lot when we're confident prices will drop". A well calibrated model will have `FP` in the predicted z% interval z% of the time.

Possible features:
- MS: How is search volume for various phrases compared to previous times? What if we drill down on particular geos (US, UK, Bolivia, Nigeria)? Taken at hourly intervals over a 7 day period this gives ~170 features per search term. This can be significantly compressed using moving averages or other aggregate stats.
- EV: Add random effects for time of day, and day of week. There should be interaction between these and search frequency.
- PPD: Suppose we use K previous periods to predict FP and each period contains W windows. Then we can generate K**W training samples by randomly sampling prices within each period. This provides a distribution of price prediction from which we can estimate FP and S. We should incorporate both price and volume into any models.

Possible feature engineering techniques:
- moving averages
- cluster data and map data as distance to clusters. This would provide an artificial way of creating "technical analysis indicators" and reducing size of the feature space. See latent source bitcoin article.
- dynamic time warping? can randomly remove data points from time series to make lengths mismatch and do DTW. This could be a better way to randomize input data.

Model criteria:
- Should be well calibrated as described above.
- Should not simply produce most recent price as estimate.
- Should be able to consider interactions between features.
- Must be able to train and evaluate in memory in a reasonable amount of time.
- Model performance should not vary with market conditions. IOW perform well during an uptrend and poorly during a downtrend.
- Losing money is more bad than gaining money is good, so should be able to build custom loss function. Taxation should also be accounted for when estimating gains.
- Simplicity and interpretability is desirable for model iteration. For example a notion of feature importance would be desirable as we can see if the different features are even contributing to the model.
