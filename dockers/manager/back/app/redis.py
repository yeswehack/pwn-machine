import aioredis

client = aioredis.from_url("redis://localhost", decode_responses=True)
