from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class DataDirectory(BaseModel):
    entry_name: str
    entry_name_chn: str
    entry_comment: str
    entry_type: str
    entry_length: int
    system_id: str
    db_id: str
    table_id: str

    class Config:
        from_attributes = True


class ListDataDirectories(BaseModel):
    start: int
    limit: int
    query: List[str]
    table_ids: Optional[List[str]] = []
    ids: Optional[List[str]] = []


class CreateSystemResource(BaseModel):
    system_name: str
    system_comment: str


class ListResources(BaseModel):
    start: int
    limit: int
    query: List[str]
    ids: Optional[List[str]] = []


class CreateDBResource(BaseModel):
    db_name: str
    db_comment: str
    system_id: str


class CreateTableResource(BaseModel):
    table_name: str
    table_comment: str
    system_id: str
    database_id: str


class ResourceType(str, Enum):
    system = "System"
    database = "Database"
    table = "Table"


class DeleteResource(BaseModel):
    resource_type: ResourceType
    resource_id: str
