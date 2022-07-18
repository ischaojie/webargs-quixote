# -*- coding: utf-8 -*-
from io import BytesIO

from webargs.core import Parser, is_json, missing, parse_json
from quixote.http_request import HTTPRequest
from quixote.upload import Upload


def is_json_request(req):
    return is_json(req.content_type)


class QuixoteParser(Parser):
    def get_request_from_view_args(self, view, args, kwargs):
        if isinstance(args[0], HTTPRequest):
            return args[0]
        return args[1]

    def _raw_load_json(self, req):
        if not is_json_request(req):
            return missing
        length = max(0, int(req.environ.get("CONTENT_LENGTH", '0')))
        raw_json = req.stdin.read(length)
        return parse_json(raw_json)

    def load_querystring(self, req, schema):
        return self._makeproxy(req.form, schema)

    def load_form(self, req, schema):
        return self._makeproxy(req.form, schema)

    def load_headers(self, req, schema):
        req_headers = {k: v for k, v in req.environ.items() if k.startswith("HTTP_")}
        print(req_headers)
        return self._makeproxy(req_headers, schema)

    def load_cookies(self, req, schema):
        return req.cookies

    def load_files(self, req, schema):
        req_files = {}
        for k, v in req.form.items():
            if isinstance(v, Upload):
                req_files[k] = BytesIO(open(v.tmp_filename, "rb").read())

        print(req_files)
        return self._makeproxy(req_files, schema)


parser = QuixoteParser()
use_args = parser.use_args
use_kwargs = parser.use_kwargs
