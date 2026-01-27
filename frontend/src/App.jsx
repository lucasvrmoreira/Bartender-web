import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [itens, setItens] = useState([])
  const [loading, setLoading] = useState(true)

  // Busca os itens do seu banco de dados assim que a página abre
  useEffect(() => {
    fetch('/api/itens')
      .then(res => res.json())
      .then(data => {
        setItens(data)
        setLoading(false)
      })
      .catch(err => console.error("Erro ao carregar dados:", err))
  }, [])

  // Função para disparar a impressão via print.py
  const imprimirEtiqueta = (id) => {
    fetch(`/imprimir/${id}?modelo=67x26&qtd=1`)
      .then(res => {
        if (res.ok) alert("Comando de impressão enviado com sucesso!")
        else alert("Erro ao imprimir. Verifique o Agent.")
      })
  }

  if (loading) return <div>Carregando monitor de estoque...</div>

  return (
    <div className="container">
      <h1>Monitor de Estoque SAP</h1>
      <table className="tabela-estoque">
        <thead>
          <tr>
            <th>Código</th>
            <th>Descrição</th>
            <th>Lote</th>
            <th>Validade</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {itens.map(item => (
            <tr key={item.id}>
              <td>{item.codigo}</td>
              <td>{item.descricao}</td>
              <td>{item.lote}</td>
              <td>{item.validade}</td>
              <td>
                <button onClick={() => imprimirEtiqueta(item.id)}>Imprimir</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default App