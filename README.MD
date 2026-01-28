# 🖨️ Bartender Web - Sistema de Automação de Etiquetas

![Status do Projeto](https://img.shields.io/badge/Status-Finalizado-brightgreen)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

> Uma solução Full Stack para gerenciamento e impressão de etiquetas em impressoras Zebra, com interface moderna e feedback em tempo real.

---

## 📸 Screenshots

### Dashboard (Dark Mode 🌑 & Light Mode ☀️)
<div style="display: flex; gap: 10px;">
  <img src="./assets/print-dark.png" alt="Modo Escuro" width="48%">
  <img src="./assets/print-light.png" alt="Modo Claro" width="48%">
</div>

---

## 🚀 Sobre o Projeto

O **Bartender Web** nasceu da necessidade de otimizar o processo de etiquetagem em ambiente industrial/logístico. Antes dependente de processos manuais ou softwares legados, a nova versão traz uma experiência web rápida, responsiva e integrada.

O sistema permite buscar lotes de produtos, visualizar prévias das etiquetas em tempo real e enviar comandos de impressão ZPL diretamente para impressoras térmicas conectadas ao servidor.

### ✨ Principais Funcionalidades

* **Interface Moderna:** UI limpa e responsiva construída com **React** e **Tailwind CSS**.
* **Temas Dinâmicos:** Suporte completo a **Dark Mode** com persistência de preferência do usuário.
* **Feedback Real:** Status do sistema e notificações (Toasts) para cada ação.
* **Múltiplos Modelos:** Suporte para etiquetas 67x26, 40x20 e 25x10.
* **Produtividade:** Busca por lotes múltiplos e persistência de contadores de produção diária.
* **Arquitetura Desacoplada:** Frontend (Vercel) separado do Backend (Render).

---

## 🛠️ Tecnologias Utilizadas

### Frontend
* **React.js (Vite):** Para uma aplicação SPA rápida e otimizada.
* **Tailwind CSS:** Para estilização utilitária e design responsivo.
* **Local Storage API:** Para persistir configurações do usuário (tema, modelo favorito).

### Backend
* **Python 3:** Linguagem base.
* **Flask:** Microframework para criar a API REST.
* **ZPL (Zebra Programming Language):** Geração dinâmica de códigos de impressão.
* **Gunicorn:** Servidor WSGI para produção.

### Infraestrutura & Deploy
* **Vercel:** Hospedagem do Frontend.
* **Render:** Hospedagem da API Python.
* **CI/CD:** Deploy automático via GitHub Actions (nativo das plataformas).

---


