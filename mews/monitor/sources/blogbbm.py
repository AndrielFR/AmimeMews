# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

import asyncio
import time

import feedparser

from bs4 import BeautifulSoup

from mews.utils import http
from mews.utils.database import exists_post
from mews.monitor.sources import BaseRSS


class BlogBBM(BaseRSS):
    def __init__(self):
        self.uri = "https://blogbbm.com/"
        self.rss_uri = "https://blogbbm.com/feed/"
        self.new_posts: List[Dict] = []
    
    async def work(self):
        response = await http.get(self.rss_uri)
        p = feedparser.parse(response.content)
        for entrie in p.entries[:10]:
            title = entrie.title
            author = entrie.author
            published_date = int(round(time.mktime(entrie.published_parsed)))
            post_link = entrie.link
            
            post_response = await http.get(post_link)
            post_soup = BeautifulSoup(post_response.content, "html.parser")
            
            post_content = post_soup.find("article", **{"class": "vn-article-content"})
            contents = post_content.find_next("div", **{"class": "entry-content"}).contents
            content = "".join(str(line) for line in contents[4:-21])
            
            if not (await exists_post(self.__class__.__name__.lower(), title, content, post_link)):
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