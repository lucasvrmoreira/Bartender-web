// src/components/SalaDeEspera.jsx
import React, { useEffect, useState } from 'react';

export function SalaDeEspera({ onServerAwake }) {
  const [mensagem, setMensagem] = useState("Acordando a aplicação...");
  const [corMensagem, setCorMensagem] = useState("#666");

  // Detecta se estamos rodando localmente (Vite oferece essa variável)
  const isDev = import.meta.env.DEV; 

  useEffect(() => {
    // Se for desenvolvimento (localhost), pula a checagem chata
    if (isDev) {
      console.log("Modo Desenvolvimento: Pulando sala de espera...");
      onServerAwake(); // Avisa o App que pode abrir
      return;
    }

    const checarServidor = async () => {
      try {
        console.log("Pingando servidor...");
        // Tenta bater na API (usamos /api/itens pois é uma rota leve)
        await fetch('/api/itens'); 
        
        // SUCESSO!
        setCorMensagem("green");
        setMensagem("Servidor Online! Iniciando...");
        
        setTimeout(() => {
          onServerAwake(); // Libera o acesso ao App
        }, 1500);

      } catch (error) {
        console.warn("Servidor dormindo... tentando de novo em 2s.");
        setTimeout(checarServidor, 2000); // Tenta de novo
      }
    };

    checarServidor();
  }, [onServerAwake, isDev]);

  return (
    <div style={styles.container}>
      <dotlottie-player
        rc="https://lottie.host/5a0ea585-6934-43cb-834c-687f8725838d/P52Wv86w0u.json"
        background="transparent"
        speed="1"
        style={{ width: '350px', height: '350px' }}
        loop
        autoplay
      ></dotlottie-player>

      <h2 style={styles.title}>Conectando ao Servidor...</h2>
      <p style={{ ...styles.msg, color: corMensagem }}>{mensagem}</p>
    </div>
  );
}

// Estilos CSS-in-JS simples para este componente
const styles = {
  container: {
    height: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    background: '#ffffff',
    fontFamily: '"Segoe UI", sans-serif',
    textAlign: 'center',
  },
  title: {
    marginTop: '-30px',
    color: '#333',
    fontWeight: '600',
  },
  msg: {
    fontSize: '14px',
    marginTop: '5px',
    transition: 'color 0.3s',
  }
};