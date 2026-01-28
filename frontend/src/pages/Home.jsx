// src/pages/Home.jsx
import React, { useState, useEffect } from 'react';
import { Etiqueta } from './Etiqueta';
import '../styles/index.css';

export function Home() {
  // --- ESTADOS ---
  
  // 👇 1. IMPORTANTE: Pegamos o endereço do Render aqui
  const API_URL = import.meta.env.VITE_API_URL || "";

  const [darkMode, setDarkMode] = useState(() => localStorage.getItem('theme') === 'dark');
  const [modelo, setModelo] = useState(() => localStorage.getItem('modelo') || '67x26');
  
  const [inputLote, setInputLote] = useState('');
  const [resultados, setResultados] = useState([]);
  const [itemSelecionado, setItemSelecionado] = useState(null);
  const [qtd, setQtd] = useState(1);
  const [contadorHoje, setContadorHoje] = useState(0); 
  
  const [loadingBusca, setLoadingBusca] = useState(false);
  const [loadingPrint, setLoadingPrint] = useState(false);
  const [toast, setToast] = useState(null);

  // --- EFEITOS ---
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

  useEffect(() => {
    localStorage.setItem('modelo', modelo);
  }, [modelo]);

  // --- LÓGICA ---
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

  const getNumerosFormatados = () => {
    const numeros = inputLote.split(',')
      .map(n => n.trim())
      .filter(n => n.length > 0)
      .map(n => n.toUpperCase().startsWith("LIC'") ? n : `LIC'${n}`);
    return numeros.join(',');
  };

  const buscarDados = async (e) => {
    if (e) e.preventDefault();
    setLoadingBusca(true);
    setItemSelecionado(null);
    setResultados([]);

    try {
      // 👇 2. CORREÇÃO AQUI: Adicionamos ${API_URL} antes do caminho
      const res = await fetch(`${API_URL}/api/buscar?lotes=${getNumerosFormatados()}`);
      const data = await res.json();
      setResultados(data);
      if (data.length === 1) setItemSelecionado(data[0]);
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
        // 👇 3. CORREÇÃO AQUI
        url = `${API_URL}/api/imprimir/${itemSelecionado.id}?modelo=${modelo}&qtd=${qtd}`;
      } else if (resultados.length > 0) {
        // 👇 4. CORREÇÃO AQUI TAMBÉM
        url = `${API_URL}/api/imprimir-fila?numeros=${lotes}&modelo=${modelo}`;
      } else {
        mostrarToast("Nada para imprimir", "error");
        setLoadingPrint(false);
        return;
      }

      const res = await fetch(url);
      
      if (res.ok) {
        mostrarToast("Enviado com sucesso!", "success");
        setContadorHoje(prev => prev + (itemSelecionado ? qtd : resultados.length * qtd));
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

  const limparTudo = () => {
    setInputLote('');
    setResultados([]);
    setItemSelecionado(null);
  };

  const mostrarToast = (msg, tipo = 'success') => {
    setToast({ msg, tipo });
    setTimeout(() => setToast(null), 3000);
  };

  const isModoFila = resultados.length > 1 && !itemSelecionado;
  const textoBotao = loadingPrint ? "..." : isModoFila ? "Imprimir Fila" : "Imprimir na Zebra";

  // --- RENDERIZAÇÃO ---
  return (
    <div className="min-h-screen transition-colors duration-300 bg-slate-50 dark:bg-slate-900 font-sans text-slate-800 dark:text-slate-100 pb-10">
      
      {/* TOAST */}
      {toast && (
        <div className={`fixed top-5 right-5 z-50 px-4 py-3 rounded shadow-lg text-white text-sm font-bold flex items-center gap-2 animate-bounce ${toast.tipo === 'error' ? 'bg-red-600' : 'bg-emerald-600'}`}>
          {toast.msg}
        </div>
      )}

      {/* HEADER NAVBAR (AGORA COM STATUS E CONTADOR) */}
      <header className="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 sticky top-0 z-20 h-16 shadow-sm transition-colors duration-300">
        <div className="max-w-7xl mx-auto px-4 h-full flex items-center justify-between">
          
          {/* ESQUERDA: Logo */}
          <div className="flex items-center gap-2">
            <div className="bg-indigo-600 text-white p-1.5 rounded-lg">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className="w-5 h-5">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9.568 3H5.25A2.25 2.25 0 0 0 3 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 0 0 5.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 0 0 9.568 3Z" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 6h.008v.008H6V6Z" />
              </svg>
            </div>
            <h1 className="font-bold text-lg text-slate-800 dark:text-white tracking-tight hidden sm:block">Bartender<span className="text-indigo-500">Web</span></h1>
          </div>
          
          {/* DIREITA: Métricas e Controles */}
          <div className="flex items-center gap-3 sm:gap-6">
            
            {/* CONTADOR DE IMPRESSÃO (NOVO LOCAL) */}
            <div className="flex flex-col items-end mr-2">
              <span className="text-[10px] font-bold text-slate-400 uppercase leading-none">Impressas</span>
              <span className="text-lg font-bold text-indigo-600 dark:text-indigo-400 leading-none">{contadorHoje}</span>
            </div>

            {/* STATUS UNIFICADO (COM PULSE) */}
            <div className="flex items-center gap-2 text-xs font-bold text-emerald-700 bg-emerald-50 dark:bg-emerald-900/30 dark:text-emerald-400 px-3 py-1.5 rounded-full border border-emerald-100 dark:border-emerald-800 shadow-sm">
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
              </span>
              <span className="hidden sm:inline">Sistema Online</span>
              <span className="sm:hidden">ON</span>
            </div>

            {/* DIVISOR VERTICAL */}
            <div className="h-8 w-px bg-slate-200 dark:bg-slate-700"></div>

            {/* BOTÃO DARK MODE */}
            <button 
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500 dark:text-slate-400 transition-colors"
            >
              {darkMode ? (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg>
              )}
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 mt-8 flex flex-col gap-6">
        
        {/* BARRA DE BUSCA (AGORA É O PRIMEIRO ITEM DA TELA) */}
        <section className="w-full">
           <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm p-1 border border-slate-200 dark:border-slate-700 flex items-center focus-within:ring-2 focus-within:ring-indigo-500/50 transition-all">
              <form onSubmit={buscarDados} className="flex-1 flex items-center h-14">
                <div className="pl-5 pr-3 text-slate-400">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                </div>
                <div className="h-8 w-px bg-slate-200 dark:bg-slate-700 mx-2"></div>
                <span className="text-slate-500 dark:text-slate-400 font-bold text-sm bg-slate-100 dark:bg-slate-700 px-3 py-1.5 rounded text-xs mr-3">LIC'</span>
                <input
                  type="text"
                  value={inputLote}
                  onChange={(e) => setInputLote(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Digite os lotes e tecle Enter..."
                  className="flex-1 bg-transparent outline-none font-medium text-lg text-slate-900 dark:text-white placeholder:text-slate-300 dark:placeholder:text-slate-600"
                  autoFocus
                />
                <button 
                  type="submit" 
                  disabled={loadingBusca}
                  className="bg-slate-900 dark:bg-indigo-600 hover:bg-black dark:hover:bg-indigo-700 text-white px-8 h-12 mr-1 rounded-lg font-bold text-sm transition-all"
                >
                  {loadingBusca ? '...' : 'Buscar'}
                </button>
              </form>
           </div>
        </section>

        {/* GRID PRINCIPAL */}
        <section className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          
          {/* TABELA */}
          <div className="lg:col-span-8 bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 min-h-[400px] flex flex-col">
            <div className="p-5 border-b border-slate-100 dark:border-slate-700 flex justify-between items-center bg-slate-50/50 dark:bg-slate-800/50 rounded-t-xl">
                <h3 className="text-sm font-bold text-slate-600 dark:text-slate-300 uppercase tracking-wide">
                    {resultados.length > 0 ? `Resultados da Busca (${resultados.length})` : 'Lista de Itens'}
                </h3>
            </div>

            <div className="flex-1 overflow-auto">
                {resultados.length === 0 ? (
                    <div className="h-full flex flex-col items-center justify-center text-slate-400 dark:text-slate-600 gap-4 p-12">
                        <div className="p-4 bg-slate-100 dark:bg-slate-700/50 rounded-full">
                           <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                        </div>
                        <span className="text-base font-medium">Use a barra acima para buscar lotes</span>
                    </div>
                ) : (
                    <table className="w-full text-left">
                        <thead className="bg-white dark:bg-slate-800 text-slate-400 sticky top-0 z-10 shadow-sm">
                        <tr>
                            <th className="px-6 py-4 text-[11px] font-bold uppercase tracking-wider bg-white dark:bg-slate-800">Lote</th>
                            <th className="px-6 py-4 text-[11px] font-bold uppercase tracking-wider bg-white dark:bg-slate-800">Código</th>
                            <th className="px-6 py-4 text-[11px] font-bold uppercase tracking-wider bg-white dark:bg-slate-800">Descrição</th>
                            <th className="px-6 py-4 text-right text-[11px] font-bold uppercase tracking-wider bg-white dark:bg-slate-800">Ação</th>
                        </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-50 dark:divide-slate-700">
                        {resultados.map((item) => {
                            const isSelected = itemSelecionado?.id === item.id;
                            return (
                            <tr 
                            key={item.id} 
                            className={`group cursor-pointer transition-all hover:bg-slate-50 dark:hover:bg-slate-700/50 ${isSelected ? 'bg-indigo-50/80 dark:bg-indigo-900/30' : ''}`}
                            onClick={() => setItemSelecionado(item)}
                            >
                            <td className="px-6 py-4 text-sm font-bold text-slate-700 dark:text-slate-200">
                                {item.lote}
                            </td>
                            <td className="px-6 py-4 text-xs text-slate-500 dark:text-slate-400 font-mono">{item.codigo}</td>
                            <td className="px-6 py-4 text-xs text-slate-600 dark:text-slate-300 truncate max-w-[220px]" title={item.descricao}>{item.descricao}</td>
                            <td className="px-6 py-4 text-right">
                                {isSelected ? (
                                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200">
                                      Selecionado
                                    </span>
                                ) : (
                                    <span className="opacity-0 group-hover:opacity-100 text-slate-400 dark:text-slate-500 text-xs font-bold">Selecionar</span>
                                )}
                            </td>
                            </tr>
                        )})}
                        </tbody>
                    </table>
                )}
            </div>
          </div>

          {/* PAINEL DE IMPRESSÃO */}
          <div className="lg:col-span-4 bg-white dark:bg-slate-800 rounded-xl shadow-lg shadow-slate-200/50 dark:shadow-black/20 border border-slate-200 dark:border-slate-700 p-6 lg:sticky lg:top-24 transition-colors">
            
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Painel de Impressão</h3>
              <div className="flex gap-2">
                 {isModoFila && <span className="text-[10px] font-bold bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded">FILA</span>}
                 {itemSelecionado && !isModoFila && <span className="text-[10px] font-bold bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded">ITEM</span>}
              </div>
            </div>

            {/* PREVIEW */}
            <div className="bg-slate-100 dark:bg-slate-900/50 rounded-xl p-4 mb-6 flex justify-center border border-slate-200 dark:border-slate-700 relative overflow-hidden min-h-[160px] items-center">
               <div className="absolute inset-0 opacity-[0.05] dark:opacity-[0.1]" style={{backgroundImage: 'radial-gradient(#64748b 1px, transparent 1px)', backgroundSize: '12px 12px'}}></div>
               
               {itemSelecionado ? (
                 <div className="scale-[0.85] shadow-sm transition-transform hover:scale-[0.9]"> 
                    <Etiqueta dados={itemSelecionado} />
                 </div>
               ) : (
                 <div className="flex flex-col items-center justify-center text-slate-400 dark:text-slate-600 gap-2">
                   <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 opacity-20" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                   <span className="text-xs font-medium">Selecione um item para ver o preview</span>
                 </div>
               )}
            </div>

            {/* CONTROLES */}
            <div className="space-y-5">
              <div className="grid grid-cols-3 gap-4">
                <div className="col-span-2">
                    <label className="text-[10px] font-bold text-slate-400 uppercase mb-1.5 block">Modelo</label>
                    <select 
                    value={modelo} 
                    onChange={(e) => setModelo(e.target.value)} 
                    className="w-full p-2.5 bg-slate-50 dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-lg text-sm font-medium text-slate-700 dark:text-white focus:border-indigo-500 outline-none"
                    >
                    <option value="67x26">Padrão (67×26)</option>
                    <option value="40x20">Reduzida (40×20)</option>
                    <option value="25x10">Mini (25×10)</option>
                    </select>
                </div>
                <div>
                    <label className="text-[10px] font-bold text-slate-400 uppercase mb-1.5 block">Cópias</label>
                    <input 
                    type="number" 
                    min="1" 
                    value={qtd} 
                    onChange={(e) => setQtd(parseInt(e.target.value) || 1)} 
                    className="w-full p-2.5 text-center bg-slate-50 dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-lg text-sm font-bold text-slate-700 dark:text-white focus:border-indigo-500 outline-none"
                    />
                </div>
              </div>

              <div className="pt-4 border-t border-slate-100 dark:border-slate-700 flex gap-3">
                <button 
                    onClick={handleImprimir}
                    disabled={resultados.length === 0 || loadingPrint}
                    className="flex-1 py-3.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl shadow-lg shadow-emerald-200/50 dark:shadow-none transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:shadow-none text-sm"
                >
                    {loadingPrint ? (
                        <span className="animate-pulse">Enviando...</span>
                    ) : (
                        <>
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" /></svg>
                        {textoBotao}
                        </>
                    )}
                </button>
                <button 
                    onClick={limparTudo}
                    disabled={resultados.length === 0}
                    className="px-4 bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 text-slate-400 hover:text-red-500 hover:border-red-200 rounded-xl transition-colors"
                    title="Limpar tela"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                </button>
              </div>
            </div>

          </div>
        </section>
      </main>
    </div>
  );
}