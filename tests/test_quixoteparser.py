# -*- coding: utf-8 -*-
import pytest
from webargs.testing import CommonTestCase

from tests.app import app


class TestQuixoteParser(CommonTestCase):
    def create_app(self):
        return app

    @pytest.mark.skip("Not implemented")
    def test_parsing_headers(self, testapp):
        res = testapp.get("/echo_headers", headers={"name": "Fred"})
        assert res.json == {"HTTP_NAME": "Fred"}

    def test_use_args_with_path_param(self, testapp):
        url = "/echo_use_args_with_path_param"
        res = testapp.get(url + "?value=42")
        assert res.json == {"value": 42}

    def test_use_kwargs_with_path_param(self, testapp):
        url = "/echo_use_kwargs_with_path_param"
        res = testapp.get(url + "?value=42")
        assert res.json == {"value": 42}
