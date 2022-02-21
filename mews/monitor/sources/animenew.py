# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

import asyncio
import time

import feedparser

from bs4 import BeautifulSoup
from typing import Dict, List, Union

from mews.utils import http
from mews.utils.database import exists_post
from mews.monitor.sources import BaseRSS


class AnimeNew(BaseRSS):
    def __init__(self):
        self.uri = "https://www.animenew.com.br/"
        self.rss_uri = "https://animenew.com.br/feed/"
        self.new_posts: List[Dict] = []
    
    async def work(self):
        response = await http.get(self.rss_uri)
        p = feedparser.parse(response.content)
        for entrie in p.entries[:10]:
            title = entrie.title
            author = entrie.author
            published_date = int(time.mktime(entrie.published_parsed))
            post_link = entrie.link
            comments_link = entrie.comments
            
            response = await http.get(post_link)
            soup = BeautifulSoup(response.content, "html.parser")
            container = soup.find("div", **{"class": "elementor-widget-theme-post-content"})
            contents = container.find_next("div").contents
            content = "".join(str(line) for line in contents[1:-2])
            
            if not (await exists_post(self.__class__.__name__.lower(), title, published_date, content, post_link, comments_link)):
                self.new_posts.append(dict(
                    title=title,
                    author=author,
                    published_date=published_date,
                    content=content,
                    post_link=post_link,
                    comments_link=comments_link
                ))
        
        await asyncio.sleep(600)
        await self.work()