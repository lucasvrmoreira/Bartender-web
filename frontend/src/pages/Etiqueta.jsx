// src/pages/Etiqueta.jsx
import React from 'react';
import '../styles/etiqueta.css';

export function Etiqueta({ dados }) {
  if (!dados) return null;

  return (
    <div className="etiqueta-container">
      <div className="etiqueta">
        <div className="codigo">{dados.codigo}</div>
        <div className="descricao">{dados.descricao}</div>
        <div className="info">
          <div><strong>Lote:</strong> {dados.lote}</div>
          <div><strong>Validade:</strong> {dados.validade || '---'}</div>
        </div>
      </div>
    </div>
  );
}