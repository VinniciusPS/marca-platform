# airflow/services/google_trends.py

from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime

class GoogleTrendsService:

    def __init__(self):
        self.client = TrendReq(hl="pt-BR", tz=180)

    def fetch(self, keyword_groups, timeframe, geo="BR-RJ"):
        print(f"[EXTRACT] timeframe={timeframe} geo={geo}")

        all_data = []

        for group, keywords in keyword_groups.items():
            print(f"[EXTRACT] Fetching group: {group}")

            self.client.build_payload(keywords, timeframe=timeframe, geo=geo)
            data = self.client.interest_over_time()

            if data.empty:
                print(f"[EXTRACT] No data for {group}")
                continue

            data = data.reset_index()

            melted = data.melt(
                id_vars=["date"],
                value_vars=keywords,
                var_name="keyword",
                value_name="interest"
            )

            melted["group_name"] = group
            melted["specialty"] = group.split("_")[0]
            melted["ingestion_ts"] = datetime.utcnow()
            melted["updated_at"] = datetime.utcnow()

            all_data.append(melted)

        if not all_data:
            raise ValueError("No data extracted")

        df = pd.concat(all_data, ignore_index=True)

        print(f"[EXTRACT] Total rows: {len(df)}")
        print(f"[EXTRACT] Columns: {list(df.columns)}")
        print("[EXTRACT] Sample:")
        print(df.head(5).to_string())

        return df

def resolve_timeframe(last_watermark):

    if not last_watermark:
        print("[WINDOW] First load → 30 days")
        return "today 1-m"

    print("[WINDOW] Incremental load → last 1 day")
    return "now 1-d"