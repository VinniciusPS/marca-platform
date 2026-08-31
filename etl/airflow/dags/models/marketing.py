 from pydantic import BaseModel, Field, ConfigDict
    
    
    class MarketingSearchTermModel(BaseModel):
        """Model para termos de busca de marketing por especialidade."""
        model_config = ConfigDict(from_attributes=True)
    
        specialty_id: int = Field(..., gt=0)
        search_term: str = Field(..., min_length=1)
    
    
    class MarketingBenchmarkModel(BaseModel):
        """Model para benchmarks econômicos de mídia de marketing (Google Ads / Performance)."""
        model_config = ConfigDict(from_attributes=True)
    
        specialty: str = Field(..., min_length=1)
        base_cpc: str = Field(...)          # Ex: "3.5000"
        base_cvr: str = Field(...)          # Ex: "0.0450" (4.5%)
        elasticity_score: str = Field(...)  # Ex: "0.85"
        net_margin_limit: str = Field(...)  # Ex: "220.00"