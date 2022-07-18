# -*- coding: utf-8 -*-
import json
from functools import wraps

import marshmallow as ma
from marshmallow.exceptions import ValidationError
from webargs import fields

from webargs_quixote import parser, use_args, use_kwargs

hello_args = {
    "name": fields.Str(load_default="World", validate=lambda n: len(n) >= 3)
}
hello_multiple = {"name": fields.List(fields.Str())}


class HelloSchema(ma.Schema):
    name = fields.Str(load_default="World", validate=lambda n: len(n) >= 3)


hello_many_schema = HelloSchema(many=True)

# variant which ignores unknown fields
hello_exclude_schema = HelloSchema(unknown=ma.EXCLUDE)


def jsonize(func):
    @wraps(func)
    def _(*a, **kw):
        rsp = a[0].response
        rsp.set_content_type("application/json")
        try:
            r = func(*a, **kw)
            return json.dumps(r)
        except ValidationError as err:
            rsp.set_status(422)
            return json.dumps({"error": err.messages})
        except json.JSONDecodeError:
            rsp.set_status(400)
            return json.dumps({"json": ["Invalid JSON body."]})

    return _


@jsonize
def echo(request):
    return parser.parse(hello_args, request, location="query")


@jsonize
def echo_form(request):
    return parser.parse(hello_args, request, location="form")


@jsonize
def echo_json(request):
    return parser.parse(hello_args, request, location="json")


@jsonize
def echo_json_or_form(request):
    return parser.parse(hello_args, request, location="json_or_form")


@use_args(hello_args, location="query")
@jsonize
def echo_use_args(request, args):
    return args


@jsonize
@use_args(
    {"value": fields.Int()},
    validate=lambda args: args["value"] > 42,
    location="form",
)
def echo_use_args_validated(request, args):
    return args


@jsonize
def echo_ignoring_extra_data(request):
    return parser.parse(hello_exclude_schema, request, unknown=None)


@use_kwargs(hello_args, location="query")
@jsonize
def echo_use_kwargs(request, name):
    return {"name": name}


@jsonize
def echo_multi(request):
    return parser.parse(hello_multiple, request, location="query")


@jsonize
def echo_multi_form(request):
    return parser.parse(hello_multiple, request, location="form")


@jsonize
def echo_multi_json(request):
    return parser.parse(hello_multiple, request)


@jsonize
def echo_many_schema(request):
    return parser.parse(hello_many_schema, request)


@jsonize
@use_args({"value": fields.Int()}, location="query")
def echo_use_args_with_path_param(request, args):
    return args


@jsonize
@use_kwargs({"value": fields.Int()}, location="query")
def echo_use_kwargs_with_path_param(request, value):
    return {"value": value}


@jsonize
def always_error(request):
    def always_fail(value):
        raise ma.ValidationError("something went wrong")

    argmap = {"text": fields.Str(validate=always_fail)}
    return parser.parse(argmap, request)


@jsonize
def echo_headers(request):
    return parser.parse(hello_args, request, location="headers")


@jsonize
def echo_cookie(request):
    return parser.parse(hello_args, request, location="cookies")


@jsonize
def echo_file(request):
    args = {"myfile": fields.Field()}
    result = parser.parse(args, request, location="files")
    myfile = result["myfile"]
    content = myfile.read().decode("utf8")
    return {"myfile": content}


@jsonize
def echo_nested(request):
    argmap = {
        "name": fields.Nested({"first": fields.Str(), "last": fields.Str()})
    }
    return parser.parse(argmap, request)


@jsonize
def echo_nested_many(request):
    argmap = {
        "users": fields.Nested(
            {"id": fields.Int(), "name": fields.Str()}, many=True
        )
    }
    return parser.parse(argmap, request)


@jsonize
def error(request):
    raise ValidationError("something went wrong")


_q_exports = [
    "echo",
    "echo_form",
    "echo_json",
    "echo_json_or_form",
    "echo_use_args",
    "echo_use_args_validated",
    "echo_ignoring_extra_data",
    "echo_use_kwargs",
    "echo_multi",
    "echo_multi_form",
    "echo_multi_json",
    "echo_many_schema",
    "echo_use_args_with_path_param",
    "echo_use_kwargs_with_path_param",
    "echo_ignoring_extra_data",
    "always_error",
    "echo_headers",
    "echo_cookie",
    "echo_file",
    "echo_nested",
    "echo_nested_many",
    "error",
]
