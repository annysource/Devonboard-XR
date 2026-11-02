using System;
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class ApiClient : MonoBehaviour
{
    private string apiUrl = "http://127.0.0.1:8000";

    void Start()
    {
        // Testa a ligação e depois envia uma mensagem de teste do galo
        StartCoroutine(CheckHealth());
        StartCoroutine(SendChatMessage("Olá, cheguei ao edifício para o meu onboarding!"));
    }

    IEnumerator CheckHealth()
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get(apiUrl + "/health"))
        {
            yield return webRequest.SendWebRequest();

            if (webRequest.result == UnityWebRequest.Result.ConnectionError || webRequest.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.LogError("Erro ao contactar a API (/health): " + webRequest.error);
            }
            else
            {
                Debug.Log("Health OK: " + webRequest.downloadHandler.text);
            }
        }
    }

    IEnumerator SendChatMessage(string userMessage)
    {
        // Cria o objeto JSON no formato esperado pelo Pydantic (ChatMessage)
        string jsonBody = JsonUtility.ToJson(new ChatPayload { message = userMessage });

        using (UnityWebRequest webRequest = new UnityWebRequest(apiUrl + "/onboarding/chat", "POST"))
        {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonBody);
            webRequest.uploadHandler = new UploadHandlerRaw(bodyRaw);
            webRequest.downloadHandler = new DownloadHandlerBuffer();
            webRequest.SetRequestHeader("Content-Type", "application/json");

            yield return webRequest.SendWebRequest();

            if (webRequest.result == UnityWebRequest.Result.ConnectionError || webRequest.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.LogError("Erro no chat da API: " + webRequest.error);
            }
            else
            {
                Debug.Log("Resposta da IA no Unity: " + webRequest.downloadHandler.text);
            }
        }
    }
}

// Classe auxiliar para serializar o payload do chat
[Serializable]
public class ChatPayload
{
    public string message;
}