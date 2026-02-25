/**
 * Hook: useBartenderLogic
 * * É o "cérebro" da tela Home. 
 * Ele guarda os dados (estados) e contém as funções que conversam com a API (buscar, imprimir).
 */
import { useState, useEffect } from "react";

export function useBartenderLogic() {
  // --- VARIÁVEIS DE AMBIENTE ---
  const API_URL = import.meta.env.VITE_API_URL || "";

  // --- ESTADOS ---
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem("theme") === "dark");
  const [modelo, setModelo] = useState(() => localStorage.getItem("modelo") || "67x26");
  const [inputLote, setInputLote] = useState("");
  const [resultados, setResultados] = useState([]);
  const [itemSelecionado, setItemSelecionado] = useState(null);
  const [qtd, setQtd] = useState(1);
  const [contadorHoje, setContadorHoje] = useState(0);
  const [imprimirQr, setImprimirQr] = useState(false);
  const [loadingBusca, setLoadingBusca] = useState(false);
  const [loadingPrint, setLoadingPrint] = useState(false);
  const [toast, setToast] = useState(null);

  // --- EFEITOS ---
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  }, [darkMode]);

  useEffect(() => {
    localStorage.setItem("modelo", modelo);
  }, [modelo]);

  // --- LÓGICA E FUNÇÕES ---
  const mostrarToast = (msg, tipo = "success") => {
    setToast({ msg, tipo });
    setTimeout(() => setToast(null), 3000);
  };

  const limparTudo = () => {
    setInputLote("");
    setResultados([]);
    setItemSelecionado(null);
  };

  const getNumerosFormatados = () => {
    const numeros = inputLote
      .split(",")
      .map((n) => n.trim())
      .filter((n) => n.length > 0)
      .map((n) => (n.toUpperCase().startsWith("LIC'") ? n : `LIC'${n}`));
    return numeros.join(",");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      const valor = inputLote.trim();
      if (valor !== "" && !valor.endsWith(",")) {
        setInputLote(valor + ", ");
      }
      buscarDados();
    }
  };

  const buscarDados = async (e) => {
    if (e) e.preventDefault();
    setLoadingBusca(true);
    setItemSelecionado(null);
    setResultados([]);

    try {
      const res = await fetch(`${API_URL}/api/buscar?lotes=${getNumerosFormatados()}`);
      const data = await res.json();

      setResultados(data);

      if (data.length === 0) {
        mostrarToast("Nenhum item encontrado com esse lote!", "error");
      } else if (data.length === 1) {
        setItemSelecionado(data[0]);
      }
    } catch (error) {
      console.error(error);
      mostrarToast("Erro ao buscar dados", "error");
    } finally {
      setLoadingBusca(false);
    }
  };

  const handleImprimir = async () => {
    setLoadingPrint(true);
    try {
      let url = "";

      if (itemSelecionado) {
        url = `${API_URL}/api/imprimir/${itemSelecionado.id}?modelo=${modelo}&qtd=${qtd}&qrcode=${imprimirQr}`;
      } else if (resultados.length > 0) {
        const lotesParaFila = getNumerosFormatados();
        url = `${API_URL}/api/imprimir-fila?numeros=${lotesParaFila}&modelo=${modelo}&qrcode=${imprimirQr}`;
      } else {
        mostrarToast("Nada para imprimir", "error");
        setLoadingPrint(false);
        return;
      }

      const res = await fetch(url);

      if (res.ok) {
        mostrarToast("Enviado com sucesso!", "success");
        setContadorHoje((prev) => prev + (itemSelecionado ? qtd : resultados.length * qtd));
        limparTudo();
      } else {
        mostrarToast("Erro no servidor", "error");
      }
    } catch (error) {
      mostrarToast("Erro de conexão", "error");
    } finally {
      setLoadingPrint(false);
    }
  };

  // --- RETORNO DO HOOK ---
  return {
    state: {
      darkMode, modelo, inputLote, resultados, itemSelecionado, 
      qtd, contadorHoje, imprimirQr, loadingBusca, loadingPrint, toast
    },
    actions: {
      setDarkMode, setModelo, setInputLote, setQtd, setImprimirQr, 
      buscarDados, handleImprimir, limparTudo, handleKeyDown
    }
  };
}