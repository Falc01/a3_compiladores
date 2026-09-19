#!/usr/bin/env python3
"""
Compilador MiniLang - Projeto de Avaliação A3
Disciplina: Teoria da Computação e Compiladores (0006964)
Universidade Salvador (UNIFACS) - Período Letivo: 2026.2
Docente: Prof. Daniel Santana

Autores (Equipe A3):
    - João Spinola Falcão (RA: 12723116405 | GitHub: @Falc01) [Responsável M1 e M4]
    - Pedro Adaime Ribeiro (RA: 12723119338 | GitHub: @pedrobelane) [Responsável M3]
    - Integrante 3 (A definir) [Responsável M2]
"""

import sys
import argparse
from pathlib import Path

# Garante saída UTF-8 no terminal Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from src.lexer import Lexer, TokenType, ErroLexico


def exibir_tabela_tokens(tokens, nome_arquivo: str) -> None:
    """Exibe no terminal a listagem tabular e formatada dos tokens gerados pelo scanner."""
    print("=" * 82)
    print(f"TABELA DE TOKENS RECONHECIDOS (Marco 1 - Análise Léxica)")
    print(f"Arquivo: {nome_arquivo} | Total de Tokens Emitidos: {len(tokens)}")
    print("=" * 82)
    print(f"{'LINHA':>5} | {'COLUNA':>6} | {'TIPO DO TOKEN':<20} | {'LEXEMA':<20} | {'VALOR ATRIBUTO':<15}")
    print("-" * 82)

    for tok in tokens:
        lexema_repr = f"'{tok.lexema}'" if tok.tipo != TokenType.EOF else "EOF"
        valor_repr = f"{tok.valor!r}" if tok.valor is not None else "-"
        print(f"{tok.linha:>5} | {tok.coluna:>6} | {tok.tipo.value:<20} | {lexema_repr:<20} | {valor_repr:<15}")

    print("-" * 82)


def main():
    parser = argparse.ArgumentParser(
        description="Compilador e Interpretador MiniLang - UNIFACS 2026.2 (Prof. Daniel Santana)",
        epilog="Exemplo de uso: python minilang.py tests/valid/exemplo.ml --tokens"
    )
    parser.add_argument("arquivo", nargs="?", help="Caminho do arquivo de código-fonte MiniLang (.ml)")
    parser.add_argument("--tokens", action="store_true", help="Executa a análise léxica e exibe a tabela de tokens (M1)")
    parser.add_argument("--ast", action="store_true", help="Exibe a Árvore Sintática Abstrata (M2)")
    parser.add_argument("--symbols", action="store_true", help="Exibe a Tabela de Símbolos e checagem de tipos (M3)")
    parser.add_argument("--optimize", action="store_true", help="Aplica otimizações de código intermediário (M4)")
    parser.add_argument("--version", action="version", version="MiniLang Compiler v0.2.0 (Marco 1 - Léxico Concluído)")

    args = parser.parse_args()

    if not args.arquivo:
        parser.print_help()
        sys.exit(0)

    caminho = Path(args.arquivo)
    if not caminho.is_file():
        print(f"[ERRO] Arquivo não encontrado: {args.arquivo}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            codigo_fonte = f.read()
    except Exception as e:
        print(f"[ERRO] Falha ao abrir o arquivo '{caminho}': {e}", file=sys.stderr)
        sys.exit(1)

    # Inicialização do Scanner Léxico (Marco 1)
    lexer = Lexer(codigo_fonte, nome_arquivo=caminho.name)
    tokens, erros = lexer.tokenizar_tudo()

    # Tratamento e Exibição de Erros Léxicos
    if erros:
        for erro in erros:
            print(erro.formatar(), file=sys.stderr)
        print(f"\n[FALHA] Compilação interrompida: {len(erros)} erro(s) léxico(s) detectado(s).", file=sys.stderr)
        sys.exit(1)

    # Exibição de Tokens quando solicitado via CLI
    if args.tokens:
        exibir_tabela_tokens(tokens, caminho.name)
        print("[SUCESSO] Análise léxica concluída com 0 erros.")
        sys.exit(0)

    # Execução padrão provisória (enquanto M2 a M4 estão em desenvolvimento)
    print(f"=== Compilador MiniLang ===")
    print(f"Arquivo processado: {caminho.name}")
    print(f"Marco 1 (Análise Léxica): OK ({len(tokens)} tokens gerados sem erros).")
    print("Dica: Utilize a flag '--tokens' para visualizar a tabela detalhada de tokens.")


if __name__ == "__main__":
    main()
