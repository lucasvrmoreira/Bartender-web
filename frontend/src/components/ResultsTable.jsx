/**
 * Componente: ResultsTable
 * * É a lista ou tabela visual que exibe os lotes encontrados.
 * * O QUE ELE FAZ:
 * 1. Mostra uma mensagem amigável ("Use a barra acima...") se não houver resultados.
 * 2. Renderiza a tabela com Lote, Código e Descrição quando a busca retorna dados.
 * 3. Permite clicar em uma linha para selecionar um item específico.
 * 4. Destaca visualmente a linha do item que está selecionado.
 * * OBSERVAÇÃO: Recebe a lista de resultados e a função de selecionar item via props.
 */

import React from "react";

export function ResultsTable({ resultados, itemSelecionado, setItemSelecionado }) {
  return (
    <div className="lg:col-span-8 bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 min-h-[400px] flex flex-col">
      {/* CABEÇALHO DA TABELA */}
      <div className="p-5 border-b border-slate-100 dark:border-slate-700 flex justify-between items-center bg-slate-50/50 dark:bg-slate-800/50 rounded-t-xl">
        <h3 className="text-sm font-bold text-slate-600 dark:text-slate-300 uppercase tracking-wide">
          {resultados.length > 0
            ? `Resultados da Busca (${resultados.length})`
            : "Lista de Itens"}
        </h3>
      </div>

      <div className="flex-1 overflow-auto">
        {resultados.length === 0 ? (
          /* ESTADO VAZIO (NENHUM RESULTADO) */
          <div className="h-full flex flex-col items-center justify-center text-slate-400 dark:text-slate-600 gap-4 p-12">
            <div className="p-4 bg-slate-100 dark:bg-slate-700/50 rounded-full">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-8 w-8 opacity-50"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <span className="text-base font-medium">
              Use a barra acima para buscar lotes
            </span>
          </div>
        ) : (
          /* TABELA COM DADOS */
          <table className="w-full text-left">
            <thead className="bg-white dark:bg-slate-800 text-slate-400 sticky top-0 z-10 shadow-sm">
              <tr>
                <th className="px-6 py-4 text-[11px] font-bold uppercase tracking-wider bg-white dark:bg-slate-800">
                  Lote
                </th>
                <th className="px-6 py-4 text-[11px] font-bold uppercase tracking-wider bg-white dark:bg-slate-800">
                  Código
                </th>
                <th className="px-6 py-4 text-[11px] font-bold uppercase tracking-wider bg-white dark:bg-slate-800">
                  Descrição
                </th>
                <th className="px-6 py-4 text-right text-[11px] font-bold uppercase tracking-wider bg-white dark:bg-slate-800">
                  Ação
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-50 dark:divide-slate-700">
              {resultados.map((item) => {
                const isSelected = itemSelecionado?.id === item.id;
                return (
                  <tr
                    key={item.id}
                    className={`group cursor-pointer transition-all hover:bg-slate-50 dark:hover:bg-slate-700/50 ${
                      isSelected ? "bg-indigo-50/80 dark:bg-indigo-900/30" : ""
                    }`}
                    onClick={() => setItemSelecionado(item)}
                  >
                    <td className="px-6 py-4 text-sm font-bold text-slate-700 dark:text-slate-200">
                      {item.lote}
                    </td>
                    <td className="px-6 py-4 text-xs text-slate-500 dark:text-slate-400 font-mono">
                      {item.codigo}
                    </td>
                    <td
                      className="px-6 py-4 text-xs text-slate-600 dark:text-slate-300 truncate max-w-[220px]"
                      title={item.descricao}
                    >
                      {item.descricao}
                    </td>
                    <td className="px-6 py-4 text-right">
                      {isSelected ? (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200">
                          Selecionado
                        </span>
                      ) : (
                        <span className="opacity-0 group-hover:opacity-100 text-slate-400 dark:text-slate-500 text-xs font-bold">
                          Selecionar
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}