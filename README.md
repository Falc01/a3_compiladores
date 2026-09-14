# 💻 MiniLang — Compilador e Interpretador

Projeto prático de avaliação semestral (**A3**) da disciplina de **Teoria da Computação e Compiladores (0006964)**.  
**Universidade Salvador (UNIFACS)** — Período Letivo: **2026.2**  
**Docente**: Prof. Daniel Santana  
**Valor da Avaliação**: 40 Pontos | **Carga Horária**: 160h  

---


## 🚀 Como Executar o Compilador (Linha Única)

Conforme exigido pelo requisito central de avaliação, o compilador é executado através de uma **única linha de comando**:

```bash
# Execução padrão do compilador/interpretador
python minilang.py tests/valid/programa_exemplo.ml

# Visualização dos tokens gerados (Análise Léxica - M1)
python minilang.py tests/valid/programa_exemplo.ml --tokens

# Inspeção visual da Árvore Sintática Abstrata (AST - M2)
python minilang.py tests/valid/programa_exemplo.ml --ast

# Inspeção da Tabela de Símbolos com escopos e tipos (Semântico - M3)
python minilang.py tests/valid/programa_exemplo.ml --symbols

# Execução com otimização ativada (ex: Constant Folding - M4)
python minilang.py tests/valid/programa_exemplo.ml --optimize
```

---

## ✅ Checklist Oficial de Avaliação (Seção 11 do Edital)

Este checklist espelha as exigências formais do documento de instruções do professor para assegurar que 100% dos requisitos sejam cumpridos:

- [x] **1. Execução em linha de comando documentada no README**: O compilador roda por comando direto `python minilang.py <arquivo>`.
- [x] **2. Repositório Git oficial disponibilizado ao professor**: Repositório [Falc01/a3_compiladores](https://github.com/Falc01/a3_compiladores.git) configurado com governança e commits contínuos.
- [ ] **3. Bateria de testes válidos e inválidos**: Pasta `tests/valid/` e `tests/invalid/` cobrindo todas as categorias de erro.
- [ ] **4. Mensagens de erro padronizadas com fase, linha e coluna**: Formato `[FASE] Linha L, Coluna C: Descrição`.
- [ ] **5. AST inspecionável e navegável**: Árvore Sintática Abstrata imprimível e verificável durante a correção.
- [ ] **6. Tabela de Símbolos completa**: Registro de identificador, tipo, escopo e posição da declaração.
- [ ] **7. Extensão obrigatória implementada**: Funcionalidade extra implementada, testada, documentada e demonstrada.
- [ ] **8. Relatório técnico com declarações formais**: Artigo de 6 a 10 páginas declarando decisões, EBNF, AFD, ferramentas e uso de IA.
- [ ] **9. Domínio individual do código**: Todos os integrantes aptos a explicar qualquer trecho na arguição oral de 15 min.

---

## 📅 Marcos Cumulativos e Pontuação (Total: 40 Pontos)

| Marco | Prazo Estimado | Pontos | Conteúdo / Entregáveis Principais |
| :---: | :---: | :---: | :--- |
| **M1** | Semana 7 (~21/09) | **8 pts** | **Analisador Léxico**: Reconhecimento de todos os tokens, tratamento de lookahead (`=`, `==`, `<`, `<=`, `>`, `>=`, `!=`), descarte de comentários `#`, rastreamento de linha/coluna, diagrama/tabela formal do AFD e testes válidos/inválidos. |
| **M2** | Semana 10 (~12/10) | **12 pts** | **Analisador Sintático + AST**: Gramática EBNF, parser descendente recursivo, construção de AST navegável, recuperação de erros em **modo pânico**, precedência e associatividade de operadores e resolução do *dangling else*. |
| **M3** | Semana 14 (~09/11) | **10 pts** | **Analisador Semântico**: Tabela de símbolos com suporte a escopos, detecção de variáveis não declaradas, redeclaração, incompatibilidade de tipos, condição não-booleana em `se`/`enquanto` e anotação da AST com tipos inferidos (+0,5 bônus para detecção de variável não inicializada). |
| **M4** | Semana 17 (~30/11) | **10 pts** | **Back-End, Otimização e Apresentação**: Interpretador da AST (ou TAC), otimização com comparativo antes/depois (*Constant Folding*), relatório técnico de 6 a 10 páginas e apresentação de 15 min com demo ao vivo e arguição oral individual. |

---

## 🧩 Extensão Obrigatória (Seção 9)

> ⚠️ **Atenção**: Conforme as regras oficiais da disciplina, sem a implementação de uma extensão, a nota do Marco 4 é limitada ao teto de **7,0 de 10**.

* **Opção Adotada pela Equipe**: **Opção D — Comandos `para` e `repita ... até`** *(ou a definir formalmente pelo grupo)*.
* **Justificativa Técnica**: Implementa construções de repetição adicionais como *açúcar sintático* (*syntactic sugar*), desaçucaradas diretamente na árvore sintática para construções de `enquanto`, mantendo a coerência semântica e a elegância no back-end.

---

## 📂 Arquitetura de Diretórios

```text
a3_comp/
├── .gitignore             # Filtro de arquivos temporários e caches
├── README.md              # Documentação principal e checklist de conformidade
├── CONTRIBUTING.md        # Diretrizes de Git Flow, branches, commits e colaboração
├── minilang.py            # Ponto de entrada CLI do compilador
├── docs/                  # Especificações formais, relatórios de marco e guias
│   ├── Guia_A3_MiniLang_Equipe.pdf
│   └── Instrucoes_A3_MiniLang_UNIFACS_2026_2_com_git_20260910151029.docx
├── src/                   # Módulos do compilador
│   ├── lexer/             # [M1] Scanner, tokens e tabela de transições
│   ├── parser/            # [M2] Gramática, parser recursivo e nós da AST
│   ├── semantic/          # [M3] Tabela de símbolos e checador de tipos
│   └── backend/           # [M4] Interpretador da AST, gerador e otimizador
└── tests/                 # Bateria de testes
    ├── valid/             # Casos de teste que devem compilar e executar
    └── invalid/           # Casos com erros provocados (léxico, sintático, semântico)
```

---

## 📜 Governança, Equipe & Contribuição

Consulte o arquivo [`CONTRIBUTING.md`](./CONTRIBUTING.md) para detalhes sobre:
* **Integrantes do grupo** e definição das atribuições de cada marco;
* Padrão de commits semânticos em Português (`feat:`, `fix:`, `test:`, `docs:`);
* Política anti-penalização (commits frequentes de todos os membros);
* Estrutura de branches (`main`, `develop`, `feature/*`);
* Padrão oficial de formatação de mensagens de erro.
