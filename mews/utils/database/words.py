# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

from typing import List, Tuple

from mews import database


conn = database.get_conn()

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

async def delete_word(id: int, user_id: int):
    await conn.execute("DELETE FROM words WHERE id = ? AND user_id = ?", (id, user_id))
    assert conn.total_changes > 0
    await conn.commit()


__all__ = ["get_word", "get_words", "delete_word"]