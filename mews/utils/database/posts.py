# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

from typing import List, Tuple

from . import conn


async def exists_post(source: str, title: str, published_date: int, content: str, post_link: str, comments_link: str) -> Tuple:
    cursor = await conn.execute("SELECT * FROM posts WHERE source = ? AND (title = ? OR published_date = ? OR content = ? OR post_link = ? OR comments_link = ?)", (source, title, published_date, content, post_link, comments_link))
    rows = await cursor.fetchall()
    await cursor.close()
    return bool(rows)

async def register_post(source: str, title: str, author: str, published_date: int, content: str, post_link: str, comments_link: str, telegraph_link: str):
    await conn.execute("INSERT INTO posts (source, title, author, published_date, content, post_link, comments_link, telegraph_link) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (source, title, author, published_date, content, post_link, comments_link, telegraph_link))
    assert conn.total_changes > 0
    await conn.commit()


__all__ = ["exists_post", "register_post"]