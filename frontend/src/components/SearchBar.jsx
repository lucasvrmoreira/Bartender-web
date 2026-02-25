/**
 * Componente: SearchBar
 * * É o formulário visual de busca de lotes.
 * * O QUE ELE FAZ:
 * 1. Exibe o campo de digitação para os códigos dos lotes.
 * 2. Mostra o prefixo fixo "LIC'" na tela.
 * 3. Renderiza o botão "Buscar", que muda para "..." quando está carregando.
 * * OBSERVAÇÃO: Ele repassa o que foi digitado (inputLote) e os eventos de 
 * clique/teclado (Enter) para as funções que vieram do hook principal.
 */

import React from "react";

export function SearchBar({ 
  inputLote, 
  setInputLote, 
  handleKeyDown, 
  buscarDados, 
  loadingBusca 
}) {
  return (
    <section className="w-full">
      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm p-1 border border-slate-200 dark:border-slate-700 flex items-center focus-within:ring-2 focus-within:ring-indigo-500/50 transition-all">
        <form
          onSubmit={buscarDados}
          className="flex-1 flex items-center h-14"
        >
          {/* ÍCONE DE LUPA */}
          <div className="pl-5 pr-3 text-slate-400">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          
          <div className="h-8 w-px bg-slate-200 dark:bg-slate-700 mx-2"></div>
          
          {/* PREFIXO FIXO */}
          <span className="text-slate-500 dark:text-slate-400 font-bold bg-slate-100 dark:bg-slate-700 px-3 py-1.5 rounded text-xs mr-3">
            LIC'
          </span>
          
          {/* CAMPO DE DIGITAÇÃO */}
          <input
            type="text"
            value={inputLote}
            onChange={(e) => setInputLote(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Digite os lotes e tecle Enter..."
            className="flex-1 bg-transparent outline-none font-medium text-lg text-slate-900 dark:text-white placeholder:text-slate-300 dark:placeholder:text-slate-600"
            autoFocus
          />
          
          {/* BOTÃO DE BUSCA */}
          <button
            type="submit"
            disabled={loadingBusca}
            className="bg-slate-900 dark:bg-indigo-600 hover:bg-black dark:hover:bg-indigo-700 text-white px-8 h-12 mr-1 rounded-lg font-bold text-sm transition-all"
          >
            {loadingBusca ? "..." : "Buscar"}
          </button>
        </form>
      </div>
    </section>
  );
}