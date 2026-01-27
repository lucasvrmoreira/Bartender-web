import React, { useState } from 'react';
import { Home } from './pages/Home';
import { SalaDeEspera } from './components/SalaDeEspera';


// Importa os estilos globais que trouxemos do projeto antigo
import './styles/index.css'; 

function App() {
  // Estado que define se podemos mostrar a tela principal
  const [servidorPronto, setServidorPronto] = useState(false);

  return (
    <div className="app-container">
      {servidorPronto ? (
        // CENÁRIO A: Servidor online. Mostra o sistema completo (Home)
        <Home />
      ) : (
        // CENÁRIO B: Servidor dormindo ou carregando. Mostra a animação da nuvem
        // Quando a SalaDeEspera detectar que o backend voltou, ela avisa aqui
        <SalaDeEspera onServerAwake={() => setServidorPronto(true)} />
      )}
    </div>
  );
}

export default App;