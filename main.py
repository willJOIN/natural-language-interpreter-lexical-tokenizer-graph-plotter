import re
import unicodedata
from parser.roman import rom_parse

from aresta import Aresta
from grafo import Grafo
from vertice import Vertice


def tokenization(grafo):
    # cria dicionario vazio
    tokens = {}

    # TODO loop pra ler cada arq_[i]

    # abre 1 arquivo de texto no modo leitura f
    with open("textos/arq_1.txt", "r", encoding="ISO-8859-1") as f:
        # le o arquivo e armazena em linha
        for line in f.readlines():
            for token in exec(line):
                if tokens.get(token):
                    tokens[token] += 1
                else:
                    tokens[token] = 1

    print(tokens)


def exec(linha):
    # substutito todas os chars com acento pelos sem acento correspondente
    def substituir_acentos(linha_com_acentos):
        return linha_com_acentos.translate(criar_tabela_substituicao())

    def remover_numeros_extenso(linha_numero_extenso):

        linha = linha_numero_extenso.split(" ")
        numeros_extenso = []

        with open("numeros_extenso.txt", "r") as f:
            numeros_extenso = f.readlines()

        numeros_extenso = [
            numero.replace("\n", "").strip() for numero in numeros_extenso
        ]

        idx_a_remover = []

        for idx in range(len(linha)):
          if linha[idx] in numeros_extenso:
              idx_a_remover.append(idx)

        for idx in idx_a_remover:
          linha.remove(linha[idx])

        return " ".join(linha)

    def remover_numeros_ordinais(linha_numeros_ordinais):
        linha = linha_numeros_ordinais.split(" ")
        linha = [palavra for palavra in linha if "ESIMO" not in palavra]

        ordinais = []

        with open("numeros_ordinais.txt", "r") as f:
            ordinais = f.readlines()

        ordinais = [numero.replace("\n", "").strip() for numero in ordinais]

        for idx in range(len(linha) - 1):
            if linha[idx] in ordinais:
                linha.remove(linha[idx])

        return " ".join(linha)

    def remover_numeros_romanos(linha_com_romanos):
        linha = linha_com_romanos.split(" ")

        for idx in range(len(linha)):
            try:
                rom_parse(linha[idx])
                linha.remove(linha[idx])
            except:
                continue

        return " ".join(linha)

    def remover_stop_words(linha_crua):
        linha = linha_crua.strip()

        stop_words = []

        with open("stop_words.txt", "r") as f:
            for line in f.readlines():
                for stop_word in line.split(", "):
                    stop_words.append(substituir_acentos(stop_word.upper()))

        stop_words = list(set(stop_words))

        linha = " ".join(
            [
                palavra.strip()
                for palavra in re.split(" +", linha)
                if palavra.strip() not in stop_words
            ]
        )

        return linha

    def limpar_linha(linha_com_espacos):
        especiais = "°ªº!@#$%¨&*=+-_()[]{}´`~^:;.,/?\|'"
        numeros = [str(valor) for valor in range(0, 10)]

        linha = linha_com_espacos

        for especial in especiais:
            linha = linha.replace(especial, "")

        for numero in numeros:
            linha = linha.replace(numero, "")

        return linha.replace("\n", "").upper()

    return re.split(
        " +",
        remover_numeros_ordinais(
            remover_numeros_extenso(
                remover_numeros_romanos(
                    remover_stop_words(substituir_acentos(limpar_linha(linha)))
                )
            )
        ),
    )


def criar_tabela_substituicao():
    chars_acentuados = "ÁÉÍÓÚÀÈÌÒÙÃẼĨÕŨÂÊÎÔÛÄËÏÖÜÇ"
    chars = "AEIOUAEIOUAEIOUAEIOUAEIOUC"

    # cria um "mapa" sendo o char com acento a value e o seu correspondente a chave
    tabela = {
        ord(acento): ord(sem_acento)
        for acento, sem_acento in zip(chars_acentuados, chars)
    }
    return tabela


if __name__ == "__main__":
    grafo = Grafo()
    v1 = grafo.add_vertice(0)
    v2 = grafo.add_vertice(1)
    v3 = grafo.add_vertice(0)
    v4 = Vertice(2)

    grafo.add_aresta(v1, v2)
    grafo.add_aresta(v1, v2)

    tokenization(grafo)
