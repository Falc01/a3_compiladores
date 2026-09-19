"""
Módulo Léxico da Linguagem MiniLang - UNIFACS 2026.2
Autor / Responsável Técnico pelo Marco 1:
    João Spinola Falcão (RA: 12723116405 | GitHub: @Falc01)
"""

from src.lexer.token import Token, TokenType, TABELA_PALAVRAS_RESERVADAS
from src.lexer.erros import ErroLexico
from src.lexer.lexer import Lexer

__all__ = [
    "Lexer",
    "Token",
    "TokenType",
    "ErroLexico",
    "TABELA_PALAVRAS_RESERVADAS",
]
