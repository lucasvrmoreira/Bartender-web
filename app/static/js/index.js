/* ======================================================
   CONFIGURAÇÃO 
====================================================== */
const API_URL = "http://localhost:8000";

/* ======================================================
   ESTADO DA APLICAÇÃO
====================================================== */
let itemSelecionado = null;
let imprimindo = false; // 🔒 lock de segurança

/* ======================================================
   ELEMENTOS DA TELA
====================================================== */
const el = {
  inputLote: document.getElementById("inputLote"),
  btnBuscar: document.getElementById("btnBuscar"),
  btnPrint: document.getElementById("btnPrint"),
  btnLimpar: document.getElementById("btnLimpar"),
  tabela: document.getElementById("tabelaResultados"),
  preview: document.getElementById("previewFrame"),
  modelo: document.getElementById("modeloEtiqueta"),
  qtd: document.getElementById("qtdEtiquetas"),
  alert: document.getElementById("alertMensagem"),
  modo: document.getElementById("modoImpressao"),
};

/* ======================================================
   FUNÇÕES DE UI (APENAS TELA)
====================================================== */
function atualizarTextoBotaoBusca() {
  if (!el.inputLote || !el.btnBuscar) return;

  if (el.inputLote.value.includes(",")) {
    el.btnBuscar.textContent = "Buscar vários";
  } else {
    el.btnBuscar.textContent = "Buscar";
  }
}

function limparTudo() {
  if (el.inputLote) el.inputLote.value = "";
  if (el.btnBuscar) el.btnBuscar.textContent = "Buscar";

  if (el.btnPrint) {
    el.btnPrint.disabled = true;
    el.btnPrint.textContent = "🖨 Imprimir na Zebra";
  }

  itemSelecionado = null;

  if (el.tabela) el.tabela.remove();
  if (el.preview) el.preview.src = "";
  if (el.modo) el.modo.classList.add("hidden");
}

function toast(mensagem, tipo = "success") {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const div = document.createElement("div");
  div.className = `toast ${tipo === "error" ? "error" : ""}`;
  div.textContent = mensagem;

  container.appendChild(div);

  setTimeout(() => {
    div.remove();
  }, 3000);
}

function setBotaoLoading() {
  if (!el.btnPrint) return;

  el.btnPrint.disabled = true;
  el.btnPrint.dataset.textoOriginal = el.btnPrint.textContent;
  el.btnPrint.textContent = "⏳ Enviando para a Zebra...";
  el.btnPrint.style.cursor = "wait";
}

function resetBotao() {
  if (!el.btnPrint) return;

  el.btnPrint.disabled = false;
  el.btnPrint.textContent =
    el.btnPrint.dataset.textoOriginal || "🖨 Imprimir na Zebra";
  el.btnPrint.style.cursor = "pointer";
}

function setModoIndividual() {
  if (!el.modo) return;

  el.modo.className = "modo-badge modo-individual";
  el.modo.textContent = "🟢 Modo: Impressão individual";
}

function setModoFila(total) {
  if (!el.modo) return;

  el.modo.className = "modo-badge modo-fila";
  el.modo.textContent = `🔵 Modo: Impressão em fila (${total} itens)`;
}

/* ======================================================
   AÇÕES (BACKEND)
====================================================== */

function getNumerosLimpos() {
  if (!el.inputLote) return "";

  return el.inputLote.value
    .split(",")
    .map((n) => n.trim())
    .filter((n) => n.length > 0)
    .join(",");
}

function getNumerosArray() {
  if (!el.inputLote) return [];
  
  return el.inputLote.value
    .split(",")                 // Separa nas vírgulas
    .map((n) => n.trim())       // Limpa espaços
    .filter((n) => n.length > 0)// Tira vazios
    .map((n) => {
      // A MÁGICA É AQUI:
      // Se o usuário digitou só "3710", a gente vira "LIC'3710"
      // Se ele digitou "LIC'3710", a gente mantém igual.
      return n.toUpperCase().startsWith("LIC'") ? n : `LIC'${n}`;
    });
}
async function imprimir() {
  if (imprimindo) return; 
  imprimindo = true;

  const modelo = el.modelo?.value || "67x26";
  const qtd = parseInt(el.qtd?.value || 1);
  let lotes = [];

  // 1. Identifica quais lotes imprimir
  if (itemSelecionado) {
    // Modo Individual: Pega o lote da tela ou do item clicado
    // Se o itemSelecionado for o ID do banco, podemos usar a rota por ID
    // Mas para simplificar, vamos usar a rota de lote (batch) que serve pra tudo
    
    // Precisamos pegar o texto do lote que está na tela ou input
    // Se você tiver o número do lote no dataset, melhor. 
    // Assumindo que o input tem o lote:
    lotes = getNumerosArray();
  } else {
    // Modo Fila
    lotes = getNumerosArray();
  }

  if (lotes.length === 0) {
    toast("Nenhum lote válido para imprimir", "error");
    imprimindo = false;
    return;
  }

  setBotaoLoading();

  // 2. Monta o JSON (Payload)
  const payload = {
    lotes: lotes,
    modelo: modelo,
    copias: qtd
  };

  try {
    // 3. Faz o POST para o FastAPI
    const response = await fetch(`${API_URL}/print/batch`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
        // Tenta ler o erro que o FastAPI mandou
        const erroJson = await response.json();
        throw new Error(erroJson.detail || "Erro desconhecido");
    }

    const dados = await response.json();
    toast(`Sucesso! ${dados.enviados} etiquetas enviadas.`);
    limparTudo();
    
  } catch (erro) {
    console.error(erro);
    toast(`Erro: ${erro.message}`, "error");
  } finally {
    resetBotao();
    imprimindo = false;
  }
}

/* ======================================================
   EVENTOS
====================================================== */
if (el.inputLote) {
  el.inputLote.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();

      const valor = el.inputLote.value.trim();
      if (valor !== "" && !valor.endsWith(",")) {
        el.inputLote.value = valor + ", ";
      }

      atualizarTextoBotaoBusca();
    }
  });

  el.inputLote.addEventListener("input", atualizarTextoBotaoBusca);
}

if (el.btnPrint) el.btnPrint.onclick = imprimir;
if (el.btnLimpar) el.btnLimpar.onclick = limparTudo;

/* ======================================================
   LÓGICA AUTOMÁTICA PÓS-BUSCA
====================================================== */
if (el.tabela) {
  const total = parseInt(el.tabela.dataset.total);

  // APENAS UM ITEM
  if (total === 1) {
    const linha = el.tabela.querySelector("tbody tr");
    itemSelecionado = linha.dataset.id;

    el.btnPrint.disabled = false;
    el.btnPrint.textContent = "🖨 Imprimir na Zebra";

    setModoIndividual();
  }

  // VÁRIOS ITENS
  if (total > 1) {
    el.btnPrint.disabled = false;
    el.btnPrint.textContent = "🖨 Imprimir fila";
    itemSelecionado = null;

    setModoFila(total);
  }
}

/* ======================================================
   ALERTA AUTOMÁTICO
====================================================== */
if (el.alert) {
  setTimeout(() => {
    el.alert.style.transition = "opacity 0.5s ease";
    el.alert.style.opacity = "0";

    setTimeout(() => {
      el.alert.remove();
    }, 500);
  }, 3000);
}

if (el.inputLote) {
  el.inputLote.addEventListener("input", () => {
    if (el.alert) el.alert.remove();
  });
}

/* =========================================================
   SENSOR DE HIBERNAÇÃO (RENDER -> VERCEL)
   ========================================================= */
(function () {
  // --- CONFIGURAÇÃO ---
  // Coloque aqui o link da sua Vercel
  const URL_SALA_ESPERA = "https://bartender-web-six.vercel.app/";
  const TEMPO_LIMITE = 3000; // 3 segundos

  async function checarServidor() {
    // Se a aba não estiver visível, não faz nada
    if (document.visibilityState !== "visible") return;

    console.log("Voltando para a aba... Checando servidor.");

    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), TEMPO_LIMITE);

    try {
      // Tenta acessar a raiz '/'
      await fetch("/", { signal: controller.signal });
      clearTimeout(id);
      console.log("Servidor acordado!");
    } catch (error) {
      // Se der erro de tempo ou rede
      if (
        error.name === "AbortError" ||
        error.message.includes("NetworkError") ||
        error.message.includes("Failed to fetch")
      ) {
        console.warn("Servidor dormindo. Indo para sala de espera...");

        // Salva a URL atual
        const atual = window.location.pathname + window.location.search;
        // Redireciona
        window.location.href = `${URL_SALA_ESPERA}?returnTo=${encodeURIComponent(atual)}`;
      }
    }
  }

  // Adiciona o ouvinte
  document.addEventListener("visibilitychange", checarServidor);
})();


