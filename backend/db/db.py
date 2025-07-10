import uuid
import time
import logging
from contextlib import contextmanager
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.config import DATABASE_URL
from backend.utils.logging_utils import method_name
from backend.db.init_db import engine  # Use the one you've already set up elsewhere

log = logging.getLogger(__name__)

@contextmanager
def managed_connection():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

def insert(table_name: str, columns_list: list[str], values_list: list):
    start_time = time.time()
    request_id = str(uuid.uuid4())
    log.info(f"[{request_id}] Inserting values into {table_name}: {values_list}")

    with managed_connection() as db:
        columns = ', '.join(columns_list)
        placeholders = ', '.join([f":val{i}" for i in range(len(values_list))])
        query = text(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})")
        params = {f"val{i}": v for i, v in enumerate(values_list)}

        result = db.execute(query, params)
        db.commit()

    exec_time = round(time.time() - start_time, 4)
    log.info(f"[{request_id}] {method_name()} completed in {exec_time}s")
    return result.rowcount

def select(table_name: str, columns: str = "*", condition: dict = None):
    start_time = time.time()
    request_id = str(uuid.uuid4())
    log.info(f"[{request_id}] Selecting {columns} from {table_name} where {condition}")

    with managed_connection() as db:
        query_str = f"SELECT {columns} FROM {table_name}"
        params = {}

        if condition:
            clause = ' AND '.join([f"{k} = :{k}" for k in condition.keys()])
            query_str += f" WHERE {clause}"
            params = condition

        query = text(query_str)
        result = db.execute(query, params)
        rows = result.fetchall()
        columns = result.keys()
        records = [dict(zip(columns, row)) for row in rows]

    exec_time = round(time.time() - start_time, 4)
    log.info(f"[{request_id}] {method_name()} completed in {exec_time}s")
    return records

def update(table_name: str, data: dict, update_condition: dict):
    """

    Args:
        table_name (str): the name of the table
        data (dict): data to be included in the update
        update_condition (dict): condition of what to update

    Returns:
        int: number of rows impacted
    """
    start_time = time.time()
    request_id = str(uuid.uuid4())

    if not update_condition:
        raise ValueError("Update condition must be provided.")

    log.info(f"[{request_id}] Updating {table_name}: {data} where {update_condition}")

    with managed_connection() as db:
        set_clause = ', '.join([f"{k} = :set_{k}" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = :cond_{k}" for k in update_condition.keys()])
        query_str = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

        params = {f"set_{k}": v for k, v in data.items()}
        params.update({f"cond_{k}": v for k, v in update_condition.items()})

        query = text(query_str)
        result = db.execute(query, params)
        db.commit()

    exec_time = round(time.time() - start_time, 4)
    log.info(f"[{request_id}] {method_name()} completed in {exec_time}s")
    return result.rowcount

def delete(table_name: str, condition: dict):
    """
    Delete records from a table.
    
    Args:
        table_name (str): the name of the table
        condition (dict): condition of what to delete
    """
    start_time = time.time()
    request_id = str(uuid.uuid4())

    if not condition:
        raise ValueError("Delete condition must be provided.")

    log.info(f"[{request_id}] Deleting from {table_name} where {condition}")

    with managed_connection() as db:
        where_clause = ' AND '.join([f"{k} = :{k}" for k in condition.keys()])
        query_str = f"DELETE FROM {table_name} WHERE {where_clause}"
        query = text(query_str)

        result = db.execute(query, condition)
        db.commit()

    exec_time = round(time.time() - start_time, 4)
    log.info(f"[{request_id}] {method_name()} completed in {exec_time}s")
    return result.rowcount

def exists(table_name: str, condition: dict):
    """
    Check if any record exists matching the condition.
    
    Args:
        table_name (str): the name of the table
        condition (dict): condition of what to check
    """
    start_time = time.time()
    request_id = str(uuid.uuid4())

    log.info(f"[{request_id}] Checking existence in {table_name} where {condition}")

    with managed_connection() as db:
        where_clause = ' AND '.join([f"{k} = :{k}" for k in condition.keys()])
        query_str = f"SELECT EXISTS (SELECT 1 FROM {table_name} WHERE {where_clause})"
        query = text(query_str)

        result = db.execute(query, condition).scalar()

    exec_time = round(time.time() - start_time, 4)
    log.info(f"[{request_id}] {method_name()} completed in {exec_time}s")
    return bool(result)
