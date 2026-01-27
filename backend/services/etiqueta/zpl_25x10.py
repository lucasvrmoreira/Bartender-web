from backend.utils.texto import ajustar_descricao_duas_linhas

def gerar_zpl_25x10(codigo, descricao, lote, validade):
    largura = 200
    altura = 80
    
    margem_lateral = 10
    fb_width = largura - (margem_lateral * 2)

    # Mantendo tamanhos legíveis (apenas leve ajuste para garantir fluxo)
    h_codigo, w_codigo = 18, 16 # Leve redução para segurança
    h_desc, w_desc     = 16, 14 
    h_lote, w_lote     = 16, 14 

    # Tenta 1 linha, se não der, usa 2
    linhas_desc = ajustar_descricao_duas_linhas(descricao, max_chars_linha=22)
    
    gap = 0 # Gap zero para colar as linhas e caber tudo

    # Se a descrição tiver 2 linhas, compacta um pouco as fontes
    if len(linhas_desc) > 1:
        h_codigo, w_codigo = 16, 14
        h_desc, w_desc     = 14, 12
        h_lote, w_lote     = 12, 10
    
    # --- CÁLCULO DE POSIÇÃO ---
    altura_texto = h_codigo + (len(linhas_desc) * h_desc) + h_lote + h_lote + (3 * gap)
    
    # Aqui está o segredo:
    # Antes centralizávamos matematicamente: (altura - altura_texto) // 2
    # Agora vamos forçar o texto a descer.
    
    y = (altura - altura_texto) // 2
    
    # CORREÇÃO: Força o início a ser pelo menos no pixel 12 ou 15
    # Se o cálculo matemático mandar começar no 0 ou 5, ignoramos e usamos 15.
    margem_seguranca_topo = 15 
    
    if y < margem_seguranca_topo:
        y = margem_seguranca_topo

    zpl = "^XA\n"
    zpl += "^CI28\n"
    zpl += f"^PW{largura}\n"
    zpl += f"^LL{altura}\n"
    zpl += "^MNW\n"
    zpl += "^LS0\n"
    
    # ^LT (Label Top): Comando global para empurrar a impressão.
    # Se ainda cortar, aumente este valor (ex: ^LT10, ^LT15)
    zpl += "^LT8\n" 

    # --- 1. CÓDIGO ---
    zpl += (
        f"^FO{margem_lateral},{y}"
        f"^A0N,{h_codigo},{w_codigo}"
        f"^FB{fb_width},1,0,C,0"
        f"^FD{codigo}^FS\n"
    )
    y += h_codigo + gap

    # --- 2. DESCRIÇÃO ---
    for linha in linhas_desc:
        zpl += (
            f"^FO{margem_lateral},{y}"
            f"^A0N,{h_desc},{w_desc}"
            f"^FB{fb_width},1,0,C,0"
            f"^FD{linha}^FS\n"
        )
        y += h_desc + gap

    # --- 3. LOTE ---
    zpl += (
        f"^FO{margem_lateral},{y}"
        f"^A0N,{h_lote},{w_lote}"
        f"^FB{fb_width},1,0,C,0"
        f"^FDLote: {lote}^FS\n"
    )
    y += h_lote + gap

    # --- 4. VALIDADE ---
    zpl += (
        f"^FO{margem_lateral},{y}"
        f"^A0N,{h_lote},{w_lote}"
        f"^FB{fb_width},1,0,C,0"
        f"^FDVal: {validade}^FS\n"
    )

    zpl += "^XZ"
    return zpl