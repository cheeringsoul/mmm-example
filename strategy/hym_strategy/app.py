import asyncio
import logging
import uuid
from decimal import Decimal

from mmm.core.events.event import TradesEvent
from mmm.core.position import StrategyPosition
from mmm.core.strategy.analyzer import Analyzer
from mmm.core.strategy.core.base import Strategy
from mmm.core.strategy.core.decorators import sub_event
from mmm.core.strategy.signals import StrategySignal
from mmm.core.strategy.status import PositionStatus
from mmm.credential import Credential
from mmm.project_types import Asset, Exchange

logger = logging.getLogger(__name__)


class PriceAnalyzer(Analyzer):

    def analysis(self) -> "StrategySignal":
        # todo

        return StrategySignal.BUY


class RiskAnalyzer(Analyzer):

    def analysis(self) -> "StrategySignal":
        return StrategySignal.SELL


class HymStrategy(Strategy):

    def __init__(self, bot_id: str, credential: "Credential"):
        super(HymStrategy, self).__init__(bot_id, credential)
        self.analyzer = PriceAnalyzer()
        self.status = PositionStatus.SHORT
        # strategy initial position
        init_assets = [Asset(inst_id='USDT', amount=Decimal("100"))]
        self.position: "StrategyPosition" = StrategyPosition(init_assets)

    @sub_event(TradesEvent)
    async def on_trades(self, trades: "TradesEvent"):
        print(trades)
        return

        if self.status == PositionStatus.SHORT:
            signal = self.analyzer.analysis()
            if signal == StrategySignal.BUY:
                uniq_id = str(uuid.uuid1())
                currency = self.position.get_asset('USDT')
                self.create_order(uniq_id, Exchange.OKEX, params={})
                try:
                    rv = await self.order_manager.query_order_async(uniq_id, timeout=10)
                except asyncio.TimeoutError:
                    logger.error(f'订单{uniq_id}创建失败')
                    self.position.add(Asset(inst_id='USDT', amount=currency))
                else:
                    self.status = PositionStatus.OPENED
                    # todo
                    self.position.add()
        elif self.status == PositionStatus.OPENED:
            ...
