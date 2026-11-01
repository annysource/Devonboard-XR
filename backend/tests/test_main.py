from fastapi.testclient import TestClient
from main import app

# Cria um cliente de teste que simula pedidos HTTP à nossa API sem precisar do servidor ligado
client = TestClient(app)

def test_health_check():
    """Testa se o endpoint de health responde com sucesso."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "API DevOnboard XR operante."}

def test_start_onboarding():
    """Testa se o endpoint de início do onboarding funciona."""
    response = client.post("/onboarding/start")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "started"
    assert data["step"] == "entrada_predio"

def test_get_progress():
    """Testa se o endpoint de progresso devolve o estado atual."""
    response = client.get("/onboarding/progress")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "in_progress"
    assert data["current_step"] == "entrada_predio"

def test_register_event():
    """Testa o registo de eventos de telemetria."""
    response = client.post("/events", json={"event_name": "player_enter", "event_data": {"x": 0, "y": 0}})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["registered_event"] == "player_enter"