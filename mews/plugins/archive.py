# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked
from pyrogram.types import CallbackQuery

from mews.utils.database import get_all_words, register_post

posts = []


@Client.on_callback_query(
    filters.regex("^archive_post (?P<answer>no|yes) (?P<index>\d+)")
)
async def archive_post(client: Client, callback: CallbackQuery):
    user = callback.from_user

    answer = callback.matches[0]["answer"]
    index = int(callback.matches[0]["index"])

    post = posts[index]

    if answer == "yes":
        await callback.edit_message_text(
            "A notícia "
            f"<a href='{post['telegraph_url']}'>{post['title']}</a>"
            f" foi arquivada por {user.mention}!",
            disable_web_page_preview=True,
        )
    else:
        chats = [client.news_channel]

        for row in await get_all_words():
            user_id = row[1]
            word = row[2]

            if word in (post["title"].lower() or post["content"].lower()):
                if user_id not in chats:
                    chats.append(user_id)

        for chat_id in chats:
            try:
                await client.send_message(
                    chat_id,
                    f"<a href='{post['telegraph_url']}>'"
                    f"{post['title']} [{post['source']}]</a>",
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except UserIsBlocked:
                pass

        await callback.edit_message_text(
            "A notícia "
            f"<a href='{post['telegraph_url']}'>{post['title']}</a>"
            f" foi postada por {user.mention}!",
            disable_web_page_preview=True,
        )

    await register_post(
        post["source"].lower(),
        post["title"],
        post["author"],
        post["published_date"],
        post["content"],
        post["post_link"],
        post["comments_link"],
        post["telegraph_url"],
        answer == "yes",
    )
