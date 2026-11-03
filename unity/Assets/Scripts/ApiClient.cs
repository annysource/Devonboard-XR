using System;
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class ApiClient : MonoBehaviour
{
    private string apiUrl = "http://127.0.0.1:8000";
    public PlayerGuiaUI playerGuia; // Referência para a UI flutuante

    void Start()
    {
        StartCoroutine(CheckHealth());
        StartCoroutine(SendChatMessage("Onde fica a minha sala?"));
    }

    IEnumerator CheckHealth()
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get(apiUrl + "/health"))
        {
            yield return webRequest.SendWebRequest();
            if (webRequest.result != UnityWebRequest.Result.Success)
                Debug.LogError("Erro: " + webRequest.error);
        }
    }

    // Novo método público para ser chamado pelos Triggers
    public void EnviarMensagemParaIA(string mensagem)
    {
        StartCoroutine(SendChatMessage(mensagem));
    }

    IEnumerator SendChatMessage(string userMessage)
    {
        string jsonBody = JsonUtility.ToJson(new ChatPayload { message = userMessage });

        using (UnityWebRequest webRequest = new UnityWebRequest(apiUrl + "/onboarding/chat", "POST"))
        {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonBody);
            webRequest.uploadHandler = new UploadHandlerRaw(bodyRaw);
            webRequest.downloadHandler = new DownloadHandlerBuffer();
            webRequest.SetRequestHeader("Content-Type", "application/json");

            yield return webRequest.SendWebRequest();

            if (webRequest.result == UnityWebRequest.Result.Success)
            {
                // Extrai apenas o texto da resposta ignorando as chaves do JSON
                ChatResponse jsonResponse = JsonUtility.FromJson<ChatResponse>(webRequest.downloadHandler.text);

                if (playerGuia != null)
                {
                    playerGuia.ExibirFala(jsonResponse.response);
                }
            }
        }
    }
}

[Serializable]
public class ChatPayload
{
    public string message;
}

// Nova classe para mapear a resposta do FastAPI: {"response": "texto..."}
[Serializable]
public class ChatResponse
{
    public string response;
}