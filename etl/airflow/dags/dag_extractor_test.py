from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from services.google_trends.extractor import GoogleTrendsExtractor

# Mock de entrada para o teste
TEST_GROUPS = {
    "teste_odontologia": ["dentista", "ortodontia"]
}

def run_extractor_test(**kwargs):
    """
    Executa o extractor e valida o stream de DTOs.
    """
    print("Iniciando teste do Extractor...")
    
    extractor = GoogleTrendsExtractor()
    
    # Geramos o stream
    stream = extractor.fetch_stream(
        keyword_groups=TEST_GROUPS,
        timeframe="now 1-H",  # Curto período para teste rápido
        geo="BR"
    )
    
    records_count = 0
    print("--- AMOSTRA DE DADOS (RAW DTO) ---")
    
    for dto in stream:
        # Validamos se é de fato um objeto Pydantic
        if records_count < 5:
            print(f"Registro {records_count + 1}: {dto.model_dump_json(indent=2)}")
        
        records_count += 1
    
    print(f"--- FIM DA AMOSTRA ---")
    print(f"Total de registros processados no stream: {records_count}")
    
    if records_count == 0:
        raise ValueError("O Extractor não retornou dados. Verifique a conexão ou os termos.")

    return {"total_extracted": records_count}

with DAG(
    dag_id="test_google_trends_extractor",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["test", "extractor"]
) as dag:

    t_test = PythonOperator(
        task_id="validate_extractor_stream",
        python_callable=run_extractor_test
    )

    t_test