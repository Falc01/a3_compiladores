"""
Módulo de Definição de Tokens da Linguagem MiniLang
Projeto de Avaliação A3 - Teoria da Computação e Compiladores (0006964)
Universidade Salvador (UNIFACS) - Período Letivo: 2026.2
Docente: Prof. Daniel Santana

Autor / Responsável Técnico pelo Marco 1:
    João Spinola Falcão (RA: 12723116405 | GitHub: @Falc01)
"""

from dataclasses import dataclass
from enum import Enum, unique
from typing import Any, Optional


@unique
class TokenType(Enum):
    """
    Enumeração canônica com as 41 categorias de tokens reconhecidas pelo
    Analisador Léxico da MiniLang (38 da especificação base + 3 da Extensão Opção D).
    """

    # --- 1. Palavras Reservadas da Base (15) ---
    PROGRAMA = "TK_PROGRAMA"
    VAR = "TK_VAR"
    TIPO_INTEIRO = "TK_TIPO_INTEIRO"
    TIPO_BOOLEANO = "TK_TIPO_BOOLEANO"
    SE = "TK_SE"
    SENAO = "TK_SENAO"
    ENQUANTO = "TK_ENQUANTO"
    ESCREVA = "TK_ESCREVA"
    LEIA = "TK_LEIA"
    FIM = "TK_FIM"
    VERDADEIRO = "TK_VERDADEIRO"
    FALSO = "TK_FALSO"
    OP_E = "TK_OP_E"
    OP_OU = "TK_OP_OU"
    OP_NAO = "TK_OP_NAO"

    # --- 2. Palavras Reservadas da Extensão Obrigatória: Opção D (3) ---
    PARA = "TK_PARA"
    REPITA = "TK_REPITA"
    ATE = "TK_ATE"

    # --- 3. Identificadores e Literais Numéricos (2) ---
    ID = "TK_ID"
    NUMERO = "TK_NUMERO"

    # --- 4. Operadores Aritméticos Primitivos (5) ---
    SOMA = "TK_SOMA"          # +
    SUB = "TK_SUB"            # -
    MULT = "TK_MULT"          # *
    DIV = "TK_DIV"            # /
    MOD = "TK_MOD"            # %

    # --- 5. Operador de Atribuição (1) ---
    ATRIB = "TK_ATRIB"        # =

    # --- 6. Operadores Relacionais com Lookahead (6) ---
    IGUAL = "TK_IGUAL"              # ==
    DIFERENTE = "TK_DIFERENTE"      # !=
    MENOR = "TK_MENOR"              # <
    MENOR_IGUAL = "TK_MENOR_IGUAL"  # <=
    MAIOR = "TK_MAIOR"              # >
    MAIOR_IGUAL = "TK_MAIOR_IGUAL"  # >=

    # --- 7. Delimitadores Estruturais (8) ---
    ABRE_PAR = "TK_ABRE_PAR"              # (
    FECHA_PAR = "TK_FECHA_PAR"            # )
    ABRE_CHAVE = "TK_ABRE_CHAVE"          # {
    FECHA_CHAVE = "TK_FECHA_CHAVE"        # }
    PONTO_VIRGULA = "TK_PONTO_VIRGULA"    # ;
    DOIS_PONTOS = "TK_DOIS_PONTOS"        # :
    VIRGULA = "TK_VIRGULA"                # ,
    PONTO = "TK_PONTO"                    # .

    # --- 8. Sentinela de Fim de Fita / Arquivo (1) ---
    EOF = "TK_EOF"


# Tabela Hash de Palavras Reservadas para resolução em tempo constante O(1)
TABELA_PALAVRAS_RESERVADAS: dict[str, TokenType] = {
    # 15 Palavras Reservadas da Base
    "programa": TokenType.PROGRAMA,
    "var": TokenType.VAR,
    "inteiro": TokenType.TIPO_INTEIRO,
    "booleano": TokenType.TIPO_BOOLEANO,
    "se": TokenType.SE,
    "senão": TokenType.SENAO,
    "enquanto": TokenType.ENQUANTO,
    "escreva": TokenType.ESCREVA,
    "leia": TokenType.LEIA,
    "fim": TokenType.FIM,
    "verdadeiro": TokenType.VERDADEIRO,
    "falso": TokenType.FALSO,
    "e": TokenType.OP_E,
    "ou": TokenType.OP_OU,
    "não": TokenType.OP_NAO,
    # 3 Palavras Reservadas da Extensão Oficial (Opção D)
    "para": TokenType.PARA,
    "repita": TokenType.REPITA,
    "até": TokenType.ATE,
}


@dataclass(frozen=True)
class Token:
    """
    Representação formal da 5-tupla canônica de um Token:
    < tipo, lexema, valor, linha, coluna >
    """
    tipo: TokenType
    lexema: str
    valor: Any = None
    linha: int = 1
    coluna: int = 1

    def __repr__(self) -> str:
        valor_str = f", valor={self.valor!r}" if self.valor is not None else ""
        return (
            f"Token({self.tipo.value}, lexema={self.lexema!r}"
            f"{valor_str}, linha={self.linha}, col={self.coluna})"
        )

    def __str__(self) -> str:
        return self.__repr__()
