import asyncio

from src.client import NetworkCli
import logging
import websockets

async def main():
    #SERVER_IP = "167.172.152.60"
    SERVER_IP = "ws://localhost"
    SERVER_PORT = 5555
    logging.getLogger().setLevel(logging.INFO)
    cli = NetworkCli(SERVER_IP, SERVER_PORT)
    await cli.main()


# Using the special variable
# __name__
if __name__ == "__main__":
    asyncio.run(main())