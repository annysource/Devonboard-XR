using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class ApiClient : MonoBehaviour
{
    private string apiUrl = "http://127.0.0.1:8000";

    void Start()
    {
        // Testa a ligação ao backend assim que o jogo/cena inicia
        StartCoroutine(CheckHealth());
    }

    IEnumerator CheckHealth()
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get(apiUrl + "/health"))
        {
            // Envia o pedido HTTP GET
            yield return webRequest.SendWebRequest();

            if (webRequest.result == UnityWebRequest.Result.ConnectionError || webRequest.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.LogError("Erro ao contactar a API: " + webRequest.error);
            }
            else
            {
                Debug.Log("Sucesso na ligação com o Backend! Resposta: " + webRequest.downloadHandler.text);
            }
        }
    }
}