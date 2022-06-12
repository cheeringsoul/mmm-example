import asyncio
import json
import logging

from mmm.core.datasource import OkexWsDatasource
from mmm.core.order.executor import OrderExecutor
from mmm.core.strategy.core.base import StrategyRunner
from mmm.credential import Credential
from strategy.hym_strategy.app import HymStrategy


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    topic1 = json.dumps({
        "op": "subscribe",
        "args": [
            {
                "channel": "trades",
                "instId": "BTC-USDT-SWAP"
            },
            {
                "channel": "trades",
                "instId": "ETH-USDT-SWAP"
            },
            {
                "channel": "candle1m",
                "instId": "BTC-USDT-SWAP"
            }
        ]
    })
    OkexWsDatasource().subscribe(topic1)
    credential = Credential('', '', '')
    StrategyRunner(HymStrategy('hym.001', credential)).create_tasks()
    OrderExecutor().create_task()
    asyncio.get_event_loop().run_forever()
