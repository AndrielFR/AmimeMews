# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

from typing import List, Tuple

from . import conn

async def get_all_words() -> List[Tuple]:
    cursor = await conn.execute("SELECT * FROM words")
    rows = await cursor.fetchall()
    await cursor.close()
    return rows

async def get_word(id: int) -> Tuple:
    cursor = await conn.execute("SELECT * FROM words WHERE id = ?", (id,))
    row = await cursor.fetchone()
    await cursor.close()
    return row

async def get_words(word: str) -> List[Tuple]:
    cursor = await conn.execute("SELECT * FROM words WHERE word = ?", (word,))
    rows = await cursor.fetchall()
    await cursor.close()
    return rows

async def get_words_by_user_id(user_id: int) -> List[str]:
    cursor = await conn.execute("SELECT * FROM words WHERE user_id = ?", (user_id,))
    rows = await cursor.fetchall()
    await cursor.close()
    return [row[2] for row in rows]

async def delete_word(user_id: int, word: str):
    await conn.execute("DELETE FROM words WHERE user_id = ? AND word = ?", (user_id, word))
    assert conn.total_changes > 0
    await conn.commit()

async def register_word(user_id: int, word: str):
    await conn.execute("INSERT INTO words (user_id, word) VALUES (?, ?)", (user_id, word))
    assert conn.total_changes > 0
    await conn.commit()


__all__ = ["get_all_words", "get_word", "get_words", "get_words_by_user_id", "delete_word", "register_word"]