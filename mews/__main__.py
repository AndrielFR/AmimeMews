# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

import asyncio
import logging
import os

from pyrogram import Client, idle

from mews import database


logging.basicConfig(
    level=logging.INFO,
    format="%(name)s.%(funcName)s | %(levelname)s | %(message)s",
    datefmt="[%X]",
)
logging.getLogger("pyrogram.syncer").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

async def main():
    await database.connect()
    
    client = Client(
        "mews",
        config_file="config.ini",
        parse_mode="html",
        workers=14,
        workdir=".",
        plugins=dict(root="mews.plugins"),
        sleep_threshold=180,
    )
    await client.start()
    client.me = await client.get_me()
    
    from mews import monitor
    await monitor.start(client)
    
    await idle()


if __name__ == "__main__":
    os.system("cls||clear")
    
    event_policy = asyncio.get_event_loop_policy()
    event_loop = event_policy.new_event_loop()
    asyncio.set_event_loop(event_loop)
    
    try:
        event_loop.run_until_complete(main())
    finally:
        if database.is_connected():
            event_loop.run_until_complete(database.close())
        
        from mews import monitor
        event_loop.run_until_complete(monitor.stop())
        
        from mews.utils import close_http
        event_loop.run_until_complete(close_http())