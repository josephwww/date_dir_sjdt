from uuid import uuid4

from sqlalchemy.orm import Session

from models import data_directory as model
from schemas import data_directory as schema

def list_data_directory(db: Session, filter=None):
    return db.query(model.DataDirectory).all()

def create_data_directory(db: Session, data_dir: schema.DataDirectory):
    db_data_dir = model.DataDirectory(id=uuid4(), system_id=data_dir.system_id, db_id=data_dir.db_id)
