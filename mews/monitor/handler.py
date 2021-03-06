# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

import asyncio
import logging
import re
from typing import List

from bs4 import BeautifulSoup
from httpx import ConnectTimeout
from pyrogram import Client
from pyrogram.errors import FloodWait, UserIsBlocked
from pyromod.helpers import ikb
from telegraph.aio import Telegraph
from telegraph.exceptions import NotAllowedTag, TelegraphException
from telegraph.utils import ALLOWED_TAGS

from mews.monitor.sources import (
    Anime21,
    AnimeNew,
    AnimeUnited,
    BlogBBM,
    Crunchyroll,
    IntoxiAnime,
    OtakuPTAnime,
    OtakuPTManga,
    TecMundo,
)
from mews.utils.database import get_all_words, get_similar_posts, register_post

logger = logging.getLogger(__name__)
sources = [
    AnimeUnited,
    AnimeNew,
    IntoxiAnime,
    TecMundo,
    OtakuPTAnime,
    OtakuPTManga,
    Anime21,
    BlogBBM,
    Crunchyroll,
]
future = None
event_loop = asyncio.get_event_loop()
telegraph = Telegraph()


async def start(client: Client):
    global future

    logger.info("Starting monitor...")
    logger.info("Sources availabes: %s", [source.__name__ for source in sources])

    future = asyncio.ensure_future(worker([source() for source in sources], client))

    logger.info("Monitor started")


async def stop():
    global future

    logger.info("Stopping monitor...")

    future.cancel()

    logger.info("Monitor stopped")


async def worker(sources: List[object], client: Client):
    for source in sources:
        event_loop.create_task(source.work())
        logger.info("Source %s is working", source.__class__.__name__)
        await asyncio.sleep(4)

    def get_new_posts():
        nonlocal sources

        new_posts = []

        for source in sources:
            new_posts.extend(source.get_new_posts())

        return new_posts

    def clear_new_posts():
        nonlocal sources

        for source in sources:
            source.clear_new_posts()

    while True:
        new_posts = get_new_posts()
        logger.info("%s new post(s) found", len(new_posts))

        for index, post in enumerate(new_posts):
            title = post["title"]
            author = post["author"]
            content = post["content"]

            for full_tag in re.findall("<[^>]+>", content):
                tag = re.sub("[/<>]", "", full_tag).split()[0]
                if tag not in ALLOWED_TAGS:
                    content = re.sub(full_tag, "", content)

            soup = BeautifulSoup(content, "html.parser")
            images = []
            for img in soup.find_all("img"):
                if img.has_attr("src"):
                    if img["src"] in images:
                        img.decompose()
                    else:
                        images.append(img["src"])

            content = str(soup)

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
                except (NotAllowedTag, TelegraphException):
                    break
                else:
                    url = response["url"]

                    similar_posts = []
                    title_splited = re.findall(r"\w+", title)
                    index = 0
                    while index < len(title_splited) - 2:
                        similar_posts = await get_similar_posts(
                            " ".join(title_splited[index : index + 3])
                        )
                        if similar_posts:
                            from mews.plugins.archive import posts

                            index = len(posts)
                            post["telegraph_url"] = url

                            repeated = False
                            for p in posts:
                                if (
                                    p["post_link"] == post["post_link"]
                                    or p["title"] == post["title"]
                                ):
                                    repeated = True
                                    break

                            if repeated:
                                break

                            posts.append(post)

                            text = "Err! Temos um problema, fui fazer a postagem de uma nova not??cia e percebi que j?? postei algo parecido, n??o sei dizer, voc?? pode olhar pra mim?\n"
                            text += f"\n<b>T??tulo</b>: {title}"
                            text += f"\n<b>Autor</b>: {author}"
                            text += f"\n<b>URL</b>: {url}"
                            text += "\n\n<b>Postagens similares que eu encontrei</b>:"

                            for similar_post in similar_posts:
                                text += f"\n<b>T??tulo</b>: {similar_post[2]}"
                                text += f"\n<b>Autor</b>: {similar_post[3]}"
                                text += f"\n<b>URL</b>: {similar_post[8]}"
                                text += "\n"

                            await client.send_message(
                                client.post_revision,
                                text,
                                reply_markup=ikb(
                                    [
                                        [
                                            ("??? Poste", f"archive_post no {index}"),
                                            ("??????? Arquive", f"archive_post yes {index}"),
                                        ]
                                    ]
                                ),
                                disable_web_page_preview=True,
                            )

                            break
                        index += 1

                    if similar_posts:
                        break
                    else:
                        chats = [client.news_channel]

                        for row in await get_all_words():
                            user_id = row[1]
                            word = row[2]

                            if word in title.lower() or word in content.lower():
                                if user_id not in chats:
                                    chats.append(user_id)

                        for chat_id in chats:
                            try:
                                await client.send_message(
                                    chat_id,
                                    f"<a href='{url}'>{title} [{post['source']}]</a>",
                                )
                            except FloodWait as e:
                                await asyncio.sleep(e.x)
                            except UserIsBlocked:
                                pass

                    await register_post(
                        post["source"].lower(),
                        title,
                        author,
                        post["published_date"],
                        content,
                        post["post_link"],
                        post["comments_link"],
                        url,
                    )

                    break

            if (index + 1) == len(new_posts):
                clear_new_posts()

            await asyncio.sleep(4.0)

        await asyncio.sleep(1800)
