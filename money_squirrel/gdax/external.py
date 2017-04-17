import datetime as dt
import GDAX
from bin import utils
from models import GDAXPrice

LOGGER = utils.get_logger(__name__)


class HistoricPriceInterface(GDAX.PublicClient):

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
        self.data = None

    def _validate_data(self):
        try:
            assert type(self.data) is list
            for record in self.data:
                assert type(record) is list
                assert len(record) == len(self.DATA_KEYS)
        except AssertionError as e:
            LOGGER.critical(
                "GDAX data failed validation:\n%s",
                self.data
            )
            raise e

    def load(
            self,
            product,
            start_dt,
            end_dt,
            granularity
    ):
        """ Download historical prices """
        self.request_payload = {
            "product": product,
            "start": start_dt.strftime(utils.ISO),
            "end": end_dt.strftime(utils.ISO),
            "granularity": granularity,
        }
        LOGGER.info(
            "Loading from GDAX:  %s",
            self.request_payload
        )
        self.data = self.getProductHistoricRates(
            **self.request_payload
        )
        LOGGER.info("Validating response")
        self._validate_data()

    def store(self):

        for datum in self.data:
            gp = GDAXPrice()
            gp.dt = dt.datetime.fromtimestamp(int(datum[0]))
            gp.granularity = self.request_payload["granularity"]
            gp.product = self.request_payload["product"]
            for i in range(1, len(self.DATA_KEYS)):
                setattr(
                    gp,
                    self.DATA_KEYS[i],
                    datum[i]
                )
            LOGGER.info("Storing GDAX Historical price %s", gp)
            gp.save()
