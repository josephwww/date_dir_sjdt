from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.data_directory import DataDirectory, DBResource

from database import get_db

router = APIRouter(prefix="/data_directory")


@router.get("")
def list_data_directories(entry_id: str, db: Session=Depends(get_db),):
    print("hh")
    tree = db.query(DBResource).filter()
    entry = db.query(DataDirectory).filter(DataDirectory.id == entry_id).first()

    return entry
