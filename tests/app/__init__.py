# -*- coding: utf-8 -*-
from quixote.qwip import QWIP
from quixote.publish import Publisher
from quixote.config import Config

config = Config()
config.upload_dir = "."

app = QWIP(Publisher("tests.app.views", config=config))
