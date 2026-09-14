#!/usr/bin/env python3
"""
Compilador MiniLang - Projeto de Avaliação A3
Disciplina: Teoria da Computação e Compiladores (0006964)
UNIFACS - Período Letivo 2026.2
Docente: Prof. Daniel Santana
"""

import sys
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Compilador e Interpretador MiniLang - UNIFACS 2026.2",
        epilog="Exemplo de uso: python minilang.py programa.ml --tokens"
    )
    parser.add_argument("arquivo", nargs="?", help="Caminho do arquivo de código-fonte MiniLang (.ml)")
    parser.add_argument("--tokens", action="store_true", help="Executa apenas a análise léxica e exibe os tokens")
    parser.add_argument("--ast", action="store_true", help="Exibe a Árvore Sintática Abstrata (AST)")
    parser.add_argument("--symbols", action="store_true", help="Exibe a Tabela de Símbolos gerada na análise semântica")
    parser.add_argument("--optimize", action="store_true", help="Aplica otimizações de código (ex: Constant Folding)")
    parser.add_argument("--version", action="version", version="MiniLang Compiler v0.1.0-alpha")

    args = parser.parse_args()

    if not args.arquivo:
        parser.print_help()
        sys.exit(0)

    caminho = Path(args.arquivo)
    if not caminho.is_file():
        print(f"[ERRO] Arquivo não encontrado: {args.arquivo}", file=sys.stderr)
        sys.exit(1)

    with open(caminho, "r", encoding="utf-8") as f:
        codigo_fonte = f.read()

    print(f"=== Compilador MiniLang ===")
    print(f"Arquivo: {caminho.name}")
    print(f"Status do Pipeline: Estrutura inicial carregada com sucesso.")
    print("Fase atual: Configuração inicial da A3 (M1 em desenvolvimento).")


if __name__ == "__main__":
    main()
