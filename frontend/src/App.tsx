import { useState } from 'react'
import './index.css'

function App() {
  const [message, setMessage] = useState('')
  const [chatLog, setChatLog] = useState<{sender: string, text: string}[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!message.trim()) return

    // Atualiza o ecrã com a mensagem do galo
    const newLog = [...chatLog, { sender: 'Galo', text: message }]
    setChatLog(newLog)
    setMessage('')
    setIsLoading(true)

    try {
      // Faz o pedido HTTP à API FastAPI
      const response = await fetch('http://127.0.0.1:8000/onboarding/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      })
      
      if (!response.ok) throw new Error('Falha na comunicação com o servidor')
      
      const data = await response.json()
      
      // Atualiza o ecrã com a resposta do assistente (IA ou Mock)
      setChatLog([...newLog, { sender: 'Assistente', text: data.response }])
    } catch (error) {
      console.error(error)
      setChatLog([...newLog, { sender: 'Sistema', text: 'Erro ao contactar a API. O backend está a correr?' }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: '600px', margin: '40px auto', padding: '20px', fontFamily: 'sans-serif' }}>
      <h2>DevOnboard XR - Painel Web</h2>
      <p style={{ color: '#555' }}>Acompanhamento do Onboarding e Chat com IA</p>
      
      <div style={{ 
        border: '1px solid #ccc', 
        borderRadius: '8px',
        padding: '16px', 
        height: '400px', 
        overflowY: 'auto', 
        marginBottom: '16px',
        backgroundColor: '#fafafa'
      }}>
        {chatLog.length === 0 ? (
          <p style={{ color: '#888', textAlign: 'center', marginTop: '150px' }}>
            Nenhuma mensagem. Escreva algo para começar...
          </p>
        ) : (
          chatLog.map((msg, index) => (
            <div key={index} style={{ 
              marginBottom: '12px', 
              textAlign: msg.sender === 'Galo' ? 'right' : 'left' 
            }}>
              <span style={{ 
                display: 'inline-block', 
                backgroundColor: msg.sender === 'Galo' ? '#007bff' : '#e9ecef', 
                color: msg.sender === 'Galo' ? 'white' : 'black',
                padding: '10px 14px', 
                borderRadius: '16px',
                maxWidth: '80%'
              }}>
                <strong>{msg.sender}: </strong><br/>
                {msg.text}
              </span>
            </div>
          ))
        )}
        {isLoading && <p style={{ color: '#888', fontStyle: 'italic' }}>Assistente a escrever...</p>}
      </div>

      <form onSubmit={sendMessage} style={{ display: 'flex', gap: '10px' }}>
        <input 
          type="text" 
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Olá, sou o galo e cheguei para o onboarding..." 
          style={{ flex: 1, padding: '12px', borderRadius: '4px', border: '1px solid #ccc' }}
          disabled={isLoading}
        />
        <button 
          type="submit" 
          disabled={isLoading || !message.trim()} 
          style={{ padding: '12px 24px', borderRadius: '4px', backgroundColor: '#007bff', color: 'white', border: 'none', cursor: 'pointer' }}
        >
          Enviar
        </button>
      </form>
    </div>
  )
}

export default App