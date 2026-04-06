from db.connection import get_connection
from datetime import datetime
import json
import time
from core.log import logger
from config.config import config
MAX_RETRIES = config["processing"]["max_retries"]
# MAX_RETRIES = 3

def upsert_file(path):
    for attempt in range(MAX_RETRIES):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO all_files (file_path, file_status, last_modified)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                last_modified = VALUES(last_modified),
                file_status = 'NEW'
            """

            cursor.execute(query, (path, "NEW", datetime.now()))
            conn.commit()

            logger.info(f"upsert_file success: {path}")
            return

        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"upsert_file failed (attempt {attempt+1}): {path} | error: {e}")
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(1 * (attempt + 1))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def mark_modified(path):
    for attempt in range(MAX_RETRIES):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
            UPDATE all_files
            SET last_modified = %s,
                file_status = 'NEW'
            WHERE file_path = %s
            """

            cursor.execute(query, (datetime.now(), path))
            conn.commit()

            logger.info(f"mark_modified success: {path}")
            return

        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"mark_modified failed (attempt {attempt+1}): {path} | error: {e}")
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(1 * (attempt + 1))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def mark_renamed(old_path, new_path):
    for attempt in range(MAX_RETRIES):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
            UPDATE all_files
            SET file_path = %s,
                file_status = 'NEW',
                last_modified = %s
            WHERE file_path = %s
            """

            cursor.execute(query, (new_path, datetime.now(), old_path))
            conn.commit()

            logger.info(f"mark_renamed success: {old_path} -> {new_path}")
            return

        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"mark_renamed failed (attempt {attempt+1}): {old_path} -> {new_path} | error: {e}")
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(1 * (attempt + 1))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def mark_deleted(path):
    for attempt in range(MAX_RETRIES):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
            UPDATE all_files
            SET file_status = 'DELETED'
            WHERE file_path = %s
            """

            cursor.execute(query, (path,))
            conn.commit()

            logger.info(f"mark_deleted success: {path}")
            return

        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"mark_deleted failed (attempt {attempt+1}): {path} | error: {e}")
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(1 * (attempt + 1))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def move_file(src_path, dest_path):
    for attempt in range(MAX_RETRIES):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
            UPDATE all_files
            SET file_path = %s,
                file_status = 'NEW'
            WHERE file_path = %s
            """

            cursor.execute(query, (dest_path, src_path))
            conn.commit()

            logger.info(f"move_file success: {src_path} -> {dest_path}")
            return
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"move_file failed (attempt {attempt+1}): {src_path} -> {dest_path} | error: {e}")
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(1 * (attempt + 1))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def get_file_id_by_path(path):
    for attempt in range(MAX_RETRIES):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
            SELECT file_id
            FROM all_files
            WHERE file_path = %s
            """

            cursor.execute(query, (path,))
            row = cursor.fetchone()

            logger.info(f"get_file_id_by_path success: {path}")
            return row[0] if row else None

        except Exception as e:
            logger.error(f"get_file_id_by_path failed (attempt {attempt+1}): {path} | error: {e}")
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(1 * (attempt + 1))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def mark_invalid(path):
    for attempt in range(MAX_RETRIES):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
            UPDATE all_files
            SET file_status = 'INVALID',
                last_modified = %s
            WHERE file_path = %s
            """

            cursor.execute(query, (datetime.now(), path))
            conn.commit()

            logger.info(f"mark_invalid success: {path}")
            return

        except Exception as e:
            if conn:
                conn.rollback()

            logger.error(
                f"mark_invalid failed (attempt {attempt+1}): {path} | error: {e}"
            )

            if attempt == MAX_RETRIES - 1:
                raise

            time.sleep(1 * (attempt + 1))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def mark_processing(path):
    for attempt in range(MAX_RETRIES):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
            UPDATE all_files
            SET file_status = 'PROCESSING',
                last_modified = %s
            WHERE file_path = %s
            """

            cursor.execute(query, (datetime.now(), path))
            conn.commit()

            logger.info(f"mark_processing success: {path}")
            return

        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"mark_processing failed (attempt {attempt+1}): {path} | error: {e}")
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(1 * (attempt + 1))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def mark_processed(path):
    for attempt in range(MAX_RETRIES):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
            UPDATE all_files
            SET file_status = 'PROCESSED',
                last_modified = %s
            WHERE file_path = %s
            """

            cursor.execute(query, (datetime.now(), path))
            conn.commit()

            logger.info(f"mark_processed success: {path}")
            return

        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"mark_processed failed (attempt {attempt+1}): {path} | error: {e}")
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(1 * (attempt + 1))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def get_new_documents(limit=10):
    for attempt in range(MAX_RETRIES):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT file_id, file_path
                FROM all_files
                WHERE file_status = 'NEW'
                AND (
                    file_path LIKE '%.pdf' OR
                    file_path LIKE '%.docx' OR
                    file_path LIKE '%.pptx' OR
                    file_path LIKE '%.txt'
                )
                LIMIT %s
            """, (limit,))

            rows = cursor.fetchall()

            logger.info(f"get_new_documents success: fetched {len(rows)} rows")
            return rows

        except Exception as e:
            logger.error(f"get_new_documents failed (attempt {attempt+1}): error: {e}")
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(1 * (attempt + 1))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
