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

function imprimir() {
  if (imprimindo) return; // Previne múltiplos cliques
  imprimindo = true;

  const modelo = el.modelo?.value;
  const qtd = el.qtd?.value || 1;

  // MODO FILA
  if (el.tabela && parseInt(el.tabela.dataset.total) > 1) {
    setBotaoLoading();

    const numeros = getNumerosLimpos();

    fetch(
      `/imprimir-fila?modelo=${modelo}&numeros=${encodeURIComponent(
        numeros,
      )}&qtd=${qtd}`,
    )
      .then(() => {
        toast("Fila enviada para a impressora Zebra");
        limparTudo();
        resetBotao();
        imprimindo = false; // 🔓 libera
      })
      .catch(() => {
        toast("Erro ao imprimir fila", "error");
        resetBotao();
        imprimindo = false; // 🔓 libera
      });

    return;
  }

  // MODO INDIVIDUAL
  if (!itemSelecionado) {
    toast("Nenhum item selecionado", "error");
    imprimindo = false; // 🔓 libera
    return;
  }

  setBotaoLoading();

  fetch(`/imprimir/${itemSelecionado}?modelo=${modelo}&qtd=${qtd}`)
    .then(() => {
      toast("Etiqueta enviada para a impressora Zebra");
      limparTudo();
      resetBotao();
      imprimindo = false; // 🔓 libera
    })
    .catch(() => {
      toast("Erro ao imprimir", "error");
      resetBotao();
      imprimindo = false; // 🔓 libera
    });
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

/* ======================================================
   LOGICA DO LOTTIE (VIGIA DA CLOUD - ZERO FLASH)
====================================================== */

async function verificarConexaoCloud() {
  const overlay = document.getElementById("loadingOverlay");
  if (!overlay) return;

  console.log("Verificando saúde da aplicação...");

  // 1. O "Timer de Graça":
  // Agendamos para mostrar o overlay apenas se a conexão demorar mais de 500ms.
  // Se o servidor responder rápido, cancelaremos esse timer antes dele disparar.
  const timerLoading = setTimeout(() => {
    overlay.classList.remove("hidden");
    overlay.classList.add("visible");
    console.log("Demorou um pouco... exibindo nuvem de carregamento.");
  }, 500);

  let servidorPronto = false;

  // Tenta conectar por no máximo 15 tentativas (aprox 30s)
  for (let i = 0; i < 15; i++) {
    try {
      // Usamos um endpoint leve apenas para ver se o servidor responde
      const response = await fetch("/api/importar-item");

      // Se a resposta NÃO for erro de Gateway (502/504), o Render/Neon já acordou!
      if (response.status !== 502 && response.status !== 504) {
        console.log("Servidor detectado e operante!");
        servidorPronto = true;
        break; // Sai do loop imediatamente
      }
    } catch (error) {
      console.log(`Tentativa ${i + 1}: Servidor ainda iniciando...`);
    }

    // Se falhou, espera 2 segundos antes de tentar de novo
    // (Enquanto isso, se passar de 500ms total, a nuvem vai aparecer sozinha via timer)
    await new Promise((r) => setTimeout(r, 2000));
  }

  // 2. Limpeza Final:
  // IMPORTANTE: Cancelamos o timer. Se a conexão foi rápida (ex: 200ms),
  // o timer nunca chegou a rodar, e o usuário NUNCA viu a nuvem.
  clearTimeout(timerLoading);

  // Garante que o overlay suma (ou continue escondido)
  overlay.classList.remove("visible");
  overlay.classList.add("hidden");

  // Opcional: Remove do DOM após a transição do CSS terminar (limpeza total)
  setTimeout(() => {
    // overlay.style.display = 'none'; // Se quiser remover totalmente
  }, 500);
}

// Chame a função apenas UMA VEZ no final do arquivo
verificarConexaoCloud();
