import asyncio
import os
from kucoin.asyncio import KucoinSocketManager
from typing import Optional

from cement.core.log import LogInterface
from kucoin.client import Client

from jtrader.core.provider import Provider


class KuCoin(Provider):
    def __init__(
            self,
            is_sandbox: bool,
            logger: LogInterface,
            no_notifications: Optional[bool] = False
    ):
        super().__init__(is_sandbox, logger, no_notifications)

        self.client_prop = Client(
            os.environ.get('KUCOIN_API_TOKEN'),
            os.environ.get('KUCOIN_API_SECRET'),
            os.environ.get('KUCOIN_API_PASSPHRASE'),
            is_sandbox
        )

    async def register_websockets(
            self,
            loop: asyncio.AbstractEventLoop,
            ticker: str,
            on_websocket_message: callable
    ) -> None:
        ksm = await KucoinSocketManager.create(loop, self.client, on_websocket_message)

        await ksm.subscribe(f"/market/candles:{ticker}_1min")

        while True:
            await asyncio.sleep(20, loop=loop)

    def chart(self, stock: str, timeframe: str) -> dict:
        return super().chart(stock, timeframe)

    def symbols(self) -> dict:
        return super().symbols()

    def intraday(self, stock: str) -> dict:
        return super().intraday(stock)
