from collections.abc import Awaitable, Callable
from typing import Any, Annotated

from pydantic import PlainValidator, PlainSerializer, WithJsonSchema
from sqlalchemy_utils import Ltree

AsyncFunc = Callable[..., Awaitable[Any]]

LtreeField = Annotated[
    Ltree,
    PlainValidator(lambda v: Ltree(v)),
    PlainSerializer(lambda v: v.path),
    WithJsonSchema({'type': 'string', 'examples': ['some.path']}),
]
