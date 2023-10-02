from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas import data_directory as schema
from crud import data_directory as crud
from database import SessionLocal

router = APIRouter(prefix="/data_directory")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
    finally:
        db.close()


@router.delete("/resources")
def delete_resource(resource: schema.DeleteResource, db: Session = Depends(get_db)):
    """
    delete resource table by resource id and type
    :param resource: {"resource_id": <>, "resource_type": <>}
    :param db:
    :return: {"status": <status>}
    """
    if crud.delete_resource(db, resource.resource_id, resource.resource_type):
        return {
            "status": "success"
        }
    return {
        "status": "failed"
    }


@router.get("/systems")
def list_systems(query_params: schema.ListResources, db: Session = Depends(get_db), ):
    """

    :param query_params:
    :param db:
    :return:
    """
    systems_count, systems = crud.list_resources(db, query_params.dict(), "System")
    return {
        "data": systems,
        "count": systems_count
    }


@router.post("/systems")
def create_system(system: schema.CreateSystemResource, db: Session = Depends(get_db), ):
    """
    create system in db_resource table
    :param system: resource params
    :param db:
    :return:
    """
    # check if system name exists
    list_system_params = {
        "start": 0,
        "limit": 1,
        "query": [system.system_name]
    }
    systems_count, _ = crud.list_resources(db, list_system_params, "System")
    if systems_count > 0:
        return {
            "reason": f"system_name: {system.system_name} exists",
            "status": "failed"
        }
    # non-exist, then create
    new_system = crud.create_system(db, system)
    return {
        "data": new_system,
        "status": "success"
    }


@router.get("/databases")
def list_dbs(query_params: schema.ListResources, db: Session = Depends(get_db)):
    dbs_count, dbs = crud.list_resources(db, query_params.dict(), "Database")
    return {
        "data": dbs,
        "count": dbs_count
    }


@router.post("/databases")
def create_db(database: schema.CreateDBResource, db: Session = Depends(get_db), ):
    """
    create database resource
    :param database:
    :param db:
    :return:
    :exception:
    1. system_id not exist
    2. db_name exist under this system id
    """
    # check system_id exists
    systems = crud.get_resource(db, database.system_id, "System")
    if not systems:
        return {
            "status": "failed",
            "reason": f"system_id: {database.system_id} not exist"
        }

    # check if db_name exist under this system id
    list_database_params = {
        "start": 0,
        "limit": 1,
        "query": database.db_name,
        "system_id": database.system_id
    }
    dbs_count, same_databases = crud.list_resources(db, list_database_params, "Database")
    if dbs_count > 0:
        return {  # 抛异常
            "reason": f"database name: {database.db_name} exists under system_id: {database.system_id}",
            "status": "failed"
        }
    # non-exist, then create
    new_database = crud.create_database(db, database)
    return {
        "data": new_database,
        "status": "success"
    }


@router.get("/tables")
def list_tables(query_params: schema.ListResources, db: Session = Depends(get_db), ):
    tables_count, tables = crud.list_resources(db, query_params.dict(), "Table")
    return {
        "data": tables,
        "count": tables_count
    }


@router.post("/tables")
def create_tables(table: schema.CreateTableResource, db: Session = Depends(get_db), ):
    """
    create table resource
    :param table:
    :param db:
    :return:
    :exception:
    1. system_id not exist
    2. db_name exist under this system id
    """
    # check system_id exists
    systems = crud.get_resource(db, table.system_id, "System")
    if not systems:
        return {
            "status": "failed",
            "reason": f"system_id: {table.system_id} not exist"
        }

    # check db_id exists
    dbs = crud.get_resource(db, table.database_id, "Database")
    if not dbs:
        return {
            "status": "failed",
            "reason": f"database_id: {table.database_id} not exist"
        }
    # check if table_name exist under this system id & database id
    list_table_params = {
        "start": 0,
        "limit": 1,
        "query": table.table_name,
        "system_id": table.system_id,
        "database_id": table.database_id
    }
    tables_count, same_tables = crud.list_resources(db, list_table_params, "Table")
    if tables_count > 0:
        return {
            "reason": f"database name: {table.table_name} exists under database_id: {table.database_id}",
            "status": "failed"
        }
    # non-exist, then create
    new_table = crud.create_table(db, table)
    return {
        "data": new_table,
        "status": "success"
    }


@router.post("")
def create_data_directories(data_directory: schema.DataDirectory, db: Session = Depends(get_db), ):
    new_data_directory = crud.create_data_directory(db, data_directory)
    return {
        "data": new_data_directory,
        "status": "success"
    }


@router.get("")
def list_data_directories(query_params: schema.ListResources, db: Session = Depends(get_db), ):
    """
    get the data directory list
    :param query_params:
    :param db:
    :return:
    """
    entries_count, entries = crud.list_data_directories(db, query_params.dict())
    return {
        "data": entries,
        "count": entries_count,
        "tree": crud.list_tree(db, query_params.query)
    }


@router.get("/databases/{database_id}")
def get_db(database_id, db: Session = Depends(get_db), ):
    """

    :param database_id:
    :param db:
    :return:
    """
    db_database = crud.get_resource(db, database_id, "Database")
    if db_database:
        return {
            "data": db_database,
            "status": "success"
        }
    return {
        "reason": f"database_id: {database_id} not found",
        "status": "failed"
    }


@router.get("/systems/{system_id}")
def get_system(system_id, db: Session = Depends(get_db), ):
    db_system = crud.get_resource(db, system_id, "System")
    if db_system:
        return {
            "data": db_system,
            "status": "success"
        }
    return {
        "reason": f"system_id: {system_id} not found",
        "status": "failed"
    }


@router.get("/tables/{table_id}")
def get_table(table_id, db: Session = Depends(get_db), ):
    """

    :param table_id:
    :param db:
    :return:
    """
    db_table = crud.get_resource(db, table_id, "Table")
    if db_table:
        return {
            "data": db_table,
            "status": "success"
        }
    return {
        "reason": f"table_id: {table_id} not found",
        "status": "failed"
    }
