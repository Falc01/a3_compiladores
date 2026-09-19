# 💻 MiniLang — Compilador e Interpretador

Projeto prático de avaliação semestral (**A3**) da disciplina de **Teoria da Computação e Compiladores (0006964)**.  
**Universidade Salvador (UNIFACS)** — Período Letivo: **2026.2**  
**Docente**: Prof. Daniel Santana  
**Valor da Avaliação**: 40 Pontos | **Carga Horária**: 160h  

---

## 📖 Sobre o Projeto

O objetivo desta avaliação é projetar e implementar um **compilador completo** para a linguagem imperativa **MiniLang**, percorrendo todas as etapas clássicas de compilação: **análise léxica**, **análise sintática com construção de Árvore Sintática Abstrata (AST)**, **análise semântica com tabela de símbolos e checagem de tipos**, e **back-end** (execução via interpretador ou geração de código intermediário com otimização demonstrada).

O desenvolvimento é cumulativo e avaliado continuamente ao longo do semestre através de **4 marcos (M1 a M4)** com versionamento rigoroso no Git.

---

## 🚀 Como Executar o Compilador (Linha Única)

Conforme exigido pelo **Item 1 do Checklist Oficial da Disciplina**, o compilador executa através de uma **linha de comando única**:

```bash
# Execução padrão do compilador/interpretador
python minilang.py tests/valid/exemplo_basico.ml

# Execução da Análise Léxica (M1 - Exibe tabela de tokens reconhecidos)
python minilang.py tests/valid/exemplo_basico.ml --tokens

# Inspeção visual da Árvore Sintática Abstrata (M2 - AST navegável)
python minilang.py tests/valid/exemplo_basico.ml --ast

# Inspeção da Tabela de Símbolos e Tipos (M3 - Escopos e identificadores)
python minilang.py tests/valid/exemplo_basico.ml --symbols

# Execução com otimização ativada (M4 - Constant Folding / Propagação de constantes)
python minilang.py tests/valid/exemplo_basico.ml --optimize
```

---

## 📜 Especificação Oficial da Linguagem MiniLang

A **MiniLang** é uma linguagem imperativa estruturada com tipagem estática e suporte a comandos de entrada/saída, condicionais, repetições e expressões:

| Categoria | Especificação Oficial do Edital |
| :--- | :--- |
| **Palavras Reservadas (18)** | • **Base (15)**: `programa`, `var`, `inteiro`, `booleano`, `se`, `senão`, `enquanto`, `escreva`, `leia`, `verdadeiro`, `falso`, `e`, `ou`, `não`, `fim`<br>• **Extensão Oficial (Opção D - 3)**: `para`, `repita`, `até` |
| **Identificadores** | Inicia obrigatoriamente com uma letra, seguida de letras, dígitos ou sublinhado `_`. Não pode coincidir com palavras reservadas. |
| **Tipos Primitivos** | `inteiro` (ex: `0`, `42`, `-10`) e `booleano` (`verdadeiro`, `falso`). |
| **Operadores** | • **Aritméticos**: `+`, `-`, `*`, `/`, `%`<br>• **Relacionais**: `==`, `!=`, `<`, `<=`, `>`, `>=`<br>• **Lógicos**: `e`, `ou`, `não`<br>• **Atribuição**: `=` |
| **Delimitadores** | Parênteses `( )`, Chaves `{ }`, Ponto e vírgula `;`, Dois-pontos `:`, Vírgula `,` e Ponto final `.` |
| **Comentários** | Caractere `#` até o final da linha (comentário de linha única, descartado pelo analisador léxico). |
| **Padrão de Erros** | Todas as fases devem reportar: **Fase**, **Linha** e **Coluna** exatas com descrição clara. |

### Exemplo de Código MiniLang Válido (`.ml`)
```pascal
programa fatorial
  var n: inteiro;
  var fat: inteiro;
  var i: inteiro;
{
  # Leitura e cálculo de fatorial
  leia(n);
  fat = 1;
  i = 1;
  
  enquanto (i <= n) {
    fat = fat * i;
    i = i + 1;
  };
  
  escreva(fat);
}
fim.
```

---

## ✅ Checklist Oficial de Avaliação (Seção 11 do Edital)

Este checklist espelha as exigências formais de conformidade estabelecidas pelo professor:

- [x] **1. Execução em linha de comando documentada no README**: O compilador roda por comando direto `python minilang.py <arquivo>`.
- [x] **2. Repositório Git oficial disponibilizado ao professor**: Repositório [Falc01/a3_compiladores](https://github.com/Falc01/a3_compiladores.git) configurado com governança e commits contínuos.
- [ ] **3. Bateria de testes válidos e inválidos**: Pastas `tests/valid/` e `tests/invalid/` cobrindo todas as categorias de código e erros provocados.
- [ ] **4. Mensagens de erro padronizadas com fase, linha e coluna**: Formato `[FASE] Linha L, Coluna C: Descrição`.
- [ ] **5. AST inspecionável e navegável**: Árvore Sintática Abstrata imprimível e verificável durante a correção.
- [ ] **6. Tabela de Símbolos completa**: Registro de identificador, tipo, escopo e posição da declaração.
- [x] **7. Extensão obrigatória definida formalmente (Opção D: `para` e `repita ... até`)**: Escolha oficial registrada, justificada teoricamente (*desugaring* na AST) e integrada desde a especificação léxica.
- [ ] **8. Relatório técnico com declarações formais**: Artigo de 6 a 10 páginas declarando decisões, EBNF, AFD, ferramentas e uso de IA.
- [ ] **9. Domínio individual do código**: Todos os integrantes aptos a explicar qualquer trecho na arguição oral de 15 min.

---

## 📅 Marcos Cumulativos e Pontuação (Total: 40 Pontos)

| Marco | Prazo Estimado | Pontos | Conteúdo / Entregáveis Principais |
| :---: | :---: | :---: | :--- |
| **M1** | Semana 7 (~21/09) | **8 pts** | **Analisador Léxico**: Reconhecimento de todos os tokens, tratamento de lookahead (`=`, `==`, `<`, `<=`, `>`, `>=`, `!=`), descarte de comentários `#`, rastreamento de linha/coluna, diagrama/tabela formal do AFD, suíte de testes e Nota de Marco de 1 página. |
| **M2** | Semana 10 (~12/10) | **12 pts** | **Analisador Sintático + AST**: Gramática EBNF, parser descendente recursivo, construção de AST navegável, recuperação de erros em **modo pânico**, precedência e associatividade de operadores e resolução do *dangling else*. |
| **M3** | Semana 14 (~09/11) | **10 pts** | **Analisador Semântico**: Tabela de símbolos com suporte a escopos aninhados, detecção de variáveis não declaradas, redeclaração, incompatibilidade de tipos, condição não-booleana em `se`/`enquanto` e anotação da AST com tipos inferidos (+0,5 bônus para detecção de variável não inicializada). |
| **M4** | Semana 17 (~30/11) | **10 pts** | **Back-End, Otimização e Apresentação**: Interpretador da AST (ou TAC), otimização com comparativo antes/depois (*Constant Folding*), relatório técnico de 6 a 10 páginas e apresentação de 15 min com demo ao vivo e arguição oral individual. |

---

## 🧩 Extensão Obrigatória (Seção 9 do Edital)

> ⚠️ **Aviso Crítico de Nota**: Equipes do projeto devem escolher e implementar **uma extensão** até o M4. **Sem a extensão implementada, a nota máxima do Marco 4 fica limitada ao teto de 7,0 de 10**.

### 🏆 Escolha Oficial da Equipe: Opção D — Comandos `para` e `repita ... até`

A equipe optou oficialmente pela **Opção D**, expandindo o conjunto de estruturas de controle da MiniLang com os laços `para` (laço determinado estilo C/Pascal) e `repita ... até` (*repeat-until* estilo Pascal).

| Opção | Extensão | O que exige a mais no Compilador | Situação na Equipe |
| :---: | :--- | :--- | :---: |
| **A** | Procedimentos | Procedimentos sem retorno, parâmetros por valor, escopo aninhado e pilha de ativação. | Alternativa |
| **B** | Vetores | Vetores 1D de inteiros, cálculo de endereço/offset e checagem de limites. | Alternativa |
| **C** | Tipo Real | Adição do tipo `real` com promoção/coerção implícita de `inteiro` para `real`. | Alternativa |
| **D** | **Comandos `para` e `repita ... até`** | **Açúcar sintático (*syntactic sugar*) desaçucarado na própria AST para nós `enquanto`.** | **⭐ ADOTADA (Oficial)** |
| **E** | Strings | Tipo cadeia de caracteres com literais `"..."` e concatenação. | Alternativa |

---

### 💡 Justificativa Técnica & Arquitetural da Escolha

1. **Elegância Teórica & Prática de Compiladores Modernos**:
   * Em linguagens de produção modernas (ex: Haskell, Rust, Python e Scala), estruturas derivadas são rotineiramente tratadas como **Açúcar Sintático (*Syntactic Sugar*)**.
   * Ao invés de contaminar o backend com novas instruções primitivas, o compilador realiza o processo de **Desaçucarização (*Desugaring / AST Lowering*)** diretamente durante a geração da AST, convertendo os comandos `para` e `repita ... até` em composições equivalentes de comandos básicos (`atribuição` e `enquanto`).
2. **Mitigação de Riscos no Back-End (M4)**:
   * Opções como *Procedimentos* (Opção A) e *Vetores* (Opção B) demandam reformulações profundas em alocação de memória na pilha, registros de ativação e cálculo dinâmico de offsets de memória em tempo de execução.
   * A Opção D transfere o esforço intelectual para a modelagem gramatical e transformação de árvores, permitindo que a análise semântica (M3) e o back-end (M4) reutilizem a infraestrutura sólida e testada do laço `enquanto`, garantindo estabilidade máxima e menor índice de defeitos.
3. **Alto Impacto Pedagógico na Arguição Oral**:
   * Na apresentação para o professor, a equipe demonstrará visualmente (via `python minilang.py arquivo.ml --ast`) como o código escrito pelo programador é elegante e enxuto, e como a AST o desdobra matematicamente na semântica fundamental da linguagem.

---

### 📝 Especificação Sintática & Regras de Desaçucarização (*Desugaring*)

#### 1. Comando `para`
Permite iterações contadas com inicialização, condição de continuidade e passo de incremento/decremento:
```pascal
# Código MiniLang com a extensão:
para (i = 1; i <= 10; i = i + 1) {
  escreva(i);
}
```
**Transformação Canônica na AST (Desugaring):**
O nó `ParaNode` é transformado em tempo de parsing em uma sequência de nós nativos:
```pascal
# AST equivalente gerada:
i = 1;
enquanto (i <= 10) {
  escreva(i);
  i = i + 1;
}
```

#### 2. Comando `repita ... até`
Executa o bloco de instruções ao menos uma vez e avalia a condição de término no final (*pós-condição*). O laço encerra quando a condição se torna **verdadeira** (semântica clássica do Pascal):
```pascal
# Código MiniLang com a extensão:
repita {
  leia(num);
} até (num > 0);
```
**Transformação Canônica na AST (Desugaring):**
O nó `RepitaAteNode` é expandido no parser para a execução do bloco seguida de um laço `enquanto` com a condição logicamente invertida (`não (condição)`):
```pascal
# AST equivalente gerada:
leia(num);
enquanto (não (num > 0)) {
  leia(num);
}
```

---

### 🗺️ Roteiro de Integração da Extensão nos 4 Marcos

* **Marco 1 (Léxico - M1)**:
  * Inclusão imediata das **3 novas palavras reservadas**: `para` (`TK_PARA`), `repita` (`TK_REPITA`) e `até` (`TK_ATE`), elevando o catálogo de palavras reservadas de 15 para **18 palavras**.
  * Suporte estrito ao caractere acentuado `é` no alfabeto $\Sigma$ e no leitor UTF-8.
* **Marco 2 (Sintático + AST - M2)**:
  * Inclusão das regras de produção na gramática EBNF: `<comando_para>` e `<comando_repita>`.
  * Implementação da função de desaçucaramento (*desugaring*) na construção da AST.
* **Marco 3 (Semântico - M3)**:
  * Reutilização automática das verificações de escopo e compatibilidade de tipos (`booleano` para condições e compatibilidade para variáveis do passo).
* **Marco 4 (Back-End & Apresentação - M4)**:
  * Demonstração funcional com casos de teste dedicados em `tests/valid/extensao_opcao_d.ml` e explicação do *desugaring* na arguição individual de 15 minutos.

---

## 🛠️ Stack Tecnológica & Declaração de Ferramentas (Seção 8 do Edital)

* **Linguagem Principal**: **Python 3** (pela alta legibilidade, facilidade na manipulação de nós da AST e clareza para a arguição individual).
* **Abordagem de Parsing**: **Descendente Recursivo Manual (*Recursive Descent Parser*)**, dispensando dependências de geradores automáticos opacos para assegurar total domínio acadêmico.
* **Uso de IA Generativa**: Declarado formalmente conforme a Seção 8 do edital. Todos os integrantes da equipe dominam a totalidade do código-fonte e estão preparados para explicar qualquer trecho na arguição oral.

---

## 📂 Arquitetura de Diretórios

```text
a3_comp/
├── .gitignore             # Filtro de arquivos temporários e caches do Python
├── README.md              # Documentação principal e checklist de conformidade
├── CONTRIBUTING.md        # Alocação de tarefas da equipe e regras de Git
├── minilang.py            # Ponto de entrada CLI do compilador (linha única)
├── docs/                  # Especificações formais, relatórios de marco e guias
│   ├── Guia_A3_MiniLang_Equipe.pdf
│   └── Instrucoes_A3_MiniLang_UNIFACS_2026_2_com_git_20260910151029.docx
├── src/                   # Módulos do compilador
│   ├── lexer/             # [M1] Scanner, tokens, AFD e lookahead
│   ├── parser/            # [M2] Gramática EBNF, parser recursivo e nós da AST
│   ├── semantic/          # [M3] Tabela de símbolos, escopos e checador de tipos
│   └── backend/           # [M4] Interpretador da AST, otimizador e gerador
└── tests/                 # Bateria de testes automatizados
    ├── valid/             # Programas MiniLang sintática e semanticamente válidos
    └── invalid/           # Casos com erros provocados (léxico, sintático, semântico)
```

---

## 👥 Alocação da Equipe & Governança Git

Para consultar a distribuição de responsabilidades e as regras operacionais, acesse o arquivo [`CONTRIBUTING.md`](./CONTRIBUTING.md):
* **Alocação de Tarefas**: Responsável dedicado para M1, M2, M3 e integração conjunta no M4;
* **Padrão de Commits Semânticos em Português** (`feat:`, `fix:`, `test:`, `docs:`);
* **Política Anti-Penalização**: Commits frequentes ao longo das semanas (proibição de commit único de véspera);
* **Padrão Obrigatório de Mensagens de Erro**: `[FASE] Linha L, Coluna C: Descrição`.

---

## 📚 Referências Bibliográficas Indicadas

* AHO, Alfred V. et al. **Compiladores: princípios, técnicas e ferramentas**. 2. ed. Pearson Addison Wesley, 2008.
* MENEZES, Paulo Blauth. **Linguagens formais e autômatos**. 6. ed. Bookman, 2011.
* SANTOS, Pedro Reis; LANGLOIS, Thibault. **Compiladores: da teoria à prática**. LTC, 2018.
* UNIFACS. **Plano de Ensino 2026.2 — Teoria da Computação e Compiladores (0006964)**.
* SANTANA, Daniel. **Projeto A3 MiniLang — Compilador da MiniLang**. UNIFACS, 2026.
