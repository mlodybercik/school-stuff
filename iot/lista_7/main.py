import yaml
import asyncio
import aiofiles
import sys
from typing import Tuple
from lib import create_app, manager
from lib.network.getter import Getter, GettableWebData
from lib.manager import Loop
from lib.logic.filter import Filter
from lib.network.sender import Sender, SenderHTTP

async def create_from_config(path: str) -> Tuple[str, Loop]:
    async with aiofiles.open(path, "r") as file:
        config = yaml.load(await file.read(), yaml.Loader)

    http_url = f"{config['http']['schema']}://" + \
               f"{config['http']['url']}:" + \
               f"{config['http']['port']}"
    
    sink: Sender
    source: Getter
    assert len(config["source"]) == 1
    key = list(config["source"].keys())[0]
    settings = config["source"][key]

    url = settings["url"]
    source = GettableWebData(url=url)
    sink = SenderHTTP(address=http_url, topic=config["http"]["path"])

    filter = settings["filter"]
    f = Filter(filter["path"], filter["soft"])

    return key, Loop(key, source, sink, int(settings["interval"]), f)


async def main():
    name, loop = await create_from_config(sys.argv[1])
    manager.set_name(name)
    manager.register_loop(loop)

    app = create_app()
    await manager.run()
    await app.run_task("10.0.0.220", 9999, debug=True, use_reloader=False)

if __name__ == "__main__":
    asyncio.run(main())
