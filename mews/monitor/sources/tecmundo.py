# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

import asyncio
import re
import time

from bs4 import BeautifulSoup

from mews.utils import http
from mews.utils.database import exists_post
from mews.monitor.sources import BaseRSS


class TecMundo(BaseRSS):
    def __init__(self):
        self.uri = "https://www.tecmundo.com.br/"
        self.posts_uri = "https://www.tecmundo.com.br/minha-serie/tag/anime"
        self.new_posts: List[Dict] = []
    
    async def work(self):
        response = await http.get(self.posts_uri)
        soup = BeautifulSoup(response.content, "html.parser")
        entries = soup.find_all("div", **{"class": "tec--card__info"})
        for entrie in entries[:10]:
            published_date = entrie.find("div", **{"class": "tec--timestamp__item"})
            published_date = [int(number) for number in published_date.string.split("/")]
            published_date = int(time.mktime(time.struct_time((published_date[2], published_date[1], published_date[0], 0, 0, 0, 0, 0, 0))))
            
            title = entrie.find("a", **{"class": "tec--card__title__link"})
            post_link = title["href"]
            title = title.string.strip()
            
            post_response = await http.get(post_link)
            post_soup = BeautifulSoup(post_response.content, "html.parser")
            
            author = post_soup.find("div", **{"class": "tec--timestamp__item z--font-bold"})
            author = author.a.string.strip()
            
            article = post_soup.find("div", **{"class": "tec--article__body"})
            contents = article.contents
            content = "".join(str(line) for line in contents)

            if not (await exists_post(self.__class__.__name__.lower(), title, published_date, content, post_link, "")):
                self.new_posts.append(dict(
                    source=self.__class__.__name__,
                    title=title,
                    author=author,
                    published_date=published_date,
                    content=content,
                    post_link=post_link,
                    comments_link=""
                ))
        
        await asyncio.sleep(600)
        await self.work()