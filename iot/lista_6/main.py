import asyncio
from lib import create_app, Aggregator, aggregators
from lib.aggregators import ASum
from lib.aggregators.aggregator_logic import AMean

default = Aggregator("default", ASum, 60) # type: ignore
random = Aggregator("random", AMean, 60) # type: ignore
aggregators["default"] = default
aggregators["random"] = random

async def main():
    app = create_app()
    await app.run_task("10.0.0.220", 9998, use_reloader=False)

asyncio.run(main())