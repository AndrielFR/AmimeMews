# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

import asyncio
import logging
import os

import pytomlpp
from pyrogram import Client, idle
from pyrogram.enums import ParseMode

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

    config_toml = pytomlpp.loads(open("config.toml", "r").read())

    api_id = config_toml["pyrogram"]["api_id"]
    api_hash = config_toml["pyrogram"]["api_hash"]
    bot_token = config_toml["pyrogram"]["bot_token"]

    client = Client(
        "mews",
        api_id=api_id,
        api_hash=api_hash,
        bot_token=bot_token,
        parse_mode=ParseMode.HTML,
        workers=14,
        workdir=".",
        plugins=dict(root="mews.plugins"),
        sleep_threshold=240,
    )
    await client.start()
    client.me = await client.get_me()

    client.news_channel = config_toml["mews"]["news_channel"]
    client.post_revision = config_toml["mews"]["post_revision"]

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
    except KeyboardInterrupt:
        pass
    finally:
        if database.is_connected():
            event_loop.run_until_complete(database.close())

        from mews import monitor

        event_loop.run_until_complete(monitor.stop())

        from mews.utils import close_http

        event_loop.run_until_complete(close_http())
