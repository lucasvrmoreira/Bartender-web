/**
 * Componente: Header
 * * É a barra superior (cabeçalho) visual da aplicação.
 * * O QUE ELE FAZ:
 * 1. Mostra o logotipo e o nome do sistema.
 * 2. Exibe o contador de etiquetas impressas no dia.
 * 3. Mostra o indicador visual de "Sistema Online".
 * 4. Renderiza o botão de alternar o Modo Escuro (Dark Mode).
 * * OBSERVAÇÃO: É um componente "burro" (Apresentacional). Ele não calcula nada, apenas recebe os dados e funções via "props" e desenha na tela.
 */

import React from "react";

export function Header({ contadorHoje, darkMode, toggleDarkMode }) {
  return (
    <header className="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 sticky top-0 z-20 h-16 shadow-sm transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 h-full flex items-center justify-between">
        
        {/* LOGO E TÍTULO */}
        <div className="flex items-center gap-2">
          <div className="bg-indigo-600 text-white p-1.5 rounded-lg">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2.5}
              stroke="currentColor"
              className="w-5 h-5"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M9.568 3H5.25A2.25 2.25 0 0 0 3 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 0 0 5.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 0 0 9.568 3Z"
              />
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 6h.008v.008H6V6Z" />
            </svg>
          </div>
          <h1 className="font-bold text-lg text-slate-800 dark:text-white tracking-tight hidden sm:block">
            Bartender<span className="text-indigo-500">Web</span>
          </h1>
        </div>

        {/* CONTROLES DA DIREITA */}
        <div className="flex items-center gap-3 sm:gap-6">
          
          {/* CONTADOR DE IMPRESSÕES */}
          <div className="flex flex-col items-end mr-2">
            <span className="text-[10px] font-bold text-slate-400 uppercase leading-none">
              Impressas
            </span>
            <span className="text-lg font-bold text-indigo-600 dark:text-indigo-400 leading-none">
              {contadorHoje}
            </span>
          </div>

          {/* STATUS ONLINE */}
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-700 bg-emerald-50 dark:bg-emerald-900/30 dark:text-emerald-400 px-3 py-1.5 rounded-full border border-emerald-100 dark:border-emerald-800 shadow-sm">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
            </span>
            <span className="hidden sm:inline">Sistema Online</span>
            <span className="sm:hidden">ON</span>
          </div>

          <div className="h-8 w-px bg-slate-200 dark:bg-slate-700"></div>

          {/* BOTÃO DARK MODE */}
          <button
            onClick={toggleDarkMode}
            className="p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500 dark:text-slate-400 transition-colors"
          >
            {darkMode ? (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
              </svg>
            )}
          </button>
        </div>

      </div>
    </header>
  );
}