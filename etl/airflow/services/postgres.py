# airflow/services/postgres_service.py

from sqlalchemy import text
import time

class PostgresService:

    def __init__(self, engine, batch_size=500):
        self.engine = engine
        self.batch_size = batch_size

    def _load_query(self):
        with open("airflow/repository/queries/upsert.sql") as f:
            return text(f.read())

    def upsert_batch(self, df):
        total_records = len(df)

        print(f"[LOAD] Total records: {total_records}")
        print(f"[LOAD] Batch size: {self.batch_size}")

        query = self._load_query()

        start_time = time.time()
        total_batches = 0

        with self.engine.begin() as conn:
            for i in range(0, total_records, self.batch_size):
                batch = df.iloc[i:i + self.batch_size]
                records = batch.to_dict(orient="records")

                batch_start = time.time()

                conn.execute(query, records)

                batch_time = time.time() - batch_start
                total_batches += 1

                print(
                    f"[LOAD] Batch {total_batches} | "
                    f"Records: {len(records)} | "
                    f"Time: {round(batch_time, 2)}s"
                )

        total_time = time.time() - start_time

        print(f"[LOAD] Completed")
        print(f"[LOAD] Total batches: {total_batches}")
        print(f"[LOAD] Total time: {round(total_time, 2)}s")

    def count_target(self):
        query = text("SELECT COUNT(*) FROM staging.stg_google_trends")

        with self.engine.connect() as conn:
            total = conn.execute(query).scalar()

        print(f"[TARGET] Total records in staging: {total}")
        return total