"""
Utilitários de texto.

Responsável por:
- quebra de texto
- normalização de descrição
- ajuste de layout textual para etiquetas
"""


def quebrar_texto(texto, max_chars):
    palavras = texto.split(" ")
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        if len(linha_atual + " " + palavra) <= max_chars:
            linha_atual += (" " if linha_atual else "") + palavra
        else:
            linhas.append(linha_atual)
            linha_atual = palavra

    if linha_atual:
        linhas.append(linha_atual)

    return linhas


def ajustar_descricao_duas_linhas(texto, max_chars_linha=17, max_linhas=2):
    texto = texto.upper().strip()

    palavras_remover = {" DE ", " DA ", " DO ", " DAS ", " DOS ", " E ", " PARA ", " COM "}
    texto_limpo = f" {texto} "
    for p in palavras_remover:
        texto_limpo = texto_limpo.replace(p, " ")

    texto_limpo = " ".join(texto_limpo.split())
    palavras = texto_limpo.split(" ")

    linhas = []
    linha_atual = ""

    for palavra in palavras:
        teste = (linha_atual + " " + palavra).strip()
        if len(teste) <= max_chars_linha:
            linha_atual = teste
        else:
            if linha_atual:
                linhas.append(linha_atual)
            linha_atual = palavra

        if len(linhas) == max_linhas:
            break

    if len(linhas) < max_linhas and linha_atual:
        linhas.append(linha_atual)

    return linhas[:max_linhas]


def abreviar_termos_tecnicos(texto):
    # Dicionário baseado na sua lista de stock
    substituicoes = {
        "5000ML": "5L",
        "1000ML": "1L",
        "1000 ML": "1L",
        "5000 ML": "5L",
        "MEMBRANA": "MEMB.",
        
        
        
    }
    texto = texto.upper()
    for original, substituto in substituicoes.items():
        texto = texto.replace(original, substituto)
    return texto

def normalizar_descricao_para_etiqueta(texto, limite=None):
    if not texto:
        return ""
    
    # Aplica abreviações primeiro para ganhar espaço real
    texto = abreviar_termos_tecnicos(texto)
    
    texto = texto.replace("\n", " ")
    texto = " ".join(texto.split()).strip()

    if limite is not None:
        texto = texto[:limite]
    return texto


"""
"ESTÉRIL": "EST.",
        "SISTEMA": "SIST.",
        "TRANSFERÊNCIA": "TRANSF.",
        "FRASCO": "FRASC.",
        "5000ML": "5L",
        "1000ML": "1L",
        "POLIPROPILENO": "PP",
        "CENTRÍFUGA": "CENT.",
        "MEMBRANA": "MEMB."
"""