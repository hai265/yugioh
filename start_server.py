import asyncio
import logging

from src.server import YugiohServer


# Using the special variable
# __name__
if __name__ == "__main__":
    server = YugiohServer("0.0.0.0", 5555)
    logging.getLogger().setLevel(logging.INFO)
    asyncio.run(server.main())