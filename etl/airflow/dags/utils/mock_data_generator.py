"""
Generic mock data generator utility.

Agnóstico a domínio - pode ser reutilizado por qualquer DAG.
Define COMO gerar, não O QUÊ gerar.
"""

import random
import string
from typing import Generator, Dict, Any, List, Optional
from datetime import datetime, timedelta


class MockDataFactory:
    """
    Gerador agnóstico de dados mock.
    
    Aceita definição de campos e gera registros realistas.
    Suporta: str, int, float, decimal, date, datetime, bool
    Padrões: realistic, cpf, crm, email, uuid, range, choice, sequence
    """

    def __init__(self, seed: Optional[int] = None):
        """
        Inicializa factory com seed opcional para reprodutibilidade.
        
        Args:
            seed: Seed para random (None = aleatório)
        """
        if seed is not None:
            random.seed(seed)

    def generate(
        self,
        field_definitions: Dict[str, Dict[str, Any]],
        rows_quantity: int
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Gera dados baseado em definição de campos.
        
        Args:
            field_definitions: Dict com definição de cada campo
            rows_quantity: Número de registros a gerar
            
        Yields:
            Dict com um registro gerado
            
        Exemplo:
            config = {
                "name": {"type": "str", "pattern": "realistic"},
                "cpf": {"type": "str", "pattern": "cpf", "unique": True},
                "created_at": {"type": "datetime", "auto": True}
            }
            factory = MockDataFactory()
            for record in factory.generate(config, 100):
                print(record)
        """
        generated_values = {}  # Para rastrear valores únicos
        
        for row_idx in range(rows_quantity):
            record = {}
            
            for field_name, field_config in field_definitions.items():
                unique = field_config.get("unique", False)
                
                # Se já foi gerado, pula
                if unique and field_name in generated_values:
                    if len(generated_values[field_name]) >= rows_quantity:
                        raise ValueError(
                            f"Cannot generate {rows_quantity} unique values for {field_name}"
                        )
                
                value = self._generate_value(field_config, row_idx)
                
                # Garante unicidade
                if unique:
                    if field_name not in generated_values:
                        generated_values[field_name] = set()
                    
                    # Regenera se já existe
                    attempts = 0
                    while value in generated_values[field_name] and attempts < 100:
                        value = self._generate_value(field_config, row_idx + attempts)
                        attempts += 1
                    
                    generated_values[field_name].add(value)
                
                record[field_name] = value
            
            yield record

    def _generate_value(self, config: Dict[str, Any], row_index: int) -> Any:
        """
        Gera valor único baseado em configuração de campo.
        
        Args:
            config: Dict com type, pattern, range, choices, etc.
            row_index: Índice da linha (útil para sequências)
            
        Returns:
            Valor gerado do tipo apropriado
        """
        field_type = config.get("type", "str")
        pattern = config.get("pattern")
        
        if field_type == "str":
            return self._generate_string(config, row_index, pattern)
        elif field_type == "int":
            return self._generate_int(config, row_index)
        elif field_type == "float":
            return self._generate_float(config, row_index)
        elif field_type == "decimal":
            return self._generate_decimal(config, row_index)
        elif field_type == "bool":
            return self._generate_bool(config)
        elif field_type == "date":
            return self._generate_date(config)
        elif field_type == "datetime":
            return self._generate_datetime(config)
        else:
            raise ValueError(f"Unknown type: {field_type}")

    def _generate_string(
        self, 
        config: Dict[str, Any], 
        row_index: int, 
        pattern: Optional[str]
    ) -> str:
        """Gera string baseado em padrão."""
        if pattern == "realistic":
            return self._realistic_string()
        elif pattern == "cpf":
            return self._generate_cpf()
        elif pattern == "crm":
            return self._generate_crm()
        elif pattern == "email":
            return self._generate_email()
        elif pattern == "sequence":
            return f"{config.get('prefix', 'item')}_{row_index}"
        elif pattern == "choice":
            choices = config.get("choices", [])
            return random.choice(choices) if choices else f"value_{row_index}"
        elif "length" in config:
            length = config.get("length", 10)
            return "".join(random.choices(string.ascii_letters + string.digits, k=length))
        else:
            return f"string_{row_index}"

    def _generate_int(self, config: Dict[str, Any], row_index: int) -> int:
        """Gera inteiro baseado em range."""
        if "range" in config:
            min_val, max_val = config["range"]
            return random.randint(min_val, max_val)
        elif "choice" in config:
            return random.choice(config["choice"])
        else:
            return row_index

    def _generate_float(self, config: Dict[str, Any], row_index: int) -> float:
        """Gera float baseado em range."""
        if "range" in config:
            min_val, max_val = config["range"]
            return round(random.uniform(min_val, max_val), 2)
        else:
            return float(row_index)

    def _generate_decimal(self, config: Dict[str, Any], row_index: int) -> str:
        """Gera decimal como string (para Pydantic Decimal)."""
        if "range" in config:
            min_val, max_val = config["range"]
            value = round(random.uniform(min_val, max_val), 2)
            return str(value)
        else:
            return str(float(row_index))

    def _generate_bool(self, config: Dict[str, Any]) -> bool:
        """Gera booleano."""
        probability = config.get("true_probability", 0.5)
        return random.random() < probability

    def _generate_date(self, config: Dict[str, Any]) -> str:
        """Gera data como string (YYYY-MM-DD)."""
        if "days_offset" in config:
            offset = config.get("days_offset", -30)
            date = datetime.now() + timedelta(days=offset)
        else:
            start = datetime.now() - timedelta(days=365)
            end = datetime.now()
            time_between = end - start
            random_days = random.randint(0, time_between.days)
            date = start + timedelta(days=random_days)
        
        return date.strftime("%Y-%m-%d")

    def _generate_datetime(self, config: Dict[str, Any]) -> str:
        """Gera datetime como string ISO."""
        if "days_offset" in config:
            offset = config.get("days_offset", -30)
            dt = datetime.now() + timedelta(days=offset)
        else:
            start = datetime.now() - timedelta(days=365)
            end = datetime.now()
            time_between = end - start
            random_seconds = random.randint(0, int(time_between.total_seconds()))
            dt = start + timedelta(seconds=random_seconds)
        
        return dt.isoformat()

    def _realistic_string(self) -> str:
        """Gera string realista (nome-like)."""
        first_names = [
            "João", "Maria", "José", "Ana", "Carlos", "Francisca", 
            "Paulo", "Antônia", "Pedro", "Fernanda"
        ]
        last_names = [
            "Silva", "Santos", "Oliveira", "Souza", "Costa", 
            "Ferreira", "Gomes", "Martins", "Rocha", "Alves"
        ]
        return f"{random.choice(first_names)} {random.choice(last_names)}"

    def _generate_cpf(self) -> str:
        """Gera CPF válido no formato XXX.XXX.XXX-XX."""
        numbers = [random.randint(0, 9) for _ in range(9)]
        
        # Calcula primeiro dígito verificador
        sum_val = sum(a * b for a, b in zip(numbers, range(10, 1, -1)))
        digit1 = (sum_val * 10) % 11
        digit1 = digit1 if digit1 < 10 else 0
        
        # Calcula segundo dígito verificador
        numbers.append(digit1)
        sum_val = sum(a * b for a, b in zip(numbers, range(11, 1, -1)))
        digit2 = (sum_val * 10) % 11
        digit2 = digit2 if digit2 < 10 else 0
        
        numbers.append(digit2)
        
        cpf_str = "".join(map(str, numbers))
        return f"{cpf_str[:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:]}"

    def _generate_crm(self) -> str:
        """Gera CRM no formato NNNNN/UF-YYYY."""
        number = random.randint(10000, 99999)
        states = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", 
                  "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", 
                  "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
        state = random.choice(states)
        year = random.randint(2000, datetime.now().year)
        return f"{number}/{state}-{year}"

    def _generate_email(self) -> str:
        """Gera email realista."""
        username = "".join(random.choices(string.ascii_lowercase, k=8))
        domain = random.choice(["gmail.com", "hotmail.com", "empresa.com", "example.com"])
        return f"{username}@{domain}"
