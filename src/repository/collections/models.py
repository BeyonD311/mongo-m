from pydantic import BaseModel, Field


class SchemaField(BaseModel):
    name: str
    type: str = Field(alias='type', default='')


class Schema(BaseModel):
    name: str
    fields: list[SchemaField] = Field(alias='fields', default=[])
