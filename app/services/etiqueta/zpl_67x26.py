from app.utils.texto import (
    quebrar_texto,
    normalizar_descricao_para_etiqueta,
    abreviar_termos_tecnicos 
)

def gerar_zpl(codigo, descricao, lote, validade):
    # Definições físicas da etiqueta (67mm x 26mm)
    largura = 536   
    altura = 208    
    margem = 20
    fb_desc = largura - (margem * 2)

    # 1. TRATAMENTO DINÂMICO DO TEXTO
    # Primeiro aplicamos as abreviações (como 1000 ML -> 1L)
    desc_abreviada = abreviar_termos_tecnicos(descricao)
    
    # Normalizamos a descrição
    desc_tratada = normalizar_descricao_para_etiqueta(desc_abreviada, limite=90)
    
    # Reduzimos o max_chars para 25 para forçar a quebra mais cedo em textos como "MYCOALERT"
    # Isso ajuda o sistema a decidir por uma fonte menor antes de sobrepor
    linhas_desc = quebrar_texto(desc_tratada, max_chars=32)
    linhas_desc = linhas_desc[:3] 
    num_linhas = len(linhas_desc)
    total_chars = len(desc_tratada)

    # 2. DEFINIÇÃO DINÂMICA DE FONTES (Lógica de Redução)
    h_codigo = 45
    esp_codigo = 50

    # Se o texto for longo (mais de 25 chars) ou tiver muitas linhas, diminuímos a fonte
    if total_chars > 25 or num_linhas >= 3:
        h_desc, w_desc, esp_desc = 22,28, 34 # Fonte pequena/média para segurança
    elif total_chars > 15 or num_linhas == 2:
        h_desc, w_desc, esp_desc = 28, 32, 38 # Fonte média
    else:
        h_desc, w_desc, esp_desc = 34, 38, 44 # Fonte grande para textos curtos

    # Tamanho do Lote e Validade (Aumentados conforme solicitado)
    h_info = 28
    esp_info = 30

    # 3. CÁLCULO DE POSICIONAMENTO VERTICAL (CURSOR Y)
    # Calculamos a altura total para centralizar o bloco
    altura_total_bloco = esp_codigo + (num_linhas * esp_desc) + (esp_info * 2)
    y = (altura - altura_total_bloco) // 2
    
    # Margem de segurança no topo
    if y < 15: 
        y = 15 

    # 4. MONTAGEM DO COMANDO ZPL
    zpl = "^XA\n"
    zpl += f"^PW{largura}\n"
    zpl += f"^LL{altura}\n"
    zpl += "^CI28\n"

    # Código do Produto (Largura ajustada para parecer negrito)
    zpl += f"^FO{margem},{y}^A0N,{h_codigo},{h_codigo+2}^FB{fb_desc},1,0,C,0^FD{codigo}^FS\n"
    y += esp_codigo

    # Descrição - Imprime linha por linha com o tamanho calculado
    for linha in linhas_desc:
        zpl += f"^FO{margem},{y}^A0N,{h_desc},{w_desc}^FB{fb_desc},1,0,C,0^FD{linha}^FS\n"
        y += esp_desc

    # Informações de Lote e Validade (Maiores e com "negrito")
    y += 4 # Pequeno respiro
    zpl += f"^FO{margem},{y}^A0N,{h_info},{h_info+4}^FB{fb_desc},1,0,C,0^FDLote: {lote}^FS\n"
    y += esp_info
    zpl += f"^FO{margem},{y}^A0N,{h_info},{h_info+4}^FB{fb_desc},1,0,C,0^FDValidade: {validade}^FS\n"

    zpl += "^XZ"
    return zpl