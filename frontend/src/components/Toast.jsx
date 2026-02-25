/**
 * Componente: Toast
 * * É a notificação flutuante de feedback para o usuário.
 * * O QUE ELE FAZ:
 * 1. Exibe uma mensagem rápida na tela (sucesso ou erro).
 * 2. Muda a cor de fundo baseado no tipo (verde para sucesso, vermelho para erro).
 * 3. Possui uma animação (bounce) para chamar a atenção.
 * * OBSERVAÇÃO: A lógica de tempo (desaparecer após 3 segundos) fica no hook principal, 
 * este componente apenas cuida do visual enquanto está na tela.
 */

import React from "react";

export function Toast({ msg, tipo = "success" }) {
  if (!msg) return null;

  return (
    <div
      className={`fixed top-5 right-5 z-50 px-4 py-3 rounded shadow-lg text-white text-sm font-bold flex items-center gap-2 animate-bounce ${
        tipo === "error" ? "bg-red-600" : "bg-emerald-600"
      }`}
    >
      {/* Ícone */}
      {tipo === "success" ? (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
        </svg>
      ) : (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      )}
      {msg}
    </div>
  );
}