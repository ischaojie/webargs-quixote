# -*- coding: utf-8 -*-
from quixote.config import Config
from quixote.publish import Publisher
from quixote.qwip import QWIP

config = Config()
config.upload_dir = "."

app = QWIP(Publisher("tests.app.views", config=config))
