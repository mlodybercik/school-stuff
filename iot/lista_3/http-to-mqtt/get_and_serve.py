from pathlib import Path
from typing import List
from aiohttp import ClientSession as Session
from libs.async_loop import AsyncLoop
from libs.post_data import MQTTPoster, HTTPPoster
from libs.get_data import GettableWebData, GettableDiskData
import yaml
import asyncio
import traceback

session: Session = None
mqtt: MQTTPoster = None
http: HTTPPoster = None

async def create_loops() -> List[AsyncLoop]:
    global session
    global mqtt
    global http
    session = Session()
    ret = []
    with open("config.yaml") as file:
        data = yaml.load(file, Loader=yaml.Loader)
    
    mqtt_client = await MQTTPoster.create_mqtt_from_dict(**data["mqtt"])
    mqtt = MQTTPoster()
    http = HTTPPoster()
    await mqtt.setup(mqtt_client, data["mqtt"]["path"])
    await http.setup(session, **data["http"])


    for key, value in data["sources"].items():
        if   value["type"] == "HTTP":
            source = GettableWebData(**value, name=key, session=session)
        elif value["type"] == "file":
            source = GettableDiskData(path=Path(value["path"]), name=key)

        if   value["send"] == "MQTT":
            ret.append(AsyncLoop(source, mqtt, value["interval"]))
        elif value["send"] == "HTTP":
            ret.append(AsyncLoop(source, http, value["interval"]))
        
    return ret

async def main():
    tasks = [asyncio.create_task(task.loop()) for task in await create_loops()]
    try:
        await asyncio.gather(*tasks, return_exceptions=False)

    except Exception as e:
        print("".join(traceback.format_exception(type(e), e, e.__traceback__)))

    finally:
        for item in tasks:
            item.cancel()


async def close():
    global session
    global mqtt
    global http
    await asyncio.gather(session.close(),
                         mqtt.teardown(),
                         http.teardown())



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass

    except Exception as e:
        print("".join(traceback.format_exception(type(e), e, e.__traceback__)))
    
    finally:
        loop.run_until_complete(close())
