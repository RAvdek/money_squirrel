import datetime as dt
import pandas as pd
from bin import utils


def get_price_features_60(start_dt, end_dt):

    df = utils.query_pg(
            """
            select distinct product
                , dt
                , close
                , volume
            from gdax_gdaxprice
            where granularity = 60
                and dt <= cast('{end_dt}' as timestamp)
                and dt >= cast('{start_dt}' as timestamp)
            """.format(
                start_dt=str(start_dt),
                end_dt=str(end_dt)
            )
    )
    close_df = df.pivot(
        columns='product',
        index='dt',
        values='close'
    ).sort_index()
    volume_df = df.pivot(
        columns='product',
        index='dt',
        values='volume'
    ).sort_index()
    output = close_df.merge(
        volume_df,
        how="outer",
        left_index=True,
        right_index=True,
        suffixes=('_close', '_volume')
    )
    return utils.fill_dt_gaps(
        output,
        start_dt,
        end_dt,
        window_seconds=60
    )
