# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

import asyncio
import logging
import re
import time

from pyrogram import Client
from pyrogram.errors import FloodWait
from telegraph.aio import Telegraph
from telegraph.utils import ALLOWED_TAGS
from telegraph.exceptions import NotAllowedTag
from httpx import ConnectTimeout

from mews.monitor.sources import AnimeUnited, AnimeNew, IntoxiAnime, TecMundo, OtakuPTAnime, OtakuPTManga, Anime21
from mews.utils.database import get_all_words, register_post


logger = logging.getLogger(__name__)
sources = [AnimeUnited, AnimeNew, IntoxiAnime, TecMundo, OtakuPTAnime, OtakuPTManga, Anime21]
futures = []
event_loop = asyncio.get_event_loop()
telegraph = Telegraph()

async def start(client: Client):
    logger.info("Starting monitor...")
    logger.info("Sources availabes: %s", [source.__name__ for source in sources])
    
    for source in sources:
        future = asyncio.ensure_future(worker(source(), client))
        futures.append(future)
        await asyncio.sleep(10)
    
    logger.info("Monitor started")

async def stop():
    logger.info("Stopping monitor...")
    
    for future in futures:
        future.cancel()
    
    futures.clear()
    logger.info("Monitor stopped")

async def worker(source: object, client: Client):
    event_loop.create_task(source.work())
    logger.debug("Source %s is working", source.__class__.__name__)
    
    await asyncio.sleep(2.5)
    
    while True:
        new_posts = source.get_new_posts()
        logger.debug("%s has %s new post(s)", source.__class__.__name__, len(new_posts))
        
        for index, post in enumerate(new_posts):
            title = post["title"]
            author = post["author"]
            content = post["content"]
            
            for full_tag in re.findall("<[^>]+>", content):
                tag = re.sub("[/<>]", "", full_tag).split()[0]
                if tag not in ALLOWED_TAGS:
                    content = re.sub(full_tag, "", content)
            
            while True:
                response = None

                try:
                    await telegraph.create_account(short_name="AmimeMews")
                    response = await telegraph.create_page(
                        title,
                        html_content=content,
                        author_name=author,
                    )
                except ConnectTimeout:
                    continue
                except NotAllowedTag: break
                else:
                    url = response["url"]
                    
                    chats = [client.news_channel]
                    
                    for row in (await get_all_words()):
                        user_id = row[1]
                        word = row[2]
                        
                        if word in title.lower() or word in content.lower():
                            if user_id not in chats:
                                chats.append(user_id)
                    
                    for chat_id in chats:
                        try:
                            await client.send_message(chat_id, f"<a href='{url}'>{title} [{source.__class__.__name__}]</a>")
                        except FloodWait as e:
                            await asyncio.sleep(e.x)
                        else: pass
                    
                    await register_post(source.__class__.__name__.lower(), title, author, post["published_date"], content, post["post_link"], post["comments_link"], url)
                    
                    break
            
            if (index + 1) == len(new_posts):
                source.clear_new_posts()
        
        await asyncio.sleep(300)