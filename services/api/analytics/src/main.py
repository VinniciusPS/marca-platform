from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from interfaces.api.routes import router as patient_router, analytics_router

def create_app() -> FastAPI:
    """Configura e instancia a aplicação FastAPI."""
    app = FastAPI(
        title="Clinic Analytics API",
        description="API para gestão de pacientes e análise de métricas clínicas.",
        version="1.0.0"
    )

    # Registro de Rotas
    app.include_router(patient_router)

    @app.get("/", tags=["Health Check"])
    async def health_check():
        return {
            "status": "online",
            "layer": "analytics-api",
            "environment": "docker-dev"
        }

    return app

# Instância que será referenciada no Docker Compose (src.main:app)
app = create_app()
app.include_router(analytics_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)