import asyncio
import aiofiles
import yaml
from pathlib import Path
from lib import create_app, Service

async def load_services(path: Path):
    ret = []
    async with aiofiles.open(path, "r") as file:
        config = yaml.load(await file.read(), yaml.Loader)
    
    try:
        for key, value in config["services"].items():
            ret.append(Service(key, value["address"]))
    except AttributeError:
        pass

    return ret

async def main():
    services = await load_services("config.yaml")
    
    await create_app(services).run_task("10.0.0.220", 8888, debug=True, use_reloader=False)

if __name__ == "__main__":
    asyncio.run(main())
