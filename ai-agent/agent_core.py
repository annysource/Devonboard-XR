import os
from google import genai
from dotenv import load_dotenv

# Carrega o .env forçando o caminho absoluto da pasta ai-agent
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path=env_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY or GEMINI_API_KEY == "sua_chave_aqui":
    print("AVISO: Chave da API do Gemini não configurada no .env!")

# Inicializa o cliente do novo SDK
client = genai.Client(api_key=GEMINI_API_KEY)

def get_onboarding_response(user_message: str) -> str:
    """Função central do agente para processar o onboarding, com fallback para 503."""
    prompt = f"Você é o assistente de onboarding de uma empresa. O novo funcionário é um galo. Responda de forma corporativa e receptiva à mensagem: '{user_message}'"
    
    try:
        # Tenta a chamada real à API
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        # Se der erro 503 ou qualquer outro, usamos o Mock para não atrasar o projeto
        print(f"\n[AVISO] API real indisponível ({e}). A usar MOCK...\n")
        return "Bem-vindo à nossa empresa, Sr. Galo! Sou o seu assistente de onboarding. Registámos a sua entrada no edifício. Por favor, dirija-se à receção para levantar o seu crachá e iniciar a sua jornada connosco."

# Bloco de teste
if __name__ == "__main__":
    print("A testar o agente isoladamente...")
    resposta = get_onboarding_response("Olá, acabei de chegar no prédio.")
    print(f"Assistente: {resposta}")