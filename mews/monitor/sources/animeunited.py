# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

from mews.monitor.sources import BaseRSS


class AnimeUnited(BaseRSS):
    def __init__(self):
        self.uri = "https://www.animeunited.com.br/"
        self.rss_uri = "https://www.animeunited.com.br/feed/"
        self.new_posts: List[Dict] = []