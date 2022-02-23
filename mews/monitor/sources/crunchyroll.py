# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

import asyncio
import re
import time

from bs4 import BeautifulSoup

from mews.utils import http
from mews.utils.database import exists_post
from mews.monitor.sources import BaseRSS


class Crunchyroll(BaseRSS):
    def __init__(self):
        self.uri = "https://crunchyroll.com/pt-br/news/"
        self.new_posts: List[Dict] = []
    
    async def work(self):
        response = await http.get(self.uri)
        soup = BeautifulSoup(response.content, "html.parser")
        entries = soup.find_all("div", **{"class": "news-share-bar"})
        for entrie in entries[:10]:
            script = entrie.find_next("script")
            post_link = re.search("data-url=\"(.*)\"", str(script)).group(1)
            comments_link = f"{post_link}#comments"
            title = re.search("data-text=\"(.*)\"", str(script)).group(1)
            
            author = soup.find("span", **{"class": "byline"}).a.string.strip()
            
            published_date = soup.find("div", **{"class": "post-date"}).contents[0].strip().split()
            months = {
                "Janeiro": 1,
                "Fevereiro": 2,
                "Maio": 3,
                "Abril": 4,
                "Março": 5,
                "Junho": 6,
                "Julho": 7,
                "Agosto": 8,
                "Setembro": 9,
                "Outubro": 10,
                "Novembro": 11,
                "Dezembro": 12
            }
            month = months[published_date[0]]
            day = int(published_date[1].replace(",", ""))
            year = int(published_date[2])
            hours, minutes = published_date[3].replace("am", "").replace("pm", "").split(":")
            hours, minutes = int(hours), int(minutes)
            published_date = int(round(time.mktime(time.struct_time((year, month, day, hours, minutes, 0, 0, 0, 0)))))
            
            post_response = await http.get(post_link)
            post_soup = BeautifulSoup(post_response.content, "html.parser")
            
            contents = post_soup.find("div", **{"class": "contents"}).contents
            content = "".join(str(line) for line in contents[:-4])
            
            if not (await exists_post(self.__class__.__name__.lower(), title, content, post_link)):
                self.new_posts.append(dict(
                    source=self.__class__.__name__,
                    title=title,
                    author=author,
                    published_date=published_date,
                    content=content,
                    post_link=post_link,
                    comments_link=comments_link
                ))
        
        await asyncio.sleep(600)
        await self.work()