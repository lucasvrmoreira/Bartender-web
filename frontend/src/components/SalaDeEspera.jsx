// src/components/SalaDeEspera.jsx
import React, { useEffect, useState } from "react"; // 👈 Importação essencial

export function SalaDeEspera({ onServerAwake }) {
  const [mensagem, setMensagem] = useState("Acordando a aplicação...");
  const [corMensagem, setCorMensagem] = useState("#666");

  // Pega a URL do Render que configuramos no .env
  const API_URL = import.meta.env.VITE_API_URL || "";
  const isDev = import.meta.env.DEV;

  useEffect(() => {
    // No seu PC, ele pula a espera para facilitar seu trabalho
    if (isDev) {
      console.log("Modo Desenvolvimento: Pulando sala de espera...");
      onServerAwake();
      return;
    }

    const checarServidor = async () => {
      try {
        console.log("Pingando servidor no Render...");
        // Usamos a URL completa para acordar o backend correto
        await fetch(`${API_URL}/api/itens`);

        setCorMensagem("green");
        setMensagem("Servidor Online! Iniciando...");

        setTimeout(() => {
          onServerAwake();
        }, 1500);
      } catch (error) {
        console.warn("Servidor dormindo... tentando de novo.");
        setTimeout(checarServidor, 2000);
      }
    };

    checarServidor();
  }, [onServerAwake, isDev, API_URL]);

  return (
    <div style={styles.container}>
      {/* Aqui usamos o seu arquivo local da pasta public */}
      <dotlottie-player
        src="/cloud.json"
        background="transparent"
        speed="1"
        style={{ width: "350px", height: "350px" }}
        loop="true" // 👈 Use aspas em vez de chaves
        autoplay="true" // 👈 Use aspas em vez de chaves
      ></dotlottie-player>

      <h2 style={styles.title}>Conectando ao Servidor...</h2>
      <p style={{ ...styles.msg, color: corMensagem }}>{mensagem}</p>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    background: "#ffffff",
    fontFamily: '"Segoe UI", sans-serif',
    textAlign: "center",
  },
  title: {
    marginTop: "-30px",
    color: "#333",
    fontWeight: "600",
  },
  msg: {
    fontSize: "14px",
    marginTop: "5px",
    transition: "color 0.3s",
  },
};
