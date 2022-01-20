import asyncio
import datetime
import json
from hbmqtt.client import MQTTClient, QOS_0, ClientException
from requests_futures.sessions import Session

session = Session()

async def send_to_server(barray: bytearray):
    text = barray.decode("utf-8")
    try:
        w = session.post("http://localhost:9999/cpu", text)
    except ConnectionRefusedError:
        pass


@asyncio.coroutine
def send_to_http():
    CONN = MQTTClient()
    yield from CONN.connect("mqtt://test.mosquitto.org:1883/")
    yield from CONN.subscribe([("/pwr/computer/cpu", QOS_0)])

    while True:
        try:
            message = yield from CONN.deliver_message()
            packet = message.publish_packet
            yield from send_to_server(packet.payload.data)
            yield from asyncio.sleep(0)
        except KeyboardInterrupt:
            break
        except ClientException as e:
            print(e)
            continue

    yield from CONN.unsubscribe(["/pwr/computer/cpu"])
    yield CONN.disconnect()

asyncio.get_event_loop().run_until_complete(send_to_http())