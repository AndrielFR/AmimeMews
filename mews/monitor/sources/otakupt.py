# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

import asyncio
import time
from typing import Dict, List

import feedparser
from bs4 import BeautifulSoup

from mews.monitor.sources import BaseRSS
from mews.utils import http
from mews.utils.database import exists_post


class OtakuPTAnime(BaseRSS):
    def __init__(self):
        self.uri = "https://www.otakupt.com/category/anime/"
        self.rss_uri = "https://www.otakupt.com/category/anime/feed/"
        self.new_posts: List[Dict] = []

    async def work(self):
        response = await http.get(self.rss_uri)
        p = feedparser.parse(response.content)
        for entrie in p.entries[:10]:
            title = entrie.title
            author = entrie.author
            published_date = int(round(time.mktime(entrie.published_parsed)))
            post_link = entrie.link
            comments_link = entrie.comments

            post_response = await http.get(post_link)
            post_soup = BeautifulSoup(post_response.content, "html.parser")

            post_content = post_soup.find("div", **{"class": "td-post-content"})
            contents = post_content.contents
            content = "".join(str(line) for line in contents[4:-7])

            if not (
                await exists_post(
                    self.__class__.__name__.lower(), title, content, post_link
                )
            ):
                self.new_posts.append(
                    dict(
                        source=self.__class__.__name__,
                        title=title,
                        author=author,
                        published_date=published_date,
                        content=content,
                        post_link=post_link,
                        comments_link=comments_link,
                    )
                )

        await asyncio.sleep(600)
        await self.work()


class OtakuPTManga(OtakuPTAnime):
    def __init__(self):
        self.uri = "https://www.otakupt.com/category/manga/"
        self.rss_uri = "https://www.otakupt.com/category/manga/feed/"
        self.new_posts: List[Dict] = []
