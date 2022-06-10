# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

import asyncio
import re
import time
from typing import Dict, List

import cloudscraper
from bs4 import BeautifulSoup

from mews.monitor.sources import BaseRSS
from mews.utils.database import exists_post


class Crunchyroll(BaseRSS):
    def __init__(self):
        self.uri = "https://crunchyroll.com/pt-br/news/"
        self.new_posts: List[Dict] = []

    async def work(self):
        cscraper = cloudscraper.create_scraper(browser="firefox")

        response = cscraper.get(self.uri)
        soup = BeautifulSoup(response.text, "html.parser")
        entries = soup.find_all("div", **{"class": "news-share-bar"})
        for entrie in entries[:10]:
            script = entrie.find_next("script")
            post_link = re.search('data-url="(.*)"', str(script)).group(1)
            comments_link = f"{post_link}#comments"
            title = re.search('data-text="(.*)"', str(script)).group(1)

            author = soup.find("span", **{"class": "byline"}).a.string.strip()

            post_date = (
                soup.find("div", **{"class": "post-date"}).contents[0].strip().split()
            )
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
                "Dezembro": 12,
            }
            month = months[post_date[0]]
            day = int(post_date[1].replace(",", ""))
            year = int(post_date[2])
            hours, minutes = post_date[3].replace("am", "").replace("pm", "").split(":")
            hours, minutes = int(hours), int(minutes)
            published_date = int(
                round(
                    time.mktime(
                        time.struct_time((year, month, day, hours, minutes, 0, 0, 0, 0))
                    )
                )
            )

            post_response = cscraper.get(post_link)
            post_soup = BeautifulSoup(post_response.text, "html.parser")

            body = post_soup.find("div", **{"class": "body"})
            contents = body.find_next("div", **{"class": "contents"}).contents
            content = "".join(str(line) for line in contents[:-4])

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
