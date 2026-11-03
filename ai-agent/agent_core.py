import os
from google import genai
from dotenv import load_dotenv

# Carrega o .env forçando o caminho absoluto
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path=env_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY or GEMINI_API_KEY == "sua_chave_aqui":
    print("AVISO: Chave da API não configurada no .env!")

# Inicializa o cliente do novo SDK
client = genai.Client(api_key=GEMINI_API_KEY)

def get_onboarding_response(user_message: str) -> str:
    """Função central do agente com RAG simplificado (Manual da Empresa)."""
    
    system_context = """
    Você é o 'Guia DevOnboard', o assistente virtual de onboarding da empresa DevOnboard. 
    O jogador é um novo funcionário (humano) recém-contratado. Seja corporativo, profissional e prestativo.
    
    MANUAL DA EMPRESA (Use APENAS estas informações para guiar o jogador):
    1. Missão 1: O jogador deve primeiro retirar o crachá de acesso na Recepção.
    2. Missão 2: A regra de segurança digital da empresa é: "Nunca cole senhas em post-its no monitor".
    3. Missão 3: A sala da equipe fica no final do corredor principal, à direita.
    
    Regra estrita: Não invente andares, salas ou regras que não estejam neste manual.
    """
    
    prompt = f"{system_context}\n\nMensagem do funcionário: '{user_message}'\nResposta do assistente:"
    
    try:
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"\n[AVISO] API real indisponível ({e}). A usar MOCK...\n")
        return "Os sistemas estão instáveis, mas a regra é clara: vá à recepção pegar seu crachá para começarmos o seu onboarding."

if __name__ == "__main__":
    print("A testar o agente isoladamente...")
    resposta = get_onboarding_response("Onde fica minha sala?")
    print(f"Assistente: {resposta}")