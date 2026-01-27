from backend.utils.texto import (
    ajustar_descricao_duas_linhas,
    normalizar_descricao_para_etiqueta
)

def gerar_zpl_40x20(codigo, descricao, lote, validade):
    largura = 320
    altura = 160
    margem = 14
    fb_desc = largura - (margem * 2)

    # Normaliza e limita a descrição
    descricao_tratada = normalizar_descricao_para_etiqueta(
        descricao,
        limite=40
    )

    # Divide o texto em uma lista de até 2 linhas
    linhas_desc = ajustar_descricao_duas_linhas(
        descricao_tratada,
        max_chars_linha=20,
        max_linhas=2
    )

    # Definições de tamanhos
    h_codigo = 32
    esp_codigo = 36
    
    # Ajuste dinâmico de altura da fonte da descrição
    if len(linhas_desc) == 1:
        h_desc = 24
        esp_desc = 28
    else:
        h_desc = 22
        esp_desc = 26

    h_info = 22
    esp_info = 22

    # Cálculo do Y inicial para centralizar o bloco todo verticalmente
    linhas_usadas = len(linhas_desc)
    altura_total_bloco = esp_codigo + (linhas_usadas * esp_desc) + (esp_info * 2)
    y = (altura - altura_total_bloco) // 2

    zpl = "^XA\n"
    zpl += f"^PW{largura}\n"
    zpl += f"^LL{altura}\n"
    zpl += "^CI28\n"

    # 1. Código do Produto
    zpl += f"^FO{margem},{y}^A0N,{h_codigo},{h_codigo-1}^FB{fb_desc},1,0,C,0^FD{codigo}^FS\n"
    y += esp_codigo

    # 2. Descrição (Imprimindo cada linha individualmente para evitar sobreposição)
    for linha in linhas_desc:
        zpl += f"^FO{margem},{y}^A0N,{h_desc},{h_desc-1}^FB{fb_desc},1,0,C,0^FD{linha}^FS\n"
        y += esp_desc

    # 3. Informações de Lote e Validade
    y += 4 # Pequeno respiro antes das infos finais
    zpl += f"^FO{margem},{y}^A0N,{h_info},{h_info-1}^FB{fb_desc},1,0,C,0^FDLote: {lote}^FS\n"
    y += esp_info
    zpl += f"^FO{margem},{y}^A0N,{h_info},{h_info-1}^FB{fb_desc},1,0,C,0^FDValidade: {validade}^FS\n"

    zpl += "^XZ"
    return zpl