"""
Módulo de Gestão e Tratamento de Erros Léxicos da MiniLang
Projeto de Avaliação A3 - Teoria da Computação e Compiladores (0006964)
Universidade Salvador (UNIFACS) - Período Letivo: 2026.2
Docente: Prof. Daniel Santana

Autor / Responsável Técnico pelo Marco 1:
    João Spinola Falcão (RA: 12723116405 | GitHub: @Falc01)
"""


class ErroLexico(Exception):
    """
    Exceção representativa de um erro de análise léxica na MiniLang.
    Armazena a localização bidimensional exata (linha e coluna) e a descrição.
    Emite a mensagem rigorosamente no padrão do edital:
        [LÉXICO] Linha L, Coluna C: Descrição
    """

    def __init__(self, mensagem: str, linha: int, coluna: int, caractere: str = ""):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna
        self.caractere = caractere

    def formatar(self) -> str:
        """Retorna a string de erro formatada conforme a rubrica oficial da disciplina."""
        return f"[LÉXICO] Linha {self.linha}, Coluna {self.coluna}: {self.mensagem}"

    def __str__(self) -> str:
        return self.formatar()

    def __repr__(self) -> str:
        return (
            f"ErroLexico(linha={self.linha}, coluna={self.coluna}, "
            f"mensagem={self.mensagem!r}, caractere={self.caractere!r})"
        )
