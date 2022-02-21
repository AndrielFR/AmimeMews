# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    user = message.from_user
    
    text = f"""
Olá {user.mention}!

Eu sou o <s>postador de notícias</s> do @AmimeMews, legal né?

Você sabia que você pode <b>filtrar</b> notícias? O processo para isso é muito simples, basta fazer uso dos comandos abaixo.

<code>•</code> /add &lt;nome&gt;    <code>—</code> adiciona uma palavra/nome à lista de filtros.
                                    Exemplo: <code>/add Jujutsu Kaisen</code>, com esse
                                    comando, você adiciona <code>Jujutsu Kaisen</code> à
                                    lista de filtros e receberá no privado toda
                                    postagem relacionada.
                                        
<code>•</code> /del &lt;nome&gt;     <code>—</code> remove uma palavra/nome da lista de filtros.
                                    Exemplo: <code>/del Jujutsu Kaisen</code>, com
                                    esse comando, você remove <code>Jujutsu Kaisen</code>
                                    da lista de filtros e não receberá mais no privado
                                    quaisquer postagem relacionada.
                                        
<code>•</code> /words               <code>—</code> veja sua lista de filtros.

No momento, é apenas isso, mas <s>eu estou ansioso</s> pelas atualizações que <s>receberei</s> em breve. 😵
    """
    await message.reply_text(text)