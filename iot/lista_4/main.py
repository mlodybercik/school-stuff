import yaml
import asyncio
import aiofiles
import sys
from typing import Tuple
from lib import create_app, manager
from lib.getter import Getter, GettableDiskData, GettableWebData
from lib.manager import Loop
from lib.sender import Sender, SenderMQTT, SenderHTTP

async def create_from_config(path: str) -> Tuple[str, Loop]:
    async with aiofiles.open(path, "r") as file:
        config = yaml.load(await file.read(), yaml.Loader)
    
    mqtt_url = f"{config['mqtt']['schema']}://" + \
               f"{config['mqtt']['url']}:" + \
               f"{config['mqtt']['port']}/"

    http_url = f"{config['http']['schema']}://" + \
               f"{config['http']['url']}:" + \
               f"{config['http']['port']}"
    
    sink: Sender
    source: Getter
    assert len(config["source"]) == 1
    key = list(config["source"].keys())[0]
    settings = config["source"][key]
    if settings["type"] == "HTTP":
        url = settings["url"]
        _path = settings["path"]
        if "json" in settings:
            json = settings["json"]
        else:
            json = False
        source = GettableWebData(url=url, path=_path, json=json)
    elif settings["type"] == "file":
        source = GettableDiskData(settings["path"])
    else:
        raise Exception(f"What? {settings['type']}")


    if settings["send"] == "HTTP":
        sink = SenderHTTP(address=http_url, topic=config["http"]["path"])
    elif settings["send"] == "MQTT":
        sink = SenderMQTT(address=mqtt_url, topic=config["mqtt"]["path"])
    else:
        raise Exception(f"What? {settings['send']}")

    return key, Loop(key, source, sink, int(settings["interval"]))


async def main():
    name, loop = await create_from_config(sys.argv[1])
    manager.set_name(name)
    manager.register_loop(loop)

    app = create_app()
    await manager.run()
    await app.run_task("10.0.0.220", 9998, debug=True, use_reloader=False)

if __name__ == "__main__":
    asyncio.run(main())
