# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

import asyncio
import time

import feedparser

from typing import Dict, List, Union

from mews.utils import http
from mews.utils.database import exists_post


class BaseRSS(object):
    def __init__(self):
        self.uri = """
        self.rss_uri = """
        self.new_posts: List[Dict] = []
    
    async def work(self):
        response = await http.get(self.rss_uri)
        p = feedparser.parse(response.content)
        for entrie in p.entries[:10]:
            title = entrie.title
            author = entrie.author
            published_date = int(time.mktime(entrie.published_parsed))
            content = entrie.content[0]["value"]
            post_link = entrie.link
            comments_link = entrie.comments
            
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

    def get_new_posts(self) -> List[Union[Dict, None]]:
        return self.new_posts
    
    def clear_new_posts(self):
        self.new_posts.clear()