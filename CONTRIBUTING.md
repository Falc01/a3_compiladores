# 🤝 Guia de Contribuição e Governança Git — MiniLang

Este documento estabelece as diretrizes de versionamento, fluxo de trabalho e padrões de desenvolvimento para a equipe da **A3 MiniLang** (UNIFACS 2026.2).

---

## 👥 1. Divisão Formal de Trabalho na Equipe

A equipe é composta por **3 integrantes**. Para garantir a clareza de escopo e domínio técnico exigido na arguição individual, o trabalho é estruturado em responsabilidades dedicadas para os Marcos 1 a 3, e integração conjunta no Marco 4:

1. **Marco 1 — Analisador Léxico (`Membro 1`)**:
   - Especificação e desenho formal do AFD (Autômato Finito Determinístico);
   - Implementação do Scanner e tabela de tokens em `src/lexer/`;
   - Tratamento de lookahead (`=`, `==`, `<`, `<=`, `>`, `>=`, `!=`) e descarte de comentários `#`;
   - Rastreamento estrito de linha e coluna;
   - Suíte de testes do M1 e relatório de 1 página.

2. **Marco 2 — Analisador Sintático & AST (`Membro 2`)**:
   - Modelagem da gramática formal EBNF da MiniLang;
   - Implementação do parser descendente recursivo em `src/parser/`;
   - Construção dos nós da Árvore Sintática Abstrata (AST);
   - Implementação da recuperação de erros sintáticos em **Modo Pânico**;
   - Resolução e documentação do problema do *dangling else*.

3. **Marco 3 — Analisador Semântico & Tipos (`Membro 3`)**:
   - Implementação da Tabela de Símbolos com escopos aninhados em `src/semantic/`;
   - Checagem e inferência estrita de tipos (`inteiro` e `booleano`);
   - Detecção de variáveis não declaradas, redeclarações e condições não-booleanas;
   - Anotação da AST com tipos validados;
   - Implementação do bônus de detecção de variável não inicializada.

4. **Marco 4 — Back-End, Otimização e Apresentação (`Equipe Completa`)**:
   - Integração completa do compilador/interpretador em `src/backend/`;
   - Implementação da otimização de código (*Constant Folding*);
   - Redação do Relatório Técnico final (artigo de 6 a 10 páginas);
   - Preparação dos slides e ensaio para a demonstração ao vivo e arguição oral individual.

---

## 🌿 2. Estrutura de Branches (Git Flow)

Para evitar conflitos de merge e garantir estabilidade, seguimos um modelo simplificado de branches:

```text
main           (Apenas entregas estáveis e tags de marcos: v1.0-m1, v2.0-m2, etc.)
  │
develop        (Branch de integração contínua da equipe)
  │
  ├── feature/m1-lexer        (Trabalho do Membro 1 no Marco 1)
  ├── feature/m2-parser       (Trabalho do Membro 2 no Marco 2)
  ├── feature/m3-semantic     (Trabalho do Membro 3 no Marco 3)
  └── feature/m4-backend      (Trabalho conjunto no Marco 4)
```

### Regras de Ouro de Branches:
* **Nenhum membro faz commit direto na branch `main`**.
* O desenvolvimento de novas funcionalidades ocorre em branches `feature/*`.
* Ao concluir uma etapa, o membro abre um Pull Request para a branch `develop`.
* A branch `main` só recebe merges a partir de `develop` quando o marco estiver 100% testado e aprovado.

---

## ✍️ 3. Padrão de Commits Semânticos (PT-BR)

Para manter o histórico do repositório legível, profissional e demonstrar a evolução contínua para o professor, todos os commits devem seguir o padrão semântico em **Português**:

| Prefixo | Significado | Exemplo Prático |
| :--- | :--- | :--- |
| `feat:` | Nova funcionalidade adicionada | `feat: implementa scanner com lookahead para operadores relacionais` |
| `fix:` | Correção de defeito ou bug | `fix: corrige contagem de coluna ao ignorar comentarios com hashtag` |
| `test:` | Adição ou alteração de testes | `test: adiciona casos invalidos para variaveis com caracteres especiais` |
| `docs:` | Alterações em documentação | `docs: adiciona tabela de transicoes de estados do AFD no M1` |
| `refactor:` | Refatoração de código sem alterar regra | `refactor: modulariza definicao dos tipos de token em modulo proprio` |
| `chore:` | Tarefas de build, gitignore ou setup | `chore: configura gitignore e estrutura basica de pastas` |

---

## ⚠️ 4. Política Anti-Penalização de Processo

> **Aviso Oficial do Professor**: *"O histórico de commits conta como evidência de processo; commit único na véspera será penalizado."*

Para garantir nota máxima no critério de processo:
1. Faça commits **atômicos e frequentes** (a cada função implementada ou teste criado).
2. Cada membro deve commitar a partir do seu próprio usuário Git configurado (`git config user.name` e `git config user.email`).
3. Nunca acumule semanas de trabalho para commitar em bloco nas horas finais antes do prazo.

---

## 🚨 5. Padrão Obrigatório de Mensagens de Erro

O compilador **deve obrigatoriamente** emitir erros detalhados contendo:
- **Fase** da compilação (`[LÉXICO]`, `[SINTÁTICO]` ou `[SEMÂNTICO]`);
- **Linha** e **Coluna** exatas onde a anomalia foi detectada;
- **Mensagem descritiva** e objetiva.

### Formato Padrão:
```text
[LÉXICO] Linha 12, Coluna 5: Caractere inválido '@' não reconhecido no alfabeto da MiniLang.
[SINTÁTICO] Linha 18, Coluna 14: Era esperado ';' após o comando de atribuição, mas foi encontrado 'fim'.
[SEMÂNTICO] Linha 25, Coluna 8: A variável 'resultado' foi utilizada sem declaração prévia.
```

---

## 🔍 6. Revisão por Pares (Code Review) & Preparação para a Arguição

Lembre-se de que na apresentação final (M4), haverá **arguição oral individual**. Se um integrante desconhecer como o código funciona, haverá penalização individual ou em grupo.

* **Revisão Obrigatória**: Antes de integrar uma branch em `develop`, os outros integrantes devem ler o código e entender o que foi feito.
* **Mini-Reuniões Semanais**: Recomendamos que a equipe faça reuniões curtas de 15 minutos para que o responsável pelo marco apresente o que programou para os colegas.
