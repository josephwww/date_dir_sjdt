from pydantic import BaseModel


class DataDirectory(BaseModel):
    id: str
    entry_name: str
    entry_name_chn: str
    entry_comment: str
    entry_type: str
    entry_length: int
    system_id: str
    db_id: str
    table_id: str

    class Config:
        orm_mode = True
