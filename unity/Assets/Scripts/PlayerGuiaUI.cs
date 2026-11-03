using UnityEngine;
using TMPro;

public class PlayerGuiaUI : MonoBehaviour
{
    [Header("UI")]
    public TextMeshProUGUI textoDialogo;

    [Header("Movimentação")]
    public Transform cameraJogador;
    public float distancia = 2.0f;
    public float altura = 0.2f;
    public float velocidade = 3.0f;

    void Update()
    {
        if (cameraJogador == null) return;

        // Calcula a posição alvo mantendo a distância na frente da câmera
        Vector3 alvo = cameraJogador.position + (cameraJogador.forward * distancia);
        alvo.y = cameraJogador.position.y + altura; 

        // Move suavemente e olha para o jogador
        transform.position = Vector3.Lerp(transform.position, alvo, Time.deltaTime * velocidade);
        transform.LookAt(cameraJogador);
        transform.Rotate(0, 180, 0); // Evita texto invertido
    }

    public void ExibirFala(string texto)
    {
        if (textoDialogo != null) textoDialogo.text = texto;
    }
    public void AtualizarTexto(string novoTexto)
    {
        if (textoDialogo != null) textoDialogo.text = novoTexto;
    }
}