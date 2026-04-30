# airflow/services/load_control_service.py

from sqlalchemy import text
from datetime import datetime

class LoadControlService:

    def __init__(self, engine):
        self.engine = engine

    def start_load(self, dataset_name):
        query = text("""
            INSERT INTO control.etl_load (dataset_name, status, start_time)
            VALUES (:dataset_name, 'running', CURRENT_TIMESTAMP)
            RETURNING id;
        """)

        with self.engine.begin() as conn:
            load_id = conn.execute(query, {
                "dataset_name": dataset_name
            }).scalar()

        print(f"[LOAD CONTROL] Started load_id={load_id}")

        return load_id

    def finish_load(self, load_id, status, rows_extracted=0, rows_loaded=0, error_message=None, last_extracted_at=None):

        query = text("""
            UPDATE control.etl_load
            SET
                status = :status,
                end_time = CURRENT_TIMESTAMP,
                rows_extracted = :rows_extracted,
                rows_loaded = :rows_loaded,
                error_message = :error_message,
                last_extracted_at = :last_extracted_at
            WHERE id = :load_id;
        """)

        with self.engine.begin() as conn:
            conn.execute(query, {
                "load_id": load_id,
                "status": status,
                "rows_extracted": rows_extracted,
                "rows_loaded": rows_loaded,
                "error_message": error_message,
                "last_extracted_at": last_extracted_at
            })

        print(f"[LOAD CONTROL] Finished load_id={load_id} status={status}")

    def get_last_successful_watermark(self, dataset_name):
        query = text("""
            SELECT MAX(last_extracted_at)
            FROM control.etl_load
            WHERE dataset_name = :dataset_name
              AND status = 'success';
        """)

        with self.engine.connect() as conn:
            result = conn.execute(query, {
                "dataset_name": dataset_name
            }).scalar()

        print(f"[LOAD CONTROL] Last watermark: {result}")

        return result