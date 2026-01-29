import unicodedata
from backend.utils.texto import (
    quebrar_texto,
    normalizar_descricao_para_etiqueta,
    abreviar_termos_tecnicos 
)

def tratar_texto_zpl(texto):
    """
    Remove sujeira da nuvem (u00c1 -> Á) e prepara para impressão.
    """
    if not texto: return ""
    texto = str(texto)
    
    # Decodifica caracteres escapados da nuvem
    if "u00" in texto or "\\u" in texto:
        try:
            texto = texto.encode('utf-8').decode('unicode_escape')
        except:
            pass 

    # Mantém acentos e deixa maiúsculo
    return texto.replace("\n", " ").replace("\r", "").strip().upper()

def gerar_zpl(codigo, descricao, lote, validade):
    # Definições físicas da etiqueta (67mm x 26mm)
    largura = 536   
    altura = 208    
    margem = 20
    
    # --- VOLTANDO AO ORIGINAL ---
    # O texto vai ocupar a largura total disponível, ficando perfeitamente centralizado.
    # Se ele for muito longo, vai passar por baixo do QR Code (sobreposição), como você pediu.
    fb_desc = largura - (margem * 2)

    # --- LIMPEZA DOS DADOS ---
    desc_final = tratar_texto_zpl(descricao)
    lote_final = tratar_texto_zpl(lote)
    validade_final = tratar_texto_zpl(validade)
    codigo_final = tratar_texto_zpl(codigo)

    # 1. TRATAMENTO DINÂMICO DO TEXTO
    desc_abreviada = abreviar_termos_tecnicos(desc_final)
    desc_tratada = normalizar_descricao_para_etiqueta(desc_abreviada, limite=90)
    
    linhas_desc = quebrar_texto(desc_tratada, max_chars=32)
    linhas_desc = linhas_desc[:3] 
    num_linhas = len(linhas_desc)
    total_chars = len(desc_tratada)

    # 2. DEFINIÇÃO DINÂMICA DE FONTES
    h_codigo = 45
    esp_codigo = 50

    if total_chars > 25 or num_linhas >= 3:
        h_desc, w_desc, esp_desc = 22,28, 34 
    elif total_chars > 15 or num_linhas == 2:
        h_desc, w_desc, esp_desc = 28, 32, 38 
    else:
        h_desc, w_desc, esp_desc = 34, 38, 44 

    h_info = 28
    esp_info = 30

    # 3. CÁLCULO DE POSICIONAMENTO VERTICAL
    altura_total_bloco = esp_codigo + (num_linhas * esp_desc) + (esp_info * 2)
    y = (altura - altura_total_bloco) // 2
    if y < 15: y = 15 

    # 4. MONTAGEM DO COMANDO ZPL
    zpl = "^XA\n"
    zpl += f"^PW{largura}\n^LL{altura}\n"
    zpl += "^CI28\n" # Aceita acentos

    # Código do Produto
    zpl += f"^FO{margem},{y}^A0N,{h_codigo},{h_codigo+2}^FB{fb_desc},1,0,C,0^FD{codigo_final}^FS\n"
    y += esp_codigo

    # Descrição
    for linha in linhas_desc:
        zpl += f"^FO{margem},{y}^A0N,{h_desc},{w_desc}^FB{fb_desc},1,0,C,0^FD{linha}^FS\n"
        y += esp_desc

    y += 4 # Respiro

    # --- QR CODE ---
    # Salvamos a posição Y onde começa o rodapé (Lote) para alinhar o QR Code
    y_qrcode = y - 7

    # Lote e Validade (Centralizados na largura total)
    zpl += f"^FO{margem},{y}^A0N,{h_info},{h_info+4}^FB{fb_desc},1,0,C,0^FDLote: {lote_final}^FS\n"
    y += esp_info
    zpl += f"^FO{margem},{y}^A0N,{h_info},{h_info+4}^FB{fb_desc},1,0,C,0^FDValidade: {validade_final}^FS\n"

    # QR Code (Estampado por cima, no canto direito)
    # X=450 deve cair bem naquele espaço vazio que você circulou
    zpl += f"^FO450,{y_qrcode}^BQN,2,3,M,A^FDQA,{lote_final}^FS\n"

    zpl += "^XZ"
    return zpl