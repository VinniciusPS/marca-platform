import time
import pandas as pd
from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError

from models.google_trends import GoogleTrendsRawDTO
from typing import Generator, Optional

class GoogleTrendsExtractor:
    """
    Gateway para extração de dados do Google Trends.
    Foca em traduzir o retorno do PyTrends para o domínio (RawDTO).
    """

    def __init__(self, hl: str = "pt-BR", tz: int = -180):
        self.client = TrendReq(hl=hl, tz=tz)

    def fetch_stream(self, keyword_groups: dict, timeframe: str, geo: str = "BR") -> Generator[GoogleTrendsRawDTO, None, None]:
        """
        Extrai dados e entrega um stream (generator) de objetos do domínio.
        """
        for group_name, keywords in keyword_groups.items():
            raw_df = self._request_data(keywords, timeframe, geo)

            if raw_df is None or raw_df.empty:
                continue

            # Delegação da transformação de DataFrame para Stream
            yield from self._df_to_dto_stream(raw_df, group_name)

    def _df_to_dto_stream(self, df: pd.DataFrame, group_name: str) -> Generator[GoogleTrendsRawDTO, None, None]:
        """
        Converte o DataFrame bruto (wide) para o formato do contrato (long/tidy).
        """
        df = df.reset_index()
        # Filtra colunas de keywords, ignorando metadados do pytrends
        target_cols = [c for c in df.columns if c not in ["date", "isPartial"]]

        for _, row in df.iterrows():
            for kw in target_cols:
                yield GoogleTrendsRawDTO(
                    date=row["date"],
                    keyword=kw,
                    value=int(row[kw]),
                    group_name=group_name
                )

    def _request_data(self, keywords: list, timeframe: str, geo: str) -> Optional[pd.DataFrame]:
        """
        Abstração da chamada externa com política de retry.
        """
        try:
            self.client.build_payload(keywords, timeframe=timeframe, geo=geo)
            return self._safe_call(lambda: self.client.interest_over_time())
        except Exception as e:
            # Aqui poderíamos logar o erro em um serviço de monitoramento
            print(f"Error fetching group {keywords}: {e}")
            return None

    def _safe_call(self, func, max_retries: int = 5):
        """
        Implementa Exponential Backoff para evitar Rate Limit.
        """
        for i in range(max_retries):
            try:
                return func()
            except TooManyRequestsError:
                wait_time = (2 ** i) * 5
                print(f"Rate limit hit. Waiting {wait_time}s...")
                time.sleep(wait_time)
        
        raise RuntimeError("Google Trends rate limit persistent after retries.")