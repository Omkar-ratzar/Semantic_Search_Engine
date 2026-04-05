from db_info import get_connection
from datetime import datetime
import json

def upsert_file(path):
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

    cursor.close()
    conn.close()

def mark_modified(path):
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

    cursor.close()
    conn.close()

def mark_renamed(old_path, new_path):
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
    cursor.close()
    conn.close()

def mark_deleted(path):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE all_files
    SET file_status = 'DELETED'
    WHERE file_path = %s
    """

    cursor.execute(query, (path,))
    conn.commit()

    cursor.close()
    conn.close()

def move_file(src_path, dest_path):
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

    cursor.close()
    conn.close()

def mark_processing(path):
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

    cursor.close()
    conn.close()

def mark_processed(path):
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

    cursor.close()
    conn.close()

def upsert_image_metadata(file_id, file_path, description, exif_dict, status="PROCESSED"):
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

    cursor.close()
    conn.close()

def get_file_id_by_path(path):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT file_id
    FROM all_files
    WHERE file_path = %s
    """

    cursor.execute(query, (path,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row[0] if row else None

def get_image_text_for_embedding(file_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT description, exif
    FROM image_metadata
    WHERE file_id = %s AND status = 'PROCESSED'
    """

    cursor.execute(query, (file_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return None

    description, exif_json = row

    exif_text = ""
    if exif_json:
        try:
            exif_dict = json.loads(exif_json)
            exif_text = " ".join(f"{k}:{v}" for k, v in exif_dict.items())
        except:
            pass

    return f"{description or ''} {exif_text}".strip()

def get_new_images(limit=10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT file_id, file_path
        FROM image_metadata
        WHERE status = 'NEW'
        LIMIT %s
    """, (limit,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows

def mark_processing_metadata(file_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE image_metadata
        SET status = 'PROCESSING'
        WHERE file_id = %s
    """, (file_id,))

    conn.commit()
    cursor.close()
    conn.close()

def mark_processed_metadata(file_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE image_metadata
        SET status = 'PROCESSED'
        WHERE file_id = %s
    """, (file_id,))

    conn.commit()
    cursor.close()
    conn.close()
