# -*- coding: utf-8 -*-
from webargs_quixote import use_args
from marshmallow import Schema, fields
from quixote.qwip import QWIP
from quixote.publish import Publisher

app = QWIP(Publisher("example"))

_q_exports = ["query"]


# Add some schema
class QuerySchema(Schema):
    start = fields.Int(default=0)
    count = fields.Int(default=10)
    title = fields.Str()
    kinds = fields.List(fields.Str())


# Router
@use_args(QuerySchema(), location="query")
def query(request, args):
    return args

# Install gunicorn and run:
# > gunicorn example:app

# Then open this url:
# http://127.0.0.1:8000/query?start=10&count=20&kinds=a&kinds=b
