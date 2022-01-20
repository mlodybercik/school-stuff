import asyncio
import lib
from lib import create_app
from lib.aggregators.aggregator_logic.aggregator_logic import AMean
from lib.aggregators.aggregator_logic.aggregator import Aggregator
from lib.aggregators.graph_logic.graphing import PlainPlot

lib.aggregator =  Aggregator("graph", AMean, 3600, PlainPlot()) # type: ignore

async def main():
    app = create_app()
    await app.run_task("10.0.0.220", 9997, use_reloader=False)

asyncio.run(main())