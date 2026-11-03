using UnityEngine;

public class MissionTrigger : MonoBehaviour
{
    [Header("Configuração da Missão")]
    public string mensagemGatilho = "Cheguei na recepção. Qual é o meu primeiro passo?";
    public ApiClient apiClient;
    
    private bool jaAtivado = false;

    void OnTriggerEnter(Collider other)
    {
        // Verifica se quem colidiu foi a câmera/cabeça do jogador ou o corpo (XR Origin)
        if (!jaAtivado && (other.CompareTag("Player") || other.CompareTag("MainCamera")))
        {
            jaAtivado = true;
            Debug.Log("Jogador entrou na área: Disparando mensagem para a IA...");
            
            if (apiClient != null)
            {
                apiClient.EnviarMensagemParaIA(mensagemGatilho);
            }
        }
    }
}