from typing import Generator
from datetime import datetime, timezone
from models.google_trends import GoogleTrendsRawDTO, GoogleTrendsStorageDTO

class GoogleTrendsMapper:
    """
    Responsabilidade: Transformar o Contrato de Extração (Raw) 
    no Contrato de Armazenamento (Storage), aplicando regras de negócio.
    """

    @staticmethod
    def _derive_specialty(group_name: str) -> str:
        """
        Regra de negócio: Deriva a especialidade a partir do grupo.
        Ex: 'teste_odontologia' -> 'odontologia'
        """
        if "_" in group_name:
            return group_name.split("_")[-1]
        return group_name

    def transform_stream(
        self, raw_stream: Generator[GoogleTrendsRawDTO, None, None]
    ) -> Generator[GoogleTrendsStorageDTO, None, None]:
        """
        Recebe um generator de RawDTO e produz um generator de StorageDTO.
        """
        now = datetime.now(timezone.utc)

        for raw in raw_stream:
            yield GoogleTrendsStorageDTO(
                source_date=raw.date,
                keyword=raw.keyword,
                group_name=raw.group_name,
                specialty=self._derive_specialty(raw.group_name),
                interest=raw.value,
                created_at=now,
                updated_at=now
            )