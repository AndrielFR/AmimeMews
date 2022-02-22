# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

from mews.monitor.sources import BaseRSS


class Anime21(BaseRSS):
    def __init__(self):
        self.uri = "https://anime21.blog.br/"
        self.rss_uri = "https://feeds.feedburner.com/_anime21?format=xml"
        self.new_posts: List[Dict] = []