from pydantic import BaseModel, Field, validator
from bson import ObjectId, json_util
from typing import Any
from enum import Enum
from datetime import datetime


class DataTypes(Enum):
    STRING = str
    INT = int
    FLOAT = float
    BOOLEAN = bool
    DATE = datetime.now
    OBJECTID = ObjectId
    ARRAY = list
    OBJECT = dict
    NULL = None


class SchemaField(BaseModel):
    name: str
    type: Any = Field(alias='type', default=None)
    default: Any = Field(alias='default', default=None)

    @validator('type')
    def validate_type(cls, v):
        return type(v)


class Schema(BaseModel):
    name: str
    fields: list[SchemaField] = Field(alias='fields', default=[])
