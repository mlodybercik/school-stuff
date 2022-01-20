import asyncio
import psutil
import datetime
import json
from hbmqtt.client import MQTTClient

def get_stats():
    obj = {}
    obj["timestamp"] = datetime.datetime.now().isoformat()
    obj["cpu_usage"] = psutil.cpu_percent()
    obj["ram_usage"] = psutil.virtual_memory()
    return bytes(json.dumps(obj), "utf-8")

@asyncio.coroutine
def publish():
    while True:
        CONN = MQTTClient()
        yield from CONN.connect("mqtt://test.mosquitto.org:1883/")
        data = get_stats()
        yield from asyncio.gather(CONN.publish("/pwr/computer/cpu", data))
        yield from CONN.disconnect()
        yield from asyncio.sleep(5)

loop = asyncio.get_event_loop()
task = loop.create_task(publish())

try:
    loop.run_until_complete(task)
except asyncio.CancelledError:
    pass