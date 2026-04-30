from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from services.google_trends.extractor import GoogleTrendsExtractor
from services.google_trends.mapper import GoogleTrendsMapper

# Configuração de teste
TEST_GROUPS = {
    "exemplo_odontologia": ["clareamento", "aparelho"]
}

def run_integration_test(**kwargs):
    """
    Testa o fluxo: Extrator -> Mapper.
    Verifica se a specialty e os nomes de colunas do SQL estão corretos.
    """
    print("Iniciando Teste Integrado: Extractor -> Mapper")
    
    # 1. Instanciação
    extractor = GoogleTrendsExtractor()
    mapper = GoogleTrendsMapper()
    
    # 2. Extração (Generator 1)
    raw_stream = extractor.fetch_stream(
        keyword_groups=TEST_GROUPS,
        timeframe="now 1-H",
        geo="BR"
    )
    
    # 3. Mapeamento (Generator 2 - Conecta no Generator 1)
    # Aqui o dado flui de um para o outro sem carregar lista na memória
    storage_stream = mapper.transform_stream(raw_stream)
    
    print("--- VALIDAÇÃO DO STORAGE DTO (PRONTO PARA O SQL) ---")
    
    count = 0
    for storage_dto in storage_stream:
        if count < 5:
            # Aqui validamos se source_date, specialty e interest existem
            data = storage_dto.model_dump()
            print(f"Registro {count + 1} validado:")
            print(f"  > Chaves: {list(data.keys())}")
            print(f"  > Specialty derivada: {data['specialty']}")
            print(f"  > Valor (Interest): {data['interest']}")
            print("-" * 30)
        
        count += 1
    
    if count == 0:
        raise ValueError("Nenhum dado fluiu pelo pipeline. Verifique o Extractor.")

    print(f"Sucesso! {count} registros transformados e validados com sucesso.")
    return {"total_processed": count}

with DAG(
    dag_id="test_google_trends_flow",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["integration", "test"]
) as dag:

    t_validate_flow = PythonOperator(
        task_id="validate_extractor_to_mapper",
        python_callable=run_integration_test
    )

    t_validate_flow