# 📄 Especificação de Requisitos, Modelagem Formal (AFD) e Arquitetura do Analisador Léxico (MiniLang)

**Autor:** João Spinola Falcão (RA: `12723116405` | GitHub: `@Falc01`)  
**Instituição:** Universidade Salvador (UNIFACS)  
**Disciplina:** Teoria da Computação e Compiladores (0006964) — Prof. Daniel Santana  
**Marco Avaliativo:** Marco 1 (M1 — Analisador Léxico / Scanner) — 8,0 Pontos  
**Período Letivo:** 2026.2 | **Carga Horária:** 160h  
**Classificação:** Especificação Técnica de Engenharia de Compiladores / Formalismo Matemático  

---

## 📌 1. Resumo Executivo & Fundamentação Teórica (*Explanation*)

O **Analisador Léxico** (ou *Scanner*) constitui a primeira fase do pipeline de compilação da **MiniLang**. Sua função primária é atuar como transdutor: ele consome o fluxo linear de caracteres brutos do código-fonte e o converte em uma sequência estruturada e finita de unidades atômicas dotadas de significado sintático, denominadas **Tokens**.

### 1.1. A Tríade Canônica da Fase Léxica
Conforme o modelo formal adotado nas aulas do Prof. Daniel Santana, a análise léxica é regida pela distinção rigorosa de três conceitos:
* **Lexema**: A cadeia concreta de caracteres extraída do código-fonte (ex: `"total"`, `"="`, `"42"`, `"<="`).
* **Token**: A categoria sintática abstrata atribuída ao lexema pelo compilador (ex: `TK_IDENT`, `TK_ATRIB`, `TK_NUMERO`, `TK_OP_REL`).
* **Padrão (*Pattern*)**: A regra formal de formação descrita por meio de uma **Expressão Regular (ER)** que define o conjunto de todos os lexemas válidos pertencentes àquela categoria.

### 1.2. Executar versus Descrever (Hierarquia de Chomsky)
A fase léxica opera estritamente no **Tipo 3 da Hierarquia de Chomsky** (Linguagens Regulares):
* A **Expressão Regular descreve** declarativamente o formato dos tokens;
* O **Autômato Finito Determinístico (AFD) executa** operacionalmente o reconhecimento na máquina;
* **Limite de Memória Finita**: O AFD codifica sua memória exclusivamente em seu conjunto finito de estados $Q$. Ele é capaz de lembrar fatos locais (ex: *"o último caractere foi '<'"*, *"já vi o início de um comentário"*), tornando-o ideal para a fase léxica. Estruturas aninhadas recursivamente (como parênteses e blocos arbitrários $\{ \}$ de $a^n b^n$) transcendem o poder das linguagens regulares e são delegadas à fase sintática posterior (Gramáticas Livres de Contexto — Tipo 2).

---

## 📋 2. Matriz de Engenharia de Requisitos da Fase Léxica (SRS Léxico)

A especificação do analisador léxico é formalizada a seguir por meio de requisitos atômicos, testáveis e rastreáveis.

### 2.1. Requisitos Funcionais (RF-LEX)

| ID | Requisito Funcional | Descrição Operacional & Regra de Negócio |
| :--- | :--- | :--- |
| **RF-LEX-01** | **Reconhecimento de Palavras Reservadas** | O scanner deve identificar exaustivamente as **15 palavras reservadas** da MiniLang: `programa`, `var`, `inteiro`, `booleano`, `se`, `senão`, `enquanto`, `escreva`, `leia`, `verdadeiro`, `falso`, `e`, `ou`, `não`, `fim`. |
| **RF-LEX-02** | **Reconhecimento de Identificadores** | Deve reconhecer identificadores pelo padrão `[A-Za-z_][A-Za-z0-9_]*`. |
| **RF-LEX-03** | **Precedência Palavra-Chave vs. Identificador** | Em caso de colisão sintática, palavras reservadas possuem **precedência estrita** sobre identificadores comuns. A resolução deve ocorrer em tempo constante $\mathcal{O}(1)$ via tabela hash. |
| **RF-LEX-04** | **Reconhecimento de Literais Inteiros** | Deve reconhecer sequências numéricas decimais `[0-9]+` e computar o atributo semântico numérico correspondente (inteiro nativo). |
| **RF-LEX-05** | **Reconhecimento de Literais Booleanos** | As palavras reservadas `verdadeiro` e `falso` devem ser emitidas como tokens booleanos com valores lógicos associados (`True`/`False`). |
| **RF-LEX-06** | **Reconhecimento de Operadores Aritméticos** | Deve reconhecer os operadores aritméticos primitivos: soma (`+`), subtração (`-`), multiplicação (`*`), divisão (`/`) e resto da divisão (`%`). |
| **RF-LEX-07** | **Lookahead para Operadores Relacionais** | Deve implementar *lookahead* determinístico de 1 caractere ($k=1$) para desambiguar: `<` vs. `<=`, `>` vs. `>=`, `==` vs. `=` e `!=` vs. `!`. |
| **RF-LEX-08** | **Operador de Atribuição Simples** | O símbolo `=` isolado deve ser classificado exclusivamente como operador de atribuição (`TK_ATRIB`). |
| **RF-LEX-09** | **Operadores Lógicos Textuais** | Os operadores lógicos `e`, `ou` e `não` devem ser categorizados com tipos de token lógicos específicos para suporte à precedência de expressões. |
| **RF-LEX-10** | **Reconhecimento de Delimitadores Estruturais** | Deve reconhecer a pontuação da MiniLang: parênteses `( )`, chaves `{ }`, ponto e vírgula `;`, dois-pontos `:`, vírgula `,` e ponto final `.`. |
| **RF-LEX-11** | **Descarte de Espaços em Branco** | Espaços (` `), tabulações (`\t`) e quebras de linha (`\r`, `\n`) devem ser consumidos sem gerar tokens espúrios na saída. |
| **RF-LEX-12** | **Descarte de Comentários de Linha Única** | Todo texto iniciado pelo caractere `#` até a quebra de linha `\n` ou fim de arquivo deve ser descartado pelo léxico. |
| **RF-LEX-13** | **Rastreamento Bidimensional $(Linha, Coluna)$** | Cada token emitido deve armazenar com precisão a **linha** e a **coluna de início** de seu primeiro caractere no código-fonte. |
| **RF-LEX-14** | **Emissão do Sentinela de Fim de Arquivo (EOF)** | Ao esgotar o código-fonte, o scanner deve emitir um token especial de término `TK_EOF` com as coordenadas finais da fita. |
| **RF-LEX-15** | **Princípio do Casamento Mais Longo (*Maximal Munch*)** | Diante de operadores ambíguos, o scanner deve sempre consumir o prefixo mais longo que satisfaça um padrão léxico (ex: `<=` em vez de `<` seguido de `=`). |
| **RF-LEX-16** | **Recuperação em Modo Descarte (*Panic Mode* Léxico)** | Ao encontrar um caractere fora do alfabeto (ex: `@`, `$`, `~`), o scanner não deve abortar bruscamente; deve registrar o erro, descartar o caractere e continuar para capturar múltiplos erros em uma única passada. |

### 2.1. Requisitos Não-Funcionais (RNF-LEX)

| ID | Requisito Não-Funcional | Critério Técnico Mensurável |
| :--- | :--- | :--- |
| **RNF-LEX-01** | **Complexidade Temporal Linear** | O algoritmo de varredura deve ter complexidade de tempo $\mathcal{O}(N)$, onde $N$ é o comprimento total do código-fonte em caracteres. |
| **RNF-LEX-02** | **Consumo de Memória Auxiliar Limitado** | O consumo de memória auxiliar do scanner deve ser $\mathcal{O}(1)$ por token emitido (independente do tamanho do arquivo). |
| **RNF-LEX-03** | **Determinismo Matemático Estrito** | O autômato implementado deve ser puramente determinístico, livre de transições vazias ($\epsilon$) e sem necessidade de *backtracking*. |
| **RNF-LEX-04** | **Codificação Padrão UTF-8** | O scanner deve operar sobre arquivos codificados em UTF-8 padrão, tratando graciosamente caracteres especiais e pontuação oculta. |
| **RNF-LEX-05** | **Idempotência do Scanner** | Executar a análise léxica repetidas vezes sobre o mesmo arquivo de entrada deve produzir rigorosamente a mesma sequência de tokens e erros. |
| **RNF-LEX-06** | **Interface Desacoplada (Iterator / Generator)** | O módulo do lexer deve disponibilizar tanto o método sob demanda `proximo_token()` para o parser quanto a extração completa de tokens para a CLI. |

### 2.3. Requisitos de Conformidade Acadêmica (RC-UNIFACS — Rubrica do M1)

| Critério Oficial do Edital | Pontuação | Requisitos Vinculados | Evidência Técnica |
| :--- | :---: | :--- | :--- |
| **Reconhece todas as categorias de tokens da especificação** | **3,0 pts** | RF-LEX-01 a 06, 08 a 10 | Bateria de testes de aceitação em `tests/valid/` cobrindo os 15 identificadores, números e pontuação. |
| **Trata corretamente lookahead: =/==, </<=, >/>= e !=** | **1,0 pt** | RF-LEX-07, RF-LEX-15 | Função `espiar()` com desambiguação e teste de `!` inválido em `tests/invalid/`. |
| **Descarta comentários e espaços; rastreia linha e coluna** | **1,0 pt** | RF-LEX-11 a 13 | Comentários com `#` ignorados e rastreamento de coordenadas testado em `tests/valid/`. |
| **Reporta erro léxico com posição correta** | **1,0 pt** | RF-LEX-14, RF-LEX-16 | Saída padronizada `[LÉXICO] Linha L, Coluna C: ...` validada em `tests/invalid/`. |
| **Documenta o AFD por diagrama ou tabela de transição** | **1,5 pts** | RNF-LEX-03 | Seções 5 e 6 deste documento com a 5-tupla formal, diagrama Mermaid e matriz $\delta$. |
| **Inclui suíte de testes com casos válidos e inválidos** | **0,5 pt** | RC-LEX-03 | Diretórios `tests/valid/` e `tests/invalid/` com scripts executáveis. |
| **TOTAL DO MARCO 1** | **8,0 pts** | — | **Aprovação integral dos critérios de avaliação da UNIFACS.** |

---

## ⚙️ 3. Mecânica de Entrada e Buffering (*Input Buffering*)

Para assegurar eficiência de tempo $\mathcal{O}(N)$ e rastreamento de coordenadas sem ambiguidade, o scanner opera sobre um modelo formal de **fita de caracteres unidimensional**:

```text
Código-Fonte:  p  r  o  g  r  a  m  a     f  a  t  o  r  i  a  l  \n  EOF
Posição:       0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17  18
               ^                       ^
               │                       └── ponteiro_atual (forward)
               └────────────────────────── inicio_lexema (lexeme_begin)
```

### 3.1. Primitivas de Manipulação da Fita
1. **`inicio_lexema`**: Ponteiro que marca o índice do caractere onde o token atual começou.
2. **`ponteiro_atual`**: Ponteiro de varredura (*forward*) que avança lendo os caracteres subsequentes.
3. **`avancar() -> str`**: Retorna o caractere atual na posição `ponteiro_atual`, incrementa o ponteiro em 1 e atualiza as coordenadas `coluna += 1` (ou `linha += 1, coluna = 1` caso o caractere consumido seja `\n`).
4. **`espiar(k=1) -> str`**: Realiza o *lookahead* de $k$ posições sem avançar os ponteiros e sem alterar as variáveis de estado de linha/coluna. Retorna o caractere sentinela `\0` caso atinja o fim da fita.
5. **`recuar()`**: Restaura o ponteiro em 1 posição (utilizado quando um estado de aceitação do AFD lê um caractere delimitador que pertence ao próximo token).

---

## ⚖️ 4. Regras Formais de Desambiguação Léxica

### 4.1. Princípio do Casamento Mais Longo (*Maximal Munch*)
Diante de uma sequência que possa casar com mais de um padrão de token, o analisador léxico consome a **maior cadeia de caracteres possível**.  
* Exemplo: Ao encontrar os caracteres `<` e `=`, o scanner avalia se o caractere seguinte forma `<=`. Como `<=` é um padrão válido e mais longo que `<`, ele emite `TK_MENOR_IGUAL` e não `TK_MENOR` seguido de `TK_ATRIB`.

#### Tabela de Desambiguação de Lookahead ($k=1$):
| Caractere Atual | Lookahead (`espiar()`) | Lexema Consumido | Token Emitido | Ação em caso de outro caractere |
| :---: | :---: | :---: | :---: | :--- |
| `=` | `=` | `==` | `TK_IGUAL` | Emite `TK_ATRIB` (`=`) isoladamente |
| `<` | `=` | `<=` | `TK_MENOR_IGUAL` | Emite `TK_MENOR` (`<`) isoladamente |
| `>` | `=` | `>=` | `TK_MAIOR_IGUAL` | Emite `TK_MAIOR` (`>`) isoladamente |
| `!` | `=` | `!=` | `TK_DIFERENTE` | **ERRO LÉXICO**: Caractere `'!'` isolado não existe na MiniLang |

### 4.2. Prioridade de Regras: Palavras-Chave vs. Identificadores
A gramática da MiniLang estabelece que uma palavra reservada (como `enquanto` ou `se`) possui exatamente a mesma forma ortográfica de um identificador (`[A-Za-z_][A-Za-z0-9_]*`).

**Decisão de Arquitetura**:  
Em vez de construir ramos dedicados no AFD para cada uma das 15 palavras reservadas (o que aumentaria o autômato em dezenas de estados redundantes), adota-se a técnica canônica do *Dragon Book*:
1. O AFD transita e aceita a cadeia genérica `[A-Za-z_][A-Za-z0-9_]*` em um estado único de identificador $q_{\text{id}}$;
2. Ao atingir o término do lexema, o scanner consulta uma **Tabela Hash de Palavras Reservadas** ($\mathcal{O}(1)$);
3. Se o lexema estiver presente na tabela, emite o token específico da palavra-chave (`TK_SE`, `TK_ENQUANTO`, etc.);
4. Caso contrário, emite o token genérico `TK_ID`.

---

## 🔤 5. Catálogo Formal de Tokens & Atributos Semânticos (*Reference*)

Cada Token gerado pelo scanner é instanciado formalmente como uma 5-tupla:
$$\text{Token} = \langle \text{tipo}, \text{lexema}, \text{valor}, \text{linha}, \text{coluna} \rangle$$

### 5.1. Tabela de Tokens da MiniLang

| Categoria Formal | Nome do Token (`TokenType`) | Expressão Regular Canônica | Exemplos de Lexema | Atributo Semântico (`valor`) |
| :--- | :--- | :--- | :--- | :--- |
| **Palavra Reservada** | `TK_PROGRAMA` | `programa` | `programa` | `None` |
| **Palavra Reservada** | `TK_VAR` | `var` | `var` | `None` |
| **Palavra Reservada** | `TK_TIPO_INTEIRO` | `inteiro` | `inteiro` | `None` |
| **Palavra Reservada** | `TK_TIPO_BOOLEANO` | `booleano` | `booleano` | `None` |
| **Palavra Reservada** | `TK_SE` | `se` | `se` | `None` |
| **Palavra Reservada** | `TK_SENAO` | `senão` | `senão` | `None` |
| **Palavra Reservada** | `TK_ENQUANTO` | `enquanto` | `enquanto` | `None` |
| **Palavra Reservada** | `TK_ESCREVA` | `escreva` | `escreva` | `None` |
| **Palavra Reservada** | `TK_LEIA` | `leia` | `leia` | `None` |
| **Palavra Reservada** | `TK_FIM` | `fim` | `fim` | `None` |
| **Literal Booleano** | `TK_VERDADEIRO` | `verdadeiro` | `verdadeiro` | `True` (bool nativo) |
| **Literal Booleano** | `TK_FALSO` | `falso` | `falso` | `False` (bool nativo) |
| **Operador Lógico** | `TK_OP_E` | `e` | `e` | `None` |
| **Operador Lógico** | `TK_OP_OU` | `ou` | `ou` | `None` |
| **Operador Lógico** | `TK_OP_NAO` | `não` | `não` | `None` |
| **Identificador** | `TK_ID` | `[A-Za-z_][A-Za-z0-9_]*` | `fatorial`, `x`, `_contador` | `"fatorial"`, `"x"` (str) |
| **Literal Inteiro** | `TK_NUMERO` | `[0-9]+` | `0`, `42`, `1000` | `0`, `42`, `1000` (int nativo) |
| **Operador Aritmético** | `TK_SOMA` | `\+` | `+` | `None` |
| **Operador Aritmético** | `TK_SUB` | `\-` | `-` | `None` |
| **Operador Aritmético** | `TK_MULT` | `\*` | `*` | `None` |
| **Operador Aritmético** | `TK_DIV` | `\/` | `/` | `None` |
| **Operador Aritmético** | `TK_MOD` | `\%` | `%` | `None` |
| **Operador Atribuição** | `TK_ATRIB` | `=` | `=` | `None` |
| **Operador Relacional** | `TK_IGUAL` | `==` | `==` | `None` |
| **Operador Relacional** | `TK_DIFERENTE` | `!=` | `!=` | `None` |
| **Operador Relacional** | `TK_MENOR` | `<` | `<` | `None` |
| **Operador Relacional** | `TK_MENOR_IGUAL` | `<=` | `<=` | `None` |
| **Operador Relacional** | `TK_MAIOR` | `>` | `>` | `None` |
| **Operador Relacional** | `TK_MAIOR_IGUAL` | `>=` | `>=` | `None` |
| **Delimitador** | `TK_ABRE_PAR` | `\(` | `(` | `None` |
| **Delimitador** | `TK_FECHA_PAR` | `\)` | `)` | `None` |
| **Delimitador** | `TK_ABRE_CHAVE` | `\{` | `{` | `None` |
| **Delimitador** | `TK_FECHA_CHAVE` | `\}` | `}` | `None` |
| **Delimitador** | `TK_PONTO_VIRGULA`| `;` | `;` | `None` |
| **Delimitador** | `TK_DOIS_PONTOS` | `:` | `:` | `None` |
| **Delimitador** | `TK_VIRGULA` | `,` | `,` | `None` |
| **Delimitador** | `TK_PONTO` | `\.` | `.` | `None` |
| **Sentinela** | `TK_EOF` | `\0` | `EOF` | `None` |

---

## 📐 6. Modelagem Matemática do Autômato Finito Determinístico (AFD)

O analisador léxico da MiniLang é formalizado matematicamente pela 5-tupla canônica:
$$M = (Q, \Sigma, \delta, q_0, F)$$

### 6.1. Componentes da 5-Tupla
1. **Conjunto Finito de Estados ($Q$)**:
   $$Q = \{ q_0, q_{\text{id}}, q_{\text{num}}, q_{=}, q_{==}, q_{<}, q_{<=}, q_{>}, q_{>=}, q_{!}, q_{!=}, q_{\text{op}}, q_{\text{delim}}, q_{\text{coment}}, q_{\text{erro}} \}$$

2. **Alfabeto de Entrada ($\Sigma$)**:
   Conjunto de todos os caracteres ASCII imprimíveis, caracteres de espaçamento (`\t`, `\r`, `\n`, ` `) e caracteres acentuados suportados em palavras-chave da língua portuguesa (`ã`).
   $$\Sigma = \{ A\dots Z, a\dots z, 0\dots 9, \_, +, -, *, /, \%, =, <, >, !, (, ), \{, \}, ;, :, ,, ., \#, \text{whitespace} \}$$

3. **Estado Inicial ($q_0$)**:
   $q_0 \in Q$ é o estado no qual o autômato inicia a varredura de cada novo token.

4. **Conjunto de Estados Finais / Aceitação ($F$)**:
   $$F = \{ q_{\text{id}}, q_{\text{num}}, q_{=}, q_{==}, q_{<}, q_{<=}, q_{>}, q_{>=}, q_{!=}, q_{\text{op}}, q_{\text{delim}} \}$$
   *(Nota: Estados finais com recuo de fita retrocedem 1 caractere quando o delimitador seguinte pertence ao próximo token).*

---

### 6.2. Diagrama de Transição de Estados (Mermaid State Machine)

```mermaid
stateDiagram-v2
    [*] --> q0: Início da varredura

    %% Espaços e comentários
    q0 --> q0: ' ', '\t', '\r', '\n'\n(Descarta e incrementa L/C)
    q0 --> q_coment: '#'
    q_coment --> q_coment: Qualquer caractere exceto '\n'
    q_coment --> q0: '\n' ou EOF (Descarta comentário)

    %% Identificadores e Palavras Reservadas
    q0 --> q_id: Letra [A-Za-z] ou '_'
    q_id --> q_id: [A-Za-z0-9_]
    q_id --> [*]: Outro caractere\n(Recua 1; Lookup Hash -> TK_ID ou Palavra-Chave)

    %% Literais Inteiros
    q0 --> q_num: Dígito [0-9]
    q_num --> q_num: [0-9]
    q_num --> [*]: Não-dígito\n(Recua 1; Emite TK_NUMERO com valor int)

    %% Atribuição e Igualdade
    q0 --> q_atrib: '='
    q_atrib --> q_igual: '='
    q_igual --> [*]: Emite TK_IGUAL ('==')
    q_atrib --> [*]: Outro caractere\n(Recua 1; Emite TK_ATRIB '=')

    %% Menor e Menor-Igual
    q0 --> q_menor: '<'
    q_menor --> q_menor_igual: '='
    q_menor_igual --> [*]: Emite TK_MENOR_IGUAL ('<=')
    q_menor --> [*]: Outro caractere\n(Recua 1; Emite TK_MENOR '<')

    %% Maior e Maior-Igual
    q0 --> q_maior: '>'
    q_maior --> q_maior_igual: '='
    q_maior_igual --> [*]: Emite TK_MAIOR_IGUAL ('>=')
    q_maior --> [*]: Outro caractere\n(Recua 1; Emite TK_MAIOR '>')

    %% Diferente e Exclamação Inválida
    q0 --> q_excl: '!'
    q_excl --> q_dif: '='
    q_dif --> [*]: Emite TK_DIFERENTE ('!=')
    q_excl --> q_erro: Outro caractere\n(ERRO: '!' solitário)

    %% Operadores Aritméticos Simples
    q0 --> q_op: '+', '-', '*', '/', '%'
    q_op --> [*]: Emite Token Aritmético correspondente

    %% Delimitadores
    q0 --> q_delim: '(', ')', '{', '}', ';', ':', ',', '.'
    q_delim --> [*]: Emite Token Delimitador correspondente

    %% Erro Léxico
    q0 --> q_erro: Símbolo fora de Σ (@, $, ~, etc.)
    q_erro --> [*]: Emite [LÉXICO] Linha L, Col C\n(Modo Pânico: descarta e continua)
```

---

### 6.3. Tabela Completa de Transição de Estados ($\delta: Q \times \Sigma \to Q$)

A tabela a seguir descreve exaustivamente a função de transição $\delta$. Para manter a representação concisa, os caracteres de entrada foram agrupados em classes canônicas:

| Estado Atual | Letra / `_` | Dígito `0-9` | `=` | `<` | `>` | `!` | Aritmético (`+ - * / %`) | Delimitador (`( ) { } ; : , .`) | `#` | `\n` | Espaço / `\t` | Outro / Inválido |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$q_0$ (Inicial)** | $q_{\text{id}}$ | $q_{\text{num}}$ | $q_{=}$ | $q_{<}$ | $q_{>}$ | $q_{!}$ | $q_{\text{op}}$ | $q_{\text{delim}}$ | $q_{\text{coment}}$ | $q_0$ | $q_0$ | $q_{\text{erro}}$ |
| **$q_{\text{id}}$ (ID/Palavra)** | $q_{\text{id}}$ | $q_{\text{id}}$ | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* |
| **$q_{\text{num}}$ (Número)** | Aceita* | $q_{\text{num}}$ | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* |
| **$q_{=}$ (Lido '=')** | Aceita* | Aceita* | $q_{==}$ | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* |
| **$q_{<}$ (Lido '<')** | Aceita* | Aceita* | $q_{<=}$ | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* |
| **$q_{>}$ (Lido '>')** | Aceita* | Aceita* | $q_{>=}$ | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* | Aceita* |
| **$q_{!}$ (Lido '!')** | $q_{\text{erro}}$ | $q_{\text{erro}}$ | $q_{!=}$ | $q_{\text{erro}}$ | $q_{\text{erro}}$ | $q_{\text{erro}}$ | $q_{\text{erro}}$ | $q_{\text{erro}}$ | $q_{\text{erro}}$ | $q_{\text{erro}}$ | $q_{\text{erro}}$ | $q_{\text{erro}}$ |
| **$q_{\text{coment}}$ (Comentário)**| $q_{\text{coment}}$ | $q_{\text{coment}}$ | $q_{\text{coment}}$ | $q_{\text{coment}}$ | $q_{\text{coment}}$ | $q_{\text{coment}}$ | $q_{\text{coment}}$ | $q_{\text{coment}}$ | $q_{\text{coment}}$ | $q_0$ | $q_{\text{coment}}$ | $q_{\text{coment}}$ |

*\*Nota: "Aceita\*" denota que o estado de aceitação emite o token correspondente à cadeia lida até então e **retrocede o caractere lido** para que ele seja processado na próxima chamada do scanner.*

---

## 🚨 7. Rastreamento de Posição e Gestão de Erros Léxicos

### 7.1. Invariantes de Rastreamento Bidimensional $(Linha, Coluna)$
O scanner mantém as coordenadas espaciais rigorosamente atualizadas:
* Inicialização: `linha = 1`, `coluna = 1`.
* Para cada caractere comum: `coluna += 1`.
* Para tabulações `\t`: `coluna += 4` (ou avanço para o próximo múltiplo de 4 colunas).
* Para quebras de linha `\n`: `linha += 1`, `coluna = 1`.
* O token emitido herda a **linha** e a **coluna exatas de início do seu primeiro caractere**.

### 7.2. Política de Recuperação em Modo Descarte (*Panic Mode* Léxico)
Conforme exigido pelo edital da UNIFACS:
1. Ao encontrar um caractere proibido (ex: `@`, `$`, `&`) ou uma exclamação não seguida de igual (`!`), o analisador emite imediatamente o diagnóstico no canal de erro padrão:
   ```text
   [LÉXICO] Linha L, Coluna C: Caractere inválido '@' não reconhecido no alfabeto da MiniLang.
   ```
2. O caractere anômalo é descartado da fita;
3. O autômato retorna ao estado $q_0$ e retoma a leitura no caractere seguinte;
4. **Benefício**: Essa estratégia impede que o compilador encerre a execução no primeiro erro, permitindo que todos os erros léxicos do arquivo sejam identificados em uma única rodada de compilação.

---

## 💻 8. Traço de Execução Passo a Passo (*Concrete Execution Trace*)

Para demonstrar a operacionalidade matemática do AFD, considere a seguinte linha de código MiniLang:

```pascal
se (x <= 10) { # validação
```

### Rastreamento da Máquina de Estados:
| Passo | Caractere | Lookahead | Estado Atual | Próximo Estado | Lexema Acumulado | Token Emitido | Posição $(L, C)$ |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: |
| 1 | `s` | `e` | $q_0$ | $q_{\text{id}}$ | `"s"` | — | (1, 1) |
| 2 | `e` | `' '` | $q_{\text{id}}$ | $q_{\text{id}}$ | `"se"` | — | (1, 1) |
| 3 | `' '` | `(` | $q_{\text{id}}$ | Aceita* | `"se"` | `TK_SE` | (1, 1) |
| 4 | `' '` | `(` | $q_0$ | $q_0$ | `""` | — (ignora espaço) | (1, 3) |
| 5 | `(` | `x` | $q_0$ | $q_{\text{delim}}$ | `"("` | `TK_ABRE_PAR` | (1, 4) |
| 6 | `x` | `' '` | $q_0$ | $q_{\text{id}}$ | `"x"` | — | (1, 5) |
| 7 | `' '` | `<` | $q_{\text{id}}$ | Aceita* | `"x"` | `TK_ID("x")` | (1, 5) |
| 8 | `' '` | `<` | $q_0$ | $q_0$ | `""` | — (ignora espaço) | (1, 6) |
| 9 | `<` | `=` | $q_0$ | $q_{<}$ | `"<"` | — (aciona lookahead) | (1, 7) |
| 10 | `=` | `' '` | $q_{<}$ | $q_{<=}$ | `"<="` | `TK_MENOR_IGUAL` | (1, 7) |
| 11 | `' '` | `1` | $q_0$ | $q_0$ | `""` | — (ignora espaço) | (1, 9) |
| 12 | `1` | `0` | $q_0$ | $q_{\text{num}}$ | `"1"` | — | (1, 10) |
| 13 | `0` | `)` | $q_{\text{num}}$ | $q_{\text{num}}$ | `"10"` | — | (1, 10) |
| 14 | `)` | `' '` | $q_{\text{num}}$ | Aceita* | `"10"` | `TK_NUMERO(10)` | (1, 10) |
| 15 | `)` | `' '` | $q_0$ | $q_{\text{delim}}$ | `")"` | `TK_FECHA_PAR` | (1, 12) |
| 16 | `' '` | `{` | $q_0$ | $q_0$ | `""` | — (ignora espaço) | (1, 13) |
| 17 | `{` | `' '` | $q_0$ | $q_{\text{delim}}$ | `"{"` | `TK_ABRE_CHAVE` | (1, 14) |
| 18 | `' '` | `#` | $q_0$ | $q_0$ | `""` | — (ignora espaço) | (1, 15) |
| 19 | `#` | ` ` | $q_0$ | $q_{\text{coment}}$ | `"#"` | — (entra no comentário) | (1, 16) |
| 20 | $\dots$ | $\dots$ | $q_{\text{coment}}$ | $q_{\text{coment}}$ | — | — (consome até `\n`) | (1, 17-26) |

---

## 🏗️ 9. Arquitetura de Módulos em Python (`src/lexer/`)

O módulo léxico é estruturado em três componentes desacoplados de alta coesão:

```text
src/lexer/
├── __init__.py      # Exporta a classe Lexer, Token e TokenType
├── token.py         # Enum TokenType e dataclass Token com formatação amigável
├── erros.py         # Hierarquia de exceções ErroLexico e formatador de mensagens
└── lexer.py         # Scanner implementando a máquina de estados, buffering e lookahead
```

### 9.1. Responsabilidades de Cada Módulo:
* **`token.py`**: Define o enum `TokenType` contendo as 38 categorias de tokens da MiniLang e a classe `@dataclass Token` que armazena `tipo`, `lexema`, `valor`, `linha` e `coluna`, implementando o método `__repr__` para exibição formatada na CLI.
* **`erros.py`**: Define a classe `ErroLexico(Exception)` contendo `mensagem`, `linha` e `coluna`, garantindo a padronização:
  `[LÉXICO] Linha L, Coluna C: Descrição`.
* **`lexer.py`**: Encapsula a lógica da máquina de estados finitos através da classe `Lexer`. Possui métodos de buffering (`avancar()`, `espiar()`), método iterador `proximo_token()` e o método `tokenizar_tudo()` que gera a lista completa de tokens para a interface de linha de comando.

---

## 🧪 10. Matriz de Verificação & Testes Experimentais (*How-To*)

Para atender integralmente aos critérios do edital e garantir a nota máxima da rubrica (0,5 pt de suíte de testes), o projeto inclui 10 baterias de teste automatizadas divididas em duas classes:

### 10.1. Casos Válidos (`tests/valid/`)
1. **`m1_tokens_palavras_chave.ml`**: Testa o reconhecimento isolado e combinado de todas as 15 palavras reservadas.
2. **`m1_tokens_operadores_relacionais.ml`**: Testa exaustivamente todos os casos de lookahead (`==`, `!=`, `<`, `<=`, `>`, `>=`).
3. **`m1_tokens_expressoes_aritmeticas.ml`**: Testa operadores aritméticos com identificadores e literais numéricos (`+`, `-`, `*`, `/`, `%`).
4. **`m1_comentarios_e_espacos.ml`**: Testa comentários com `#` no início, meio e fim de linhas, garantindo preservação de linhas e colunas.
5. **`m1_programa_fatorial_completo.ml`**: Programa MiniLang completo e funcional demonstrando o pipeline integrado.

### 10.2. Casos Inválidos Provocados (`tests/invalid/`)
1. **`m1_erro_caractere_invalido_arroba.ml`**: Contém o caractere `@` fora do alfabeto, testando reporte exato de linha e coluna.
2. **`m1_erro_caractere_invalido_cifrao.ml`**: Contém identificadores iniciados por `$` (ex: `$preco`).
3. **`m1_erro_exclamacao_solitaria.ml`**: Contém o caractere `!` não seguido de `=`, testando a falha de lookahead.
4. **`m1_erro_multiplos_caracteres_invalidos.ml`**: Testa a recuperação em modo pânico léxico, emitindo múltiplos erros em um único arquivo sem travar o compilador.
5. **`m1_erro_simbolo_especial_e_comercial.ml`**: Testa o caractere `&` solitário (deve sugerir a palavra reservada `e`).

### 10.3. Como Executar a Análise Léxica via CLI:
```bash
# Executa a análise léxica exibindo a tabela formatada de tokens
python minilang.py tests/valid/m1_programa_fatorial_completo.ml --tokens

# Executa teste com erro léxico provocado
python minilang.py tests/invalid/m1_erro_exclamacao_solitaria.ml --tokens
```

---

## 📚 11. Referências Bibliográficas

1. AHO, Alfred V.; LAM, Monica S.; SETHI, Ravi; ULLMAN, Jeffrey D. **Compiladores: princípios, técnicas e ferramentas** (Dragon Book). 2. ed. São Paulo: Pearson Addison Wesley, 2008. (Capítulo 3: Análise Léxica).
2. COOPER, Keith D.; TORCZON, Linda. **Construindo Compiladores**. 2. ed. Rio de Janeiro: Elsevier, 2014. (Capítulo 2: Scanners).
3. MENEZES, Paulo Blauth. **Linguagens formais e autômatos**. 6. ed. Porto Alegre: Bookman, 2011.
4. SANTANA, Daniel. **Aulas 01 a 05: Teoria da Computação e Compiladores**. Universidade Salvador (UNIFACS), 2026.2.
5. SANTANA, Daniel. **Instruções da Avaliação A3 — Projeto MiniLang**. UNIFACS, 2026.
