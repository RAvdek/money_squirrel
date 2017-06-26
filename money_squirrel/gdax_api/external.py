import datetime as dt
from time import sleep
import requests
import gdax
from bin import utils
from models import Quote

LOGGER = utils.get_logger(__name__)


class QuoteDownloader(gdax.PublicClient):

    RECORD_LIMIT = 200
    RATE_LIMIT_SLEEP = 1  # limit 3 requests/sec, so being conservative
    DATA_KEYS = [
        "timestamp",  # storing everything but this
        "low",
        "high",
        "open",
        "close",
        "volume"
    ]

    def __init__(self):
        gdax.PublicClient.__init__(self)
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
                "GDAX response failed validation:\n%s",
                response
            )
            raise e

    def _download_and_clean(self, payload):
        new_data = self.get_product_historic_rates(
            **payload
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
            datum['dt'] = dt.datetime.fromtimestamp(datum['timestamp'])
            datum.update({
                'product_id': payload["product_id"],
                'granularity': payload["granularity"],
            })
            del datum['timestamp']
        return new_data

    @staticmethod
    def _store(records):

        for datum in records:
            price_record, created = Quote.objects.get_or_create(**datum)
            if created:
                LOGGER.info("Storing GDAX Historical price %s",
                            price_record)
                price_record.save()
            else:
                LOGGER.info("Record already exists: %s",
                            price_record)

    def run(
            self,
            start_dt,
            end_dt,
            granularity=20,
            product_list=('BTC-USD', 'LTC-USD', 'ETH-USD'),
            max_failures=10
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
        failure_count = 0
        while current_dt < end_dt:
            try:
                for product_id in product_list:
                    sleep(self.RATE_LIMIT_SLEEP)
                    request_payload = {
                        "product_id": product_id,
                        "start": current_dt.strftime(utils.ISO),
                        "end": next_dt.strftime(utils.ISO),
                        "granularity": granularity,
                    }
                    LOGGER.info(
                        "Loading from GDAX:  %s",
                        request_payload
                    )
                    new_data = self._download_and_clean(request_payload)
                    self._store(new_data)
                current_dt = next_dt
                next_dt = min(
                    current_dt + dt.timedelta(
                        seconds=granularity * self.RECORD_LIMIT
                    ),
                    end_dt
                )
            except requests.exceptions.ConnectionError:
                failure_count += 1
                LOGGER.warn(
                    "HTTP Connection failure. Failure count: {}"
                    .format(failure_count)
                )
                sleep(60)
                if failure_count >= max_failures:
                    raise RuntimeError(
                        "{} HTTP connection errors. Aborting."
                        .format(max_failures)
                    )
        LOGGER.info("GDAX finished downloading")
