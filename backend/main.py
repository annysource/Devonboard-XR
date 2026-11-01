import os
import sys
import importlib.util
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

# --- Importação dinâmica do módulo agent_core ---
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
agent_path = os.path.join(base_dir, "ai-agent", "agent_core.py")

spec = importlib.util.spec_from_file_location("agent_core", agent_path)
agent_core = importlib.util.module_from_spec(spec)
sys.modules["agent_core"] = agent_core
spec.loader.exec_module(agent_core)
# ------------------------------------------------

app = FastAPI(
    title="DevOnboard XR API",
    description="API para gerir o onboarding do personagem e integração com IA.",
    version="0.1.0"
)

# --- Configuração de Segurança CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos Pydantic (Validação de Dados) ---
class ChatMessage(BaseModel):
    message: str

class GameEvent(BaseModel):
    event_name: str
    event_data: Dict[str, Any] = {}

# --- Endpoints da API ---
@app.get("/health")
def health_check():
    """Verifica se a API está a funcionar corretamente."""
    return {"status": "ok", "message": "API DevOnboard XR operante."}

@app.post("/onboarding/start")
def start_onboarding():
    """Inicia a jornada de onboarding do galo no edifício."""
    return {
        "status": "started",
        "step": "entrada_predio",
        "message": "O onboarding começou. O galo entrou no edifício fictício."
    }

# NOVO: Endpoint para verificar o progresso
@app.get("/onboarding/progress")
def get_progress():
    """Devolve a etapa atual do onboarding."""
    # Futuramente, isto consultará uma base de dados ou a memória do agente
    return {
        "status": "in_progress",
        "current_step": "entrada_predio",
        "progress_percentage": 10
    }

# NOVO: Endpoint para telemetria do Unity
@app.post("/events")
def register_event(event: GameEvent):
    """Recebe eventos do Unity (ex: movimento, interações) para telemetria e observabilidade."""
    # Futuramente, ligaremos isto ao Prometheus/Grafana
    return {"status": "success", "registered_event": event.event_name}

@app.post("/onboarding/chat")
def chat_with_agent(payload: ChatMessage):
    """Recebe a mensagem do frontend/Unity e devolve a resposta da IA."""
    resposta = agent_core.get_onboarding_response(payload.message)
    return {"response": resposta}