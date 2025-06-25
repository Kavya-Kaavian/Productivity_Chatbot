

from services.helloWorldServices import hello_world_services


async def hello_world():
    return await hello_world_services()