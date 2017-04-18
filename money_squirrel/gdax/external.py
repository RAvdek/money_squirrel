import datetime as dt
from time import sleep
import GDAX
from bin import utils
from models import GDAXPrice

LOGGER = utils.get_logger(__name__)


class GDAXPriceDownloader(GDAX.PublicClient):

    RECORD_LIMIT = 200
    RATE_LIMIT_SLEEP = 1  # limit 3/sec, so being conservative
    DATA_KEYS = [
        "timestamp",  # storing everything but this
        "low",
        "high",
        "open",
        "close",
        "volume"
    ]

    def __init__(self):
        GDAX.PublicClient.__init__(self)
        self.request_payload = dict()
        self.data = []
        self.start_dt = None
        self.end_dt = None
        self.granularity = None

    def _validate_response(self, response):
        try:
            assert type(response) is list
            for record in response:
                assert type(record) is list
                assert len(record) is len(self.DATA_KEYS)
        except AssertionError as e:
            LOGGER.critical(
                "GDAX data failed validation:\n%s",
                self.data
            )
            raise e

    def load(
            self,
            start_dt,
            end_dt,
            granularity=20,
            product_list=('BTC-USD', 'LTC-USD', 'ETH-USD')
    ):
        """ Download historical prices """
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.granularity = granularity
        current_dt = start_dt
        next_dt = min(
            current_dt + dt.timedelta(
                seconds=granularity * self.RECORD_LIMIT
            ),
            end_dt
        )
        while current_dt < end_dt:
            for product in product_list:
                sleep(self.RATE_LIMIT_SLEEP)
                request_payload = {
                    "product": product,
                    "start": current_dt.strftime(utils.ISO),
                    "end": next_dt.strftime(utils.ISO),
                    "granularity": granularity,
                }
                LOGGER.info(
                    "Loading from GDAX:  %s",
                    request_payload
                )
                new_data = self.getProductHistoricRates(
                    **self.request_payload
                )
                LOGGER.info("Validating response")
                self._validate_response(new_data)
                new_data = [
                    {
                        self.DATA_KEYS[i]: datum[i]
                        for i in range(len(self.DATA_KEYS))
                    }
                    for datum in new_data
                ]
                for datum in new_data:
                    dt_timestamp = dt.datetime.fromtimestamp(
                        int(datum.pop('timestamp'))
                    )
                    datum.update({
                        'product': product,
                        'granularity': granularity,
                        'dt': dt_timestamp
                    })
                self.data += new_data
            current_dt = next_dt
            next_dt = min(
                current_dt + dt.timedelta(
                    seconds=granularity * self.RECORD_LIMIT
                ),
                end_dt
            )
        LOGGER.info("GDAX finished downloading")

    def store(self):

        for datum in self.data:
            price_record, created = GDAXPrice.objects.get_or_create(**datum)
            if created:
                LOGGER.info("Storing GDAX Historical price %s",
                            price_record)
                price_record.save()
            else:
                LOGGER.info("Record already exists: %s",
                            price_record)

