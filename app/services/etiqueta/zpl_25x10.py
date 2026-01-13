from app.utils.texto import ajustar_descricao_duas_linhas


def gerar_zpl_25x10(codigo, descricao, lote, validade):
    largura = 200
    altura = 80
    margem = 6
    fb_desc = largura - (margem * 2)

    linhas_desc = ajustar_descricao_duas_linhas(descricao, max_chars_linha=20)
    linhas_usadas = len(linhas_desc)

    desc_formatada = "\\&".join(linhas_desc)

    h_codigo = 18
    esp_codigo = 15

    h_desc = 10
    esp_desc = 16

    altura_bloco = esp_codigo + (linhas_usadas * esp_desc)

    y_centro_bloco = altura // 2
    y = y_centro_bloco - (altura_bloco // 2)
    y -= 2

    zpl = "^XA\n"
    zpl += "^CI28\n"
    zpl += f"^PW{largura}\n"
    zpl += f"^LL{altura}\n"
    zpl += "^MNW\n"
    zpl += "^LS0\n"
    zpl += "^LT0\n"

    zpl += (
        f"^FO{margem},{y}"
        f"^A0N,{h_codigo},{h_codigo-1}"
        f"^FB{fb_desc},1,0,C,0"
        f"^FD{codigo}^FS\n"
    )
    y += esp_codigo
    y += 6

    zpl += (
        f"^FO{margem},{y}"
        f"^A0N,16,15"
        f"^FB{fb_desc},2,0,C,0"
        f"^FD{desc_formatada}^FS\n"
    )

    y += 30

    zpl += (
        f"^FO{margem},{y}"
        f"^A0N,15,14"
        f"^FB{fb_desc},1,0,C,0"
        f"^FDL:{lote} V:{validade}^FS\n"
    )

    zpl += "^XZ"
    return zpl
