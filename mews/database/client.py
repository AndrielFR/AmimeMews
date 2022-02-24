# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

import logging

import aiosqlite

logger = logging.getLogger(__name__)
conn: aiosqlite.Connection = None
path: str = "mews/database/sqlite.db3"


async def connect():
    global conn

    logger.info("Connecting database...")
    conn = await aiosqlite.connect(path)

    await conn.execute(
        """
    CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            word VARCHAR(512) NOT NULL
    )
    """
    )

    await conn.execute(
        """
    CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            source VARCHAR(64) NOT NULL,
            title VARCHAR(512) NOT NULL,
            author VARCHAR(256) NOT NULL,
            published_date INTEGER NOT NULL,
            content TEXT NOT NULL,
            post_link TEXT NOT NULL,
            comments_link TEXT NOT NULL,
            telegraph_link TEXT NOT NULL,
            is_archived INTEGER NOT NULL DEFAULT 0
    )
    """
    )

    await conn.execute("PRAGMA journal_mode=WAL;")
    logger.info("Database connected")


async def close():
    global conn

    await conn.close()
    conn = None


def get_conn():
    global conn

    return conn


def is_connected():
    return get_conn() is not None


__all__ = ["connect", "close", "get_conn", "is_connected"]
