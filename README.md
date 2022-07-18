# webargs-quixote

[webargs](https://webargs.readthedocs.io/en/latest/index.html) support for Quixote web framework.

## Install
```shell
pip install webargs-quixote
# or
poetry add webargs-quixote
```

## Usage

```python
from webargs import fields
from webargs_quixote import parser, use_args


@use_args({"value": fields.Int()})
def home(req, args):
    return args
```

Looks [webargs](https://webargs.readthedocs.io/en/latest/index.html) docs for more details.
