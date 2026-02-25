/**
 * Componente: PrintPanel
 * * É o painel lateral direito de configuração e ação de impressão.
 * * O QUE ELE FAZ:
 * 1. Exibe o Preview da etiqueta (usando o componente Etiqueta) se houver um item selecionado.
 * 2. Disponibiliza os controles de Modelo (tamanho), Cópias (quantidade) e o Toggle do QR Code.
 * 3. Renderiza o botão principal de Imprimir (que muda para modo "Fila" ou "Item único").
 * 4. Renderiza o botão de limpar a tela.
 * * OBSERVAÇÃO: Depende do componente `<Etiqueta />` para renderizar o preview visual.
 */

import React from "react";
// Como movemos este arquivo para a pasta 'components', 
// o caminho para importar a Etiqueta que está em 'pages' ganha um "../"
import { Etiqueta } from "../pages/Etiqueta";

export function PrintPanel({
  itemSelecionado,
  resultados,
  modelo,
  setModelo,
  qtd,
  setQtd,
  imprimirQr,
  setImprimirQr,
  handleImprimir,
  loadingPrint,
  limparTudo,
}) {
  
  // Regras visuais do botão de impressão
  const isModoFila = resultados.length > 1 && !itemSelecionado;
  const textoBotao = loadingPrint
    ? "..."
    : isModoFila
      ? "Imprimir Fila"
      : "Imprimir na Zebra";

  return (
    <div className="lg:col-span-4 bg-white dark:bg-slate-800 rounded-xl shadow-lg shadow-slate-200/50 dark:shadow-black/20 border border-slate-200 dark:border-slate-700 p-6 lg:sticky lg:top-24 transition-colors">
      
      {/* CABEÇALHO DO PAINEL */}
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
          Painel de Impressão
        </h3>
        <div className="flex gap-2">
          {isModoFila && (
            <span className="text-[10px] font-bold bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded">
              FILA
            </span>
          )}
          {itemSelecionado && !isModoFila && (
            <span className="text-[10px] font-bold bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded">
              ITEM
            </span>
          )}
        </div>
      </div>

      {/* ÁREA DE PREVIEW DA ETIQUETA */}
      <div className="bg-slate-100 dark:bg-slate-900/50 rounded-xl p-4 mb-6 flex justify-center border border-slate-200 dark:border-slate-700 relative overflow-hidden min-h-[160px] items-center">
        <div
          className="absolute inset-0 opacity-[0.05] dark:opacity-[0.1]"
          style={{
            backgroundImage: "radial-gradient(#64748b 1px, transparent 1px)",
            backgroundSize: "12px 12px",
          }}
        ></div>

        {itemSelecionado ? (
          <div className="scale-[0.85] shadow-sm transition-transform hover:scale-[0.9]">
            <Etiqueta dados={itemSelecionado} />
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center text-slate-400 dark:text-slate-600 gap-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-10 w-10 opacity-20"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span className="text-xs font-medium">
              Selecione um item para ver o preview
            </span>
          </div>
        )}
      </div>

      {/* CONTROLES (MODELO, QTD, QR CODE) */}
      <div className="space-y-5">
        <div className="grid grid-cols-3 gap-4">
          <div className="col-span-2">
            <label className="text-[10px] font-bold text-slate-400 uppercase mb-1.5 block">
              Modelo
            </label>
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
            <label className="text-[10px] font-bold text-slate-400 uppercase mb-1.5 block">
              Cópias
            </label>
            <input
              type="text"
              inputMode="numeric"
              pattern="[0-9]*"
              value={qtd}
              onChange={(e) => {
                const valor = e.target.value.replace(/\D/g, "");
                setQtd(valor === "" ? "" : parseInt(valor));
              }}
              className="w-full p-2.5 text-center bg-slate-50 dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-lg text-sm font-bold text-slate-700 dark:text-white focus:border-indigo-500 outline-none"
            />
          </div>
        </div>

        {/* TOGGLE QR CODE */}
        <div className="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-700/30 rounded-lg border border-slate-100 dark:border-slate-700/50">
          <div className="flex items-center gap-2">
            <div className="p-1.5 bg-slate-200 dark:bg-slate-600 rounded text-slate-600 dark:text-slate-300">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v1m6 11h2m-6 0h-2v4h2v-4zM6 6h6v6H6V6zm12 0h-6v6h6V6zm-6 12H6v-6h6v6z" />
              </svg>
            </div>
            <span className="text-xs font-bold text-slate-600 dark:text-slate-300">
              Imprimir QR Code?
            </span>
          </div>

          <button
            onClick={() => setImprimirQr(!imprimirQr)}
            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none ${
              imprimirQr ? "bg-indigo-600" : "bg-slate-300 dark:bg-slate-600"
            }`}
          >
            <span
              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                imprimirQr ? "translate-x-6" : "translate-x-1"
              }`}
            />
          </button>
        </div>

        {/* BOTÕES DE AÇÃO */}
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
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                </svg>
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
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>

    </div>
  );
}