from uuid import uuid4
from sqlalchemy import and_, text
from sqlalchemy.orm import Session

from models import data_directory as model
from schemas import data_directory as schema

DOUBLE_PERCENTAGE_QUERY = "%{}%"


def create_data_directory(db: Session, data_directory: schema.DataDirectory):
    db_data = model.DataDirectory(id=str(uuid4()),
                                  system_id=data_directory.system_id,
                                  db_id=data_directory.db_id,
                                  table_id=data_directory.table_id,
                                  entry_name=data_directory.entry_name,
                                  entry_name_chn=data_directory.entry_name_chn,
                                  comment=data_directory.entry_comment,
                                  entry_length=data_directory.entry_length,
                                  entry_type=data_directory.entry_type)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def create_system(db: Session, system: schema.CreateSystemResource):
    db_system = model.DBResource(
        id=str(uuid4()),
        resource_name=system.system_name,
        resource_type='System',
        resource_comment=system.system_comment,
        extra=dict()
    )
    db.add(db_system)
    db.commit()
    db.refresh(db_system)
    return db_system


def delete_resource(db: Session, resource_id, resource_type):
    db_resource = db.query(model.DBResource).filter(model.DBResource.resource_type == resource_type) \
        .filter(model.DBResource.id == resource_id).delete()
    db.commit()
    return db_resource


def create_database(db: Session, database: schema.CreateDBResource):
    db_database = model.DBResource(
        id=str(uuid4()),
        resource_name=database.db_name,
        resource_type='Database',
        resource_comment=database.db_comment,
        system_id=database.system_id,
        extra=dict()
    )
    db.add(db_database)
    db.commit()
    db.refresh(db_database)
    return db_database


def create_table(db: Session, table: schema.CreateTableResource):
    db_database = model.DBResource(
        id=str(uuid4()),
        resource_name=table.table_name,
        resource_type='Table',
        resource_comment=table.table_comment,
        system_id=table.system_id,
        database_id=table.database_id,
        extra=dict()
    )
    db.add(db_database)
    db.commit()
    db.refresh(db_database)
    return db_database


def list_resources(db: Session, query_params, resource_type):
    """
    get the resources list
    :param db: db connection
    :param query_params: search the resource_name column using like
    :param: resource_type:
    :return:
    :sql:   SELECT */COUNT(*) FROM db_resources
            WHERE resource_type = {resource_type}
            AND resource_name LIKE %{query_params.query[0]}%
            AND resource_name LIKE %{query_params.query[1]}%
            ...
            LIMIT query_params.start, query_params.limit
    """
    base_query = db.query(model.DBResource).filter(model.DBResource.resource_type == resource_type)
    if query_params.get("query"):
        format_query = [model.DBResource.resource_name.like(DOUBLE_PERCENTAGE_QUERY.format(q))
                        for q in query_params.get("query")]
        base_query = base_query.filter(and_(*format_query))
    if query_params.get("ids"):
        base_query = base_query.filter(model.DBResource.id.in_(query_params.get("ids")))
    if query_params.get("system_id"):
        base_query = base_query.filter(model.DBResource.system_id == query_params.get("system_id"))
    if query_params.get("database_id"):
        base_query = base_query.filter(model.DBResource.database_id == query_params.get("database_id"))
    # if query_params.get("system_ids"):
    #     base_query = base_query.filter(model.DBResource.system_id.in_(query_params.get("system_ids")))
    count = base_query.count()
    systems = base_query.offset(query_params.get("start")).limit(query_params.get("limit")).all()
    return count, systems


def get_resource(db: Session, resource_id, resource_type: str):
    return db.query(model.DBResource).filter(model.DBResource.resource_type == resource_type). \
        filter(model.DBResource.id == resource_id).first()


def list_data_directories(db: Session, query_params):
    """
    get the data directories list
    :param db: db connection
    :param query_params: search the data directories by query
    :return:
    :sql:   SELECT * FROM db_resources
            WHERE resource_type = {resource_type}
            AND resource_name LIKE %{query_params.query[0]}%
            AND resource_name LIKE %{query_params.query[1]}%
            ...
            LIMIT query_params.start, query_params.limit
    """
    print("I ma in")
    base_query = db.query(model.DataDirectory)
    if query_params.get("query"):
        format_query = [model.DataDirectory.resource_name.like(DOUBLE_PERCENTAGE_QUERY.format(q))
                        for q in query_params.get("query")]
        base_query = base_query.filter(and_(*format_query))
    if query_params.get("ids"):
        base_query = base_query.filter(model.DataDirectory.id.in_(query_params.get("ids")))
    if query_params.get("system_ids"):
        base_query = base_query.filter(model.DBResource.system_id.in_(query_params.get("system_ids")))
    if query_params.get("database_ids"):
        base_query = base_query.filter(model.DBResource.database_id.in_(query_params.get("database_ids")))
    if query_params.get("table_ids"):
        base_query = base_query.filter(model.DBResource.table_id.in_(query_params.get("table_ids")))
    count = base_query.count()

    systems = base_query.offset(query_params.get("start")).limit(query_params.get("limit")).all()
    return count, systems


def list_tree(db: Session, query_list):
    result = []
    for row in db.execute(text("select distinct system_id, db_id, table_id from data_directories")):
        result.append(
            {
                "system_id": row[0],
                "database_id": row[1],
                "table_id": row[2]
            }
        )
    return result
