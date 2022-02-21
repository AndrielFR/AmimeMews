# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

import logging

import httpx


logger = logging.getLogger(__name__)

http = httpx.AsyncClient(
    http2=True,
    transport=httpx.AsyncHTTPTransport(retries=3),
    follow_redirects=True,
)

async def close_http():
    await http.aclose()
    logger.debug("HTTP closed")