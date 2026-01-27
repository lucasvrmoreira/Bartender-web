## Arquitetura do Frontend (React + Vite)

## MAIN.JSX
Este diretório contém o código-fonte compilado da aplicação. A estrutura segue o padrão de **Separation of Concerns (SoC)**, dividindo responsabilidades entre lógica de negócio, interface de usuário e estilização.

### Arquivos Principais:
- **`main.jsx` (Entry Point):** Responsável pelo **Bootstrapping** da aplicação. Injeta a árvore de componentes React no DOM do navegador (`div#root`) e configura wrappers globais (StrictMode).
- **`App.jsx` (Root Component):** Atua como o **Orquestrador de Estado Global**. Implementa a lógica de *Conditional Rendering* para verificar a disponibilidade do Backend (Health Check) antes de montar a árvore de componentes da aplicação principal.




## src/pages/
Este diretório contém os **Container Components** (ou Smart Components). Estes arquivos são responsáveis por:

1.  **Gerenciamento de Estado (State Management):** Controlam os dados locais (`useState`) e o ciclo de vida da página (`useEffect`).
2.  **Integração com API:** Executam as chamadas HTTP (Fetch) para o Backend e tratam as Promises.
3.  **Lógica de Negócio:** Processam os dados brutos antes de passá-los para os componentes visuais.

### Componentes:
- **`Home.jsx`:** View principal. Gerencia o fluxo de busca, a tabela de resultados e o disparo de requisições de impressão para a API.
- **`Etiqueta.jsx`:** Sub-view focada na renderização visual dos dados da etiqueta. Atua como um componente puro de visualização.





## src/components/
## Componentes de UI (Presentational Components)
Este diretório armazena componentes reutilizáveis e isolados, focados exclusivamente na **Interface de Usuário**.

### Características Técnicas:
- **Stateless (preferencialmente):** Não mantêm estados complexos de negócio.
- **Props-driven:** Todo o conteúdo e comportamento é recebido via `props` do componente pai.
- **Isolamento:** Podem ser reutilizados em diferentes contextos da aplicação sem causar efeitos colaterais.

### Componentes:
- **`SalaDeEspera.jsx`:** Componente de **Guarda (Guard)**. Implementa um mecanismo de *Polling* para verificar o status do servidor ("ping") e impedir a renderização da aplicação enquanto o backend estiver em estado de hibernação (Cold Start).




## src/styles/
## Camada de Estilização (Global & Scoped CSS)
Diretório responsável pela definição visual e design system da aplicação.

- **`index.css`:** Define o **Global Reset**, tipografia base, variáveis de cores e layout estrutural do container `#root`. Aplica correções de *viewport* necessárias para o SPA (Single Page Application).
- **`etiqueta.css`:** Estilização de escopo específico para o componente de etiqueta. Segue regras estritas de dimensões para garantir a fidelidade da impressão térmica (ZPL visual preview).



## public/
## Static Assets (Non-bundled)
Diretório para ativos estáticos servidos diretamente pelo servidor web, sem processamento pelo Bundler (Vite/Webpack).

### Conteúdo:
- **`manifest.json` e `sw.js`:** Configurações para suporte a **PWA (Progressive Web App)**.
- **`favicon.ico` e Ícones:** Recursos gráficos referenciados diretamente pelo `index.html`.
- **`cloud.json`:** Arquivos Lottie/JSON para animações carregadas via *lazy loading* ou runtime.