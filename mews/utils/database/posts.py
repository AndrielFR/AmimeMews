# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

from typing import Optional, List, Tuple

from . import conn


async def exists_post(source: str, title: str, published_date: int, content: str, post_link: str, comments_link: str) -> Tuple:
    cursor = await conn.execute("SELECT * FROM posts WHERE source = ? AND (title = ? OR published_date = ? OR content = ? OR post_link = ? OR comments_link = ?)", (source, title, published_date, content, post_link, comments_link))
    rows = await cursor.fetchall()
    await cursor.close()
    return bool(rows)

async def get_similar_posts(title: str) -> Optional[List[Tuple]]:
    cursor = await conn.execute(f"SELECT * FROM posts WHERE LOWER(title) LIKE ?", (title.replace(" ", "%").lower(),))
    rows = await cursor.fetchall()
    await cursor.close()
    return rows

async def register_post(source: str, title: str, author: str, published_date: int, content: str, post_link: str, comments_link: str, telegraph_link: str, is_archived: bool = False):
    await conn.execute("INSERT INTO posts (source, title, author, published_date, content, post_link, comments_link, telegraph_link, is_archived) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (source, title, author, published_date, content, post_link, comments_link, telegraph_link, int(is_archived)))
    assert conn.total_changes > 0
    await conn.commit()


__all__ = ["exists_post", "get_similar_posts", "register_post"]