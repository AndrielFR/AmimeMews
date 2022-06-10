<!--
  ~ Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>
  ~ 
  ~ SPDX-License-Identifier: MIT
  -->

# AmimeMews - Telegram Bot

![License](https://img.shields.io/github/license/AndrielFR/AmimeMews)

AmimeMews é um bot simples de Telegram feito para o [AmimeMews](https://t.me/AmimeMews) (canal do Telegram) para acompanhar notícias do mundo Otaku.

Developed in Python using the MTProto library [Pyrogram](https://github.com/pyrogram/pyrogram).

## Preparing and running

Rename `config.toml.sample` to `config.toml` and fill with your data like: <br>

```toml
[pyrogram]
api_id = 1234567
api_hash = "1z02nserl588a2tek491t74839941e29"
bot_token = "1234567890:A8BCD3Ef7ghijk1LmNO9pQr5stuvwX2Yz0A"

[mews]
news_channel = -1004567890098
post_revision = -1007654321123
```

Install the requirements with: <br>

```bash
python -m pip install -Ur requirements.txt
```

And finally, starts the bot with: <br>

```bash
python -m mews
```

## License

Copyright © 2022 [AndrielFR](https://github.com/AndrielFR)

Licensed under the [Expat/MIT license](LICENSE).
This project is also [REUSE compliant](https://reuse.software/).
See individual files for more copyright information.
