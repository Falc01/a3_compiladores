"""
Módulo do Analisador Léxico (Scanner) da Linguagem MiniLang
Projeto de Avaliação A3 - Teoria da Computação e Compiladores (0006964)
Universidade Salvador (UNIFACS) - Período Letivo: 2026.2
Docente: Prof. Daniel Santana

Autor / Responsável Técnico pelo Marco 1:
    João Spinola Falcão (RA: 12723116405 | GitHub: @Falc01)
"""

from typing import Optional
from src.lexer.token import Token, TokenType, TABELA_PALAVRAS_RESERVADAS
from src.lexer.erros import ErroLexico


class Lexer:
    """
    Analisador Léxico da MiniLang implementado via Autômato Finito Determinístico (AFD) manual.
    
    Características Técnicas:
        - Complexidade temporal O(N) com memória auxiliar O(1);
        - Rastreamento bidimensional rigoroso de (Linha, Coluna);
        - Lookahead determinístico k=1 para operadores relacionais e de atribuição;
        - Descarte transparente de espaços em branco e comentários '#';
        - Resolução O(1) de palavras reservadas (18 palavras, incluindo Opção D: para, repita, até);
        - Recuperação em Modo Pânico (Panic Mode) para acumular múltiplos erros léxicos.
    """

    def __init__(self, codigo_fonte: str, nome_arquivo: str = ""):
        self.codigo: str = codigo_fonte
        self.tamanho: int = len(codigo_fonte)
        self.posicao: int = 0
        self.linha: int = 1
        self.coluna: int = 1
        self.nome_arquivo: str = nome_arquivo
        self.erros: list[ErroLexico] = []

    # =========================================================================
    # Primitivas de Manipulação da Fita (Input Buffering)
    # =========================================================================

    def fim_de_arquivo(self) -> bool:
        """Verifica se o ponteiro de leitura atingiu o término da cadeia de entrada."""
        return self.posicao >= self.tamanho

    def caractere_atual(self) -> str:
        """Retorna o caractere sob o ponteiro de leitura ou '\\0' se for EOF."""
        if self.fim_de_arquivo():
            return "\0"
        return self.codigo[self.posicao]

    def espiar(self, k: int = 1) -> str:
        """
        Lookahead de k posições à frente sem avançar os ponteiros de estado.
        Por padrão k=1 inspeciona o caractere imediatamente subsequente.
        """
        indice = self.posicao + k - 1
        if indice >= self.tamanho:
            return "\0"
        return self.codigo[indice]

    def avancar(self) -> str:
        """
        Consome o caractere atual e avança o ponteiro de leitura,
        atualizando com precisão as coordenadas espaciais (linha e coluna).
        """
        if self.fim_de_arquivo():
            return "\0"
        
        char = self.codigo[self.posicao]
        self.posicao += 1
        
        if char == "\n":
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1
            
        return char

    # =========================================================================
    # Descarte de Espaços e Comentários
    # =========================================================================

    def _pular_brancos_e_comentarios(self) -> None:
        """
        Consome espaços em branco, tabulações e quebras de linha.
        Descarta comentários iniciados por '#' até o final da linha ou EOF.
        """
        while not self.fim_de_arquivo():
            char = self.caractere_atual()

            # Espaços, tabulações e novas linhas
            if char in (" ", "\t", "\r", "\n"):
                self.avancar()
                continue

            # Comentários de linha única iniciados por '#'
            if char == "#":
                # Consome o '#' e tudo até o '\n' ou EOF
                while not self.fim_de_arquivo() and self.caractere_atual() != "\n":
                    self.avancar()
                # Não consumimos o '\n' aqui para deixar o controle de linha para o loop
                continue

            break

    # =========================================================================
    # Reconhecedores Específicos do AFD
    # =========================================================================

    def _eh_inicio_identificador(self, c: str) -> bool:
        """
        Verifica se o caractere pode iniciar um identificador ou palavra reservada.
        Permite letras ASCII, sublinhado '_' e caracteres acentuados da língua portuguesa.
        """
        return c.isalpha() or c == "_"

    def _eh_corpo_identificador(self, c: str) -> bool:
        """Verifica se o caractere pode compor o corpo de um identificador (letras, dígitos, _)."""
        return c.isalnum() or c == "_"

    def _reconhecer_identificador_ou_palavra_reservada(self) -> Token:
        """
        Reconhece cadeias alfanuméricas e consulta a tabela hash de palavras reservadas O(1).
        Se estiver na tabela, emite o token específico da palavra-chave; caso contrário, emite TK_ID.
        """
        linha_inicio = self.linha
        coluna_inicio = self.coluna
        caracteres: list[str] = []

        while not self.fim_de_arquivo() and self._eh_corpo_identificador(self.caractere_atual()):
            caracteres.append(self.avancar())

        lexema = "".join(caracteres)

        # Resolução de precedência Palavra Reservada vs. Identificador
        if lexema in TABELA_PALAVRAS_RESERVADAS:
            tipo_token = TABELA_PALAVRAS_RESERVADAS[lexema]
            valor: Any = None
            
            # Literais booleanos possuem valor lógico nativo associado
            if tipo_token == TokenType.VERDADEIRO:
                valor = True
            elif tipo_token == TokenType.FALSO:
                valor = False
                
            return Token(
                tipo=tipo_token,
                lexema=lexema,
                valor=valor,
                linha=linha_inicio,
                coluna=coluna_inicio
            )

        # Identificador comum
        return Token(
            tipo=TokenType.ID,
            lexema=lexema,
            valor=lexema,
            linha=linha_inicio,
            coluna=coluna_inicio
        )

    def _reconhecer_numero(self) -> Token:
        """
        Reconhece literais numéricos inteiros [0-9]+ e calcula o valor inteiro nativo.
        """
        linha_inicio = self.linha
        coluna_inicio = self.coluna
        digitos: list[str] = []

        while not self.fim_de_arquivo() and self.caractere_atual().isdigit():
            digitos.append(self.avancar())

        lexema = "".join(digitos)
        valor_int = int(lexema)

        return Token(
            tipo=TokenType.NUMERO,
            lexema=lexema,
            valor=valor_int,
            linha=linha_inicio,
            coluna=coluna_inicio
        )

    # =========================================================================
    # Motor Principal do Scanner
    # =========================================================================

    def proximo_token(self) -> Token:
        """
        Consome a fita de entrada e retorna o próximo Token sintático.
        Implementa recuperação em Modo Pânico: caso encontre caracteres fora do alfabeto,
        registra o erro, descarta o caractere e continua até localizar o próximo token válido.
        """
        while not self.fim_de_arquivo():
            self._pular_brancos_e_comentarios()

            if self.fim_de_arquivo():
                break

            linha_inicio = self.linha
            coluna_inicio = self.coluna
            char = self.caractere_atual()

            # 1. Identificadores e Palavras Reservadas (letras ou _)
            if self._eh_inicio_identificador(char):
                return self._reconhecer_identificador_ou_palavra_reservada()

            # 2. Literais Numéricos Inteiros (dígitos 0-9)
            if char.isdigit():
                return self._reconhecer_numero()

            # 3. Operadores com Lookahead k=1 (=, ==, <, <=, >, >=, !=)
            if char == "=":
                self.avancar()
                if self.caractere_atual() == "=":
                    self.avancar()
                    return Token(TokenType.IGUAL, "==", None, linha_inicio, coluna_inicio)
                return Token(TokenType.ATRIB, "=", None, linha_inicio, coluna_inicio)

            if char == "<":
                self.avancar()
                if self.caractere_atual() == "=":
                    self.avancar()
                    return Token(TokenType.MENOR_IGUAL, "<=", None, linha_inicio, coluna_inicio)
                return Token(TokenType.MENOR, "<", None, linha_inicio, coluna_inicio)

            if char == ">":
                self.avancar()
                if self.caractere_atual() == "=":
                    self.avancar()
                    return Token(TokenType.MAIOR_IGUAL, ">=", None, linha_inicio, coluna_inicio)
                return Token(TokenType.MAIOR, ">", None, linha_inicio, coluna_inicio)

            if char == "!":
                self.avancar()
                if self.caractere_atual() == "=":
                    self.avancar()
                    return Token(TokenType.DIFERENTE, "!=", None, linha_inicio, coluna_inicio)
                
                # Exclamação solitária não existe na especificação da MiniLang
                erro = ErroLexico(
                    mensagem="Caractere '!' solitário é inválido na MiniLang. Operador relacional esperado é '!='.",
                    linha=linha_inicio,
                    coluna=coluna_inicio,
                    caractere="!"
                )
                self.erros.append(erro)
                continue  # Modo pânico: descarta e procura próximo token

            # 4. Operadores Aritméticos Primitivos (+, -, *, /, %)
            if char == "+":
                self.avancar()
                return Token(TokenType.SOMA, "+", None, linha_inicio, coluna_inicio)
            if char == "-":
                self.avancar()
                return Token(TokenType.SUB, "-", None, linha_inicio, coluna_inicio)
            if char == "*":
                self.avancar()
                return Token(TokenType.MULT, "*", None, linha_inicio, coluna_inicio)
            if char == "/":
                self.avancar()
                return Token(TokenType.DIV, "/", None, linha_inicio, coluna_inicio)
            if char == "%":
                self.avancar()
                return Token(TokenType.MOD, "%", None, linha_inicio, coluna_inicio)

            # 5. Delimitadores Estruturais
            if char == "(":
                self.avancar()
                return Token(TokenType.ABRE_PAR, "(", None, linha_inicio, coluna_inicio)
            if char == ")":
                self.avancar()
                return Token(TokenType.FECHA_PAR, ")", None, linha_inicio, coluna_inicio)
            if char == "{":
                self.avancar()
                return Token(TokenType.ABRE_CHAVE, "{", None, linha_inicio, coluna_inicio)
            if char == "}":
                self.avancar()
                return Token(TokenType.FECHA_CHAVE, "}", None, linha_inicio, coluna_inicio)
            if char == ";":
                self.avancar()
                return Token(TokenType.PONTO_VIRGULA, ";", None, linha_inicio, coluna_inicio)
            if char == ":":
                self.avancar()
                return Token(TokenType.DOIS_PONTOS, ":", None, linha_inicio, coluna_inicio)
            if char == ",":
                self.avancar()
                return Token(TokenType.VIRGULA, ",", None, linha_inicio, coluna_inicio)
            if char == ".":
                self.avancar()
                return Token(TokenType.PONTO, ".", None, linha_inicio, coluna_inicio)

            # 6. Caracteres Inválidos (Fora do Alfabeto) - Modo Pânico
            char_invalido = self.avancar()
            mensagem = f"Caractere inválido '{char_invalido}' não reconhecido no alfabeto da MiniLang."
            
            # Diagnósticos amigáveis com sugestão
            if char_invalido == "&":
                mensagem += " Para conjunção lógica, utilize a palavra reservada 'e'."
            elif char_invalido == "|":
                mensagem += " Para disjunção lógica, utilize a palavra reservada 'ou'."
            elif char_invalido == "$":
                mensagem += " O símbolo '$' não é permitido em identificadores."
            elif char_invalido == "@":
                mensagem += " O símbolo '@' não faz parte da sintaxe da MiniLang."

            erro = ErroLexico(
                mensagem=mensagem,
                linha=linha_inicio,
                coluna=coluna_inicio,
                caractere=char_invalido
            )
            self.erros.append(erro)
            # Continua o loop para coletar os próximos tokens válidos ou erros subsequentes

        # Fim de Arquivo (EOF)
        return Token(
            tipo=TokenType.EOF,
            lexema="EOF",
            valor=None,
            linha=self.linha,
            coluna=self.coluna
        )

    def tokenizar_tudo(self) -> tuple[list[Token], list[ErroLexico]]:
        """
        Executa a análise léxica completa do código-fonte até encontrar o token EOF.
        Retorna a lista de todos os tokens identificados e a lista de erros léxicos acumulados.
        """
        tokens: list[Token] = []
        
        while True:
            tok = self.proximo_token()
            tokens.append(tok)
            if tok.tipo == TokenType.EOF:
                break

        return tokens, self.erros
