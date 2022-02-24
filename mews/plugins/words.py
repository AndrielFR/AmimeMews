# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

import random

from pyrogram import Client, filters
from pyrogram.types import Message

from mews.utils.database import delete_word, get_words_by_user_id, register_word


@Client.on_message(filters.command("add") & filters.private)
async def _add(client: Client, message: Message):
    user = message.from_user

    word = " ".join(message.command[1:]).lower()
    if len(word) == 0:
        await message.reply_text(
            "Nenhuma palavra/nome foi dado, tente algo como"
            " <code>/add One Piece</code>."
        )
        return

    if word in (await get_words_by_user_id(user.id)):
        await message.reply_text(
            "Essa palavra/nome já está na sua lista de filtros,"
            " verifique a lista com /words."
        )
        return

    await register_word(user.id, word)
    await message.reply_text(
        "Palavra/nome adicionada com succeso à sua lista de"
        " filtros, verique a lista com /words"
    )


@Client.on_message(filters.command("del") & filters.private)
async def _del(client: Client, message: Message):
    user = message.from_user

    word = " ".join(message.command[1:]).lower()
    if len(word) == 0:
        await message.reply_text(
            "Nenhuma palavra/nome foi dado, tente algo como"
            " <code>/del Naruto</code>."
        )
        return

    if word not in (await get_words_by_user_id(user.id)):
        await message.reply_text(
            "Essa palavra/nome não está na sua lista de filtros,"
            " verifique a lista com /words."
        )
        return

    await delete_word(user.id, word)
    await message.reply_text(
        "Palavra/nome removida com succeso da sua lista de"
        " filtros, verique a lista com /words"
    )


@Client.on_message(filters.command("words") & filters.private)
async def _words(client: Client, message: Message):
    user = message.from_user

    words = [word.capitalize() for word in await get_words_by_user_id(user.id)]
    if len(words) == 0:
        await message.reply_text(
            "Nenhuma palavra/nome foi encontrada, tente algo"
            " como <code>/add Dragon Ball</code>."
        )
        return

    text = "<b>Abaixo está sua lista de filtros</b>:"
    for word in words:
        text += f"\n– <code>{word}</code>"
    text += "\n\n<i>Remova quaisquer das palavras/nomes acima"
    text += " com <code>/del &lt;nome&gt;</code></i>."
    text += "\n<b>Exemplo</b>:"
    text += f" <code>/del {random.choice(words)}</code>"

    await message.reply_text(text)
