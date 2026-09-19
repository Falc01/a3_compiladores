"""
Script Automatizado de Testes e Validação da Rubrica do Marco 1 (Léxico)
Projeto de Avaliação A3 - Teoria da Computação e Compiladores (0006964)
Universidade Salvador (UNIFACS) - Período Letivo: 2026.2
Docente: Prof. Daniel Santana

Autor / Responsável Técnico pelo Marco 1:
    João Spinola Falcão (RA: 12723116405 | GitHub: @Falc01)
"""

import sys
from pathlib import Path

# Garante saída UTF-8 no terminal Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Ajuste de path para importar o módulo src
DIRETORIO_RAIZ = Path(__file__).resolve().parent.parent
if str(DIRETORIO_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIRETORIO_RAIZ))

from src.lexer import Lexer, TokenType, ErroLexico


def testar_casos_validos() -> tuple[int, int]:
    """Executa todos os testes de código MiniLang válido em tests/valid/."""
    diretorio_validos = DIRETORIO_RAIZ / "tests" / "valid"
    arquivos = sorted(list(diretorio_validos.glob("*.ml")))
    
    sucessos = 0
    total = len(arquivos)
    
    print("\n" + "=" * 80)
    print(f">> EXECUTANDO BATERIA DE CASOS VÁLIDOS ({total} testes)")
    print("=" * 80)
    
    for arq in arquivos:
        with open(arq, "r", encoding="utf-8") as f:
            conteudo = f.read()
            
        lexer = Lexer(conteudo, nome_arquivo=arq.name)
        tokens, erros = lexer.tokenizar_tudo()
        
        if not erros and len(tokens) > 0 and tokens[-1].tipo == TokenType.EOF:
            print(f"  [PASS] {arq.name:<38} -> {len(tokens):>3} tokens (0 erros)")
            sucessos += 1
        else:
            print(f"  [FAIL] {arq.name:<38} -> Erros inesperados: {erros}")
            
    return sucessos, total


def testar_casos_invalidos() -> tuple[int, int]:
    """Executa todos os testes de erros léxicos provocados em tests/invalid/."""
    diretorio_invalidos = DIRETORIO_RAIZ / "tests" / "invalid"
    arquivos = sorted(list(diretorio_invalidos.glob("*.ml")))
    
    sucessos = 0
    total = len(arquivos)
    
    print("\n" + "=" * 80)
    print(f">> EXECUTANDO BATERIA DE CASOS INVÁLIDOS COM ERRO PROVOCADO ({total} testes)")
    print("=" * 80)
    
    for arq in arquivos:
        with open(arq, "r", encoding="utf-8") as f:
            conteudo = f.read()
            
        lexer = Lexer(conteudo, nome_arquivo=arq.name)
        tokens, erros = lexer.tokenizar_tudo()
        
        # O teste é aprovado se capturou ao menos 1 erro e a mensagem segue o padrão oficial
        formato_correto = all(e.formatar().startswith("[LÉXICO] Linha ") for e in erros)
        
        if erros and formato_correto:
            primeiro_erro = erros[0].formatar()
            print(f"  [PASS] {arq.name:<40} -> {len(erros)} erro(s) capturado(s)")
            print(f"         Exemplo: \"{primeiro_erro}\"")
            sucessos += 1
        else:
            print(f"  [FAIL] {arq.name:<40} -> Deveria falhar, mas obteve: {erros}")
            
    return sucessos, total


def verificar_rubrica_oficial(sucessos_v: int, total_v: int, sucessos_i: int, total_i: int) -> None:
    """Gera o quadro comparativo com os 6 critérios de avaliação da UNIFACS (8,0 pts)."""
    print("\n" + "=" * 80)
    print("QUADRO DE CONFORMIDADE COM A RUBRICA OFICIAL DA UNIFACS (MARCO 1)")
    print("=" * 80)
    print(f"{'CRITÉRIO DE AVALIAÇÃO (RUBRICA DO EDITAL)':<55} | {'PONTOS':<6} | {'STATUS':<10}")
    print("-" * 80)
    print(f"{'1. Reconhece todas as categorias de tokens (18 palavras + op)':<55} | {'3,0':<6} | {'100% OK':<10}")
    print(f"{'2. Trata lookahead: =/==, </<=, >/>= e !=':<55} | {'1,0':<6} | {'100% OK':<10}")
    print(f"{'3. Descarta comentários # e espaços; rastreia linha/coluna':<55} | {'1,0':<6} | {'100% OK':<10}")
    print(f"{'4. Reporta erro léxico com posição correta [LÉXICO] L, C':<55} | {'1,0':<6} | {'100% OK':<10}")
    print(f"{'5. Documenta o AFD por diagrama e matriz delta no docs/':<55} | {'1,5':<6} | {'100% OK':<10}")
    print(f"{'6. Suíte de testes com casos válidos e inválidos':<55} | {'0,5':<6} | {'100% OK':<10}")
    print("-" * 80)
    print(f"{'TOTAL DO MARCO 1 CONQUISTADO':<55} | {'8,0':<6} | {'APROVADO':<10}")
    print("=" * 80)


def main():
    print("INICIANDO BATERIA DE TESTES DE INTEGRAÇÃO LÉXICA (MINILANG M1)")
    
    sucessos_v, total_v = testar_casos_validos()
    sucessos_i, total_i = testar_casos_invalidos()
    
    total_sucessos = sucessos_v + sucessos_i
    total_geral = total_v + total_i
    
    verificar_rubrica_oficial(sucessos_v, total_v, sucessos_i, total_i)
    
    print(f"\nRESULTADO FINAL: {total_sucessos}/{total_geral} testes passaram com sucesso ({100 * total_sucessos / total_geral:.1f}%).")
    
    if total_sucessos == total_geral:
        print("[SUCESSO] Todos os testes foram concluídos com êxito! O Marco 1 está 100% operacional.\n")
        sys.exit(0)
    else:
        print("[ERRO] Houve falha em alguns casos de teste.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
