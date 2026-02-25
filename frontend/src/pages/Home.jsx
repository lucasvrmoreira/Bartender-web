/**
 * Página: Home
 * * É o contêiner principal da aplicação.
 * * O QUE ELE FAZ:
 * 1. Importa a lógica central através do hook useBartenderLogic.
 * 2. Importa todos os componentes visuais (Header, SearchBar, etc).
 * 3. Distribui os dados (state) e as funções (actions) para cada componente, 
 * montando a tela de forma declarativa e limpa.
 */

// src/pages/Home.jsx
import React from "react";
import { Etiqueta } from "./Etiqueta"; // Mantivemos a Etiqueta na mesma pasta
import { Header } from "../components/Header";
import { SearchBar } from "../components/SearchBar";
import { ResultsTable } from "../components/ResultsTable";
import { PrintPanel } from "../components/PrintPanel";
import { Toast } from "../components/Toast";
import { useBartenderLogic } from "../hooks/useBartenderLogic";
import "../styles/index.css";

export function Home() {
  // Importando o "Cérebro" da nossa página
  const { state, actions } = useBartenderLogic();

  return (
    <div className="min-h-screen transition-colors duration-300 bg-slate-50 dark:bg-slate-900 font-sans text-slate-800 dark:text-slate-100 pb-10">
      
      {/* ALERTA FLUTUANTE */}
      {state.toast && (
        <Toast msg={state.toast.msg} tipo={state.toast.tipo} />
      )}

      {/* CABEÇALHO */}
      <Header 
        contadorHoje={state.contadorHoje} 
        darkMode={state.darkMode} 
        toggleDarkMode={() => actions.setDarkMode(!state.darkMode)} 
      />

      <main className="max-w-7xl mx-auto px-4 mt-8 flex flex-col gap-6">
        
        {/* BARRA DE BUSCA */}
        <SearchBar 
          inputLote={state.inputLote} 
          setInputLote={actions.setInputLote} 
          buscarDados={actions.buscarDados} 
          handleKeyDown={actions.handleKeyDown}
          loadingBusca={state.loadingBusca} 
        />

        {/* ÁREA DE CONTEÚDO (TABELA + PAINEL DE IMPRESSÃO) */}
        <section className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          
          <ResultsTable 
            resultados={state.resultados} 
            itemSelecionado={state.itemSelecionado} 
            setItemSelecionado={actions.setItemSelecionado} 
          />

          <PrintPanel 
            itemSelecionado={state.itemSelecionado}
            resultados={state.resultados}
            modelo={state.modelo}
            setModelo={actions.setModelo}
            qtd={state.qtd}
            setQtd={actions.setQtd}
            imprimirQr={state.imprimirQr}
            setImprimirQr={actions.setImprimirQr}
            handleImprimir={actions.handleImprimir}
            loadingPrint={state.loadingPrint}
            limparTudo={actions.limparTudo}
          />

        </section>
      </main>
    </div>
  );
}