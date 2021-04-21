import aiohttp
import asyncio

ROOT = "http://127.0.0.1:8080/api"


async def get_from_api(path):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{ROOT}{path}") as response:
            return await response.json()


async def wait_from_api(path):
    max_try = 10

    while max_try := max_try - 1:
        try:
            return await get_from_api(path)
        except:
            await asyncio.sleep(0.1 * (10 - max_try))


async def wait_delete_from_api(path):
    max_try = 10

    try:
        while max_try := max_try - 1:
            await get_from_api(path)
            await asyncio.sleep(0.1 * (10 - max_try))
        return False
    except Exception as e:
        print(e)
        return True
