# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

from mews.monitor.sources import BaseRSS


class IntoxiAnime(BaseRSS):
    def __init__(self):
        self.uri = "https://www.intoxianime.com/"
        self.rss_uri = "https://www.intoxianime.com/feed/"
        self.new_posts: List[Dict] = []
