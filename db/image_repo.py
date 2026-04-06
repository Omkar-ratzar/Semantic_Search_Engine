from db.connection import get_connection
from datetime import datetime
import json
import time
from core.log import logger
from config.config import config
MAX_RETRIES = config["processing"]["max_retries"]


def upsert_image_metadata(file_id, file_path, description, exif_dict, status="NEW"):
    for attempt in range(MAX_RETRIES):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO image_metadata (file_id, file_path, description, exif, status)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                file_path = VALUES(file_path),
                description = VALUES(description),
                exif = VALUES(exif),
                status = VALUES(status)
            """

            exif_json = json.dumps(exif_dict) if exif_dict else None

            cursor.execute(query, (file_id, file_path, description, exif_json, status))
            conn.commit()

            logger.info(f"upsert_image_metadata success: file_id={file_id}")
            return

        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"upsert_image_metadata failed (attempt {attempt+1}): file_id={file_id} | error: {e}")
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(1 * (attempt + 1))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def get_image_text_for_embedding(file_id):
    for attempt in range(MAX_RETRIES):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
            SELECT description, exif
            FROM image_metadata
            WHERE file_id = %s AND status = 'PROCESSED'
            """

            cursor.execute(query, (file_id,))
            row = cursor.fetchone()

            if not row:
                return None

            description, exif_json = row

            exif_text = ""
            if exif_json:
                try:
                    exif_dict = json.loads(exif_json)
                    exif_text = " ".join(f"{k}:{v}" for k, v in exif_dict.items())
                except Exception as e:
                    logger.error(f"EXIF parse failed for file_id={file_id}: {e}")

            logger.info(f"get_image_text_for_embedding success: file_id={file_id}")
            return f"{description or ''} {exif_text}".strip()

        except Exception as e:
            logger.error(f"get_image_text_for_embedding failed (attempt {attempt+1}): file_id={file_id} | error: {e}")
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(1 * (attempt + 1))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def get_new_images(limit=10):
    for attempt in range(MAX_RETRIES):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT file_id, file_path
                FROM image_metadata
                WHERE status = 'NEW'
                LIMIT %s
            """, (limit,))

            rows = cursor.fetchall()

            logger.info(f"get_new_images success: fetched {len(rows)} rows")
            return rows

        except Exception as e:
            logger.error(f"get_new_images failed (attempt {attempt+1}): error: {e}")
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(1 * (attempt + 1))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def mark_processing_metadata(file_id):
    for attempt in range(MAX_RETRIES):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE image_metadata
                SET status = 'PROCESSING'
                WHERE file_id = %s
            """, (file_id,))

            conn.commit()

            logger.info(f"mark_processing_metadata success: file_id={file_id}")
            return

        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"mark_processing_metadata failed (attempt {attempt+1}): file_id={file_id} | error: {e}")
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(1 * (attempt + 1))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def mark_processed_metadata(file_id):
    for attempt in range(MAX_RETRIES):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE image_metadata
                SET status = 'PROCESSED'
                WHERE file_id = %s
            """, (file_id,))

            conn.commit()

            logger.info(f"mark_processed_metadata success: file_id={file_id}")
            return

        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"mark_processed_metadata failed (attempt {attempt+1}): file_id={file_id} | error: {e}")
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(1 * (attempt + 1))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

