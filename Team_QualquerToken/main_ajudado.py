# --- main.py atualizado ---

import sys
from antlr4 import *

# --- Importe as classes geradas ---
try:
    from MOCLexer import MOCLexer
    from MOCParser import MOCParser
    from MOCVisitor import MOCVisitor # Usando o seu ficheiro base
except ModuleNotFoundError:
    print("Erro: Classes Lexer/Parser/Visitor não encontradas.")
    print("Execute: antlr4 -Dlanguage=Python3 -visitor MOC.g4")
    sys.exit(1)

# --- Classe Visitor para Geração de Código Intermédio ---
class IntermediateCodeGeneratorVisitor(MOCVisitor):

    def __init__(self):
        self.intermediate_code = [] # Lista para armazenar as 'instruções' intermédias
        self.temp_counter = 0       # Contador para variáveis temporárias simples
        self.label_counter = 0      # Contador para rótulos (labels)

    def new_temp(self):
        """Gera um nome para uma variável temporária."""
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def new_label(self, prefix="L"):
        """Gera um nome para um rótulo único."""
        self.label_counter += 1
        return f"{prefix}{self.label_counter}"

    def add_instruction(self, instruction):
        """Adiciona uma instrução à lista e imprime (para debug)."""
        self.intermediate_code.append(instruction)
        print(f"  -> Gerado CI: {instruction}")

    # --- Métodos Visit Sobrescritos ---

    # Regra inicial
    #def visitPrograma(self, ctx: MOCParser.ProgramaContext):
        #print("Visitando Programa...")
        #self.visitChildren(ctx) # Visita prototipos, corpo, etc.
    def visitPrograma(self, ctx: MOCParser.ProgramaContext):
        print("Visitando Programa...")
        # Processa protótipos (pode ser útil para tabela de símbolos, ignorado aqui)
        # self.visit(ctx.prototipos()) # Descomentar se necessário processar
        # Processa corpo (funções)
        self.visit(ctx.corpo())
        self.add_instruction(('HALT',)) # Adiciona instrução final
        return self.intermediate_code

    # Corpo do programa (contém funções e a principal)
    def visitCorpo(self, ctx:MOCParser.CorpoContext):
        print("Visitando Corpo...")
        return self.visitChildren(ctx) # Visita todas as funções

    # Função (normal ou principal)
    # Poderia gerar labels de início/fim de função, lidar com parâmetros
    def visitFuncao(self, ctx: MOCParser.FuncaoContext):
        func_name = ctx.IDENTIFICADOR().getText()
        print(f"Visitando Funcao: {func_name}")
        self.add_instruction(('FUNC_BEGIN', func_name))
        # Processar parâmetros (ctx.parametros()) - pode envolver alocação
        # Visitar o bloco da função
        self.visit(ctx.bloco())
        self.add_instruction(('FUNC_END', func_name))
        return None  # Não retorna valor diretamente aqui

    def visitFuncaoPrincipal(self, ctx: MOCParser.FuncaoPrincipalContext):
        print(f"Visitando FuncaoPrincipal (main)")
        self.add_instruction(('FUNC_BEGIN', 'main'))
        # Processar parâmetros se houver
        self.visit(ctx.bloco())
        self.add_instruction(('FUNC_END', 'main'))
        return None

    # Bloco de código
    def visitBloco(self, ctx: MOCParser.BlocoContext):
        print(f"Visitando Bloco")
        # Simplesmente visita as instruções dentro do bloco
        return self.visit(ctx.instrucoes())

    # Declaração de Variáveis
    # No código intermédio focado em execução, muitas vezes as declarações
    # não geram código direto, mas atualizam uma tabela de símbolos (não implementada aqui).
    def visitDeclaracao(self, ctx: MOCParser.DeclaracaoContext):
        print(f"Visitando Declaracao: {ctx.getText()}")
        var_type = self.visit(ctx.tipo())  # Obtem o tipo ('int', 'double')
        # Itera sobre a lista de variáveis declaradas
        for var_ctx in ctx.listaVariaveis().variavel():
            var_name = var_ctx.IDENTIFICADOR().getText()
            is_array = var_ctx.ABRECOLCH() is not None
            size = None
            initial_value_repr = None

            if is_array:
                if var_ctx.NUMERO():
                    size = int(var_ctx.NUMERO().getText())
                # Verificar inicialização de array: = {...} ou = reads()
                if var_ctx.blocoArray():
                    initial_value_repr = self.visit(var_ctx.blocoArray())  # Pode gerar N assigns
                elif var_ctx.chamadaReads():
                    initial_value_repr = self.visit(var_ctx.chamadaReads())  # Pode gerar instrução READS_ARRAY
            else:
                # Verificar inicialização de variável simples: = expr
                if var_ctx.expressao():
                    initial_value_repr = self.visit(var_ctx.expressao())

            # Ação: Adicionar à tabela de símbolos (não feito aqui) ou gerar pseudo-instrução
            print(
                f"  -> Declarado: Tipo={var_type}, Nome={var_name}, Array={is_array}, Tamanho={size}, Init={initial_value_repr}")
            # Exemplo de pseudo-instrução (opcional):
            # self.add_instruction(('DECLARE', var_type, var_name, size, initial_value_repr))
            # Se houver valor inicial, gerar instrução ASSIGN
            if not is_array and initial_value_repr is not None:
                self.add_instruction(('ASSIGN', ('VAR', var_name), initial_value_repr))
            # (Inicialização de array precisaria de lógica mais complexa)

        return None  # Declaração não retorna valor de expressão

    def visitBlocoArray(self, ctx: MOCParser.BlocoArrayContext):
        print(f"Visitando BlocoArray: {ctx.getText()}")
        # Visita a lista de valores e retorna a lista de representações
        if ctx.listaValores():
            return self.visit(ctx.listaValores())
        return []  # Retorna lista vazia se não houver valores

    def visitListaValores(self, ctx: MOCParser.ListaValoresContext):
        print(f"Visitando ListaValores: {ctx.getText()}")
        values_repr = []
        for expr_ctx in ctx.expressao():
            values_repr.append(self.visit(expr_ctx))
        return values_repr  # Retorna lista de valores/representações

    # Instrução de Atribuição: target = expression ;
    # Atribuição: target = expression ; (Refinada com base na versão anterior)
    def visitInstrucaoAtribuicao(self, ctx: MOCParser.InstrucaoAtribuicaoContext):
        print(f"Visitando InstrucaoAtribuicao: {ctx.getText()}")
        target_repr = None
        # Assume target é ID ou ID[expr]
        if ctx.IDENTIFICADOR() and ctx.ABRECOLCH() is None:  # Var simples: ID = expr ;
            target_repr = ('VAR', ctx.IDENTIFICADOR().getText())
        elif ctx.IDENTIFICADOR() and ctx.ABRECOLCH():  # Acesso Array: ID [ expr1 ] = expr2 ;
            array_name = ctx.IDENTIFICADOR().getText()
            index_repr = self.visit(ctx.expressao(0))  # Primeira expr é o índice
            target_repr = ('ARRAY_TARGET', array_name, index_repr)
        else:
            print("  AVISO: Estrutura de alvo de atribuição desconhecida.")
            return None

        # A expressão do lado direito é a última na lista de expressões
        rhs_expr_ctx = ctx.expressao(len(ctx.expressao()) - 1)
        expr_result_repr = self.visit(rhs_expr_ctx) if rhs_expr_ctx else None

        if target_repr and expr_result_repr:
            self.add_instruction(('ASSIGN', target_repr, expr_result_repr))
            return None  # Instrução não retorna valor
        return None

    # While: WHILE ( expressao ) bloco
    def visitInstrucaoWhile(self, ctx: MOCParser.InstrucaoWhileContext):
        print(f"Visitando InstrucaoWhile: {ctx.getText()}")
        start_label = self.new_label("WHILE_START")
        end_label = self.new_label("WHILE_END")

        self.add_instruction(('LABEL', start_label))  # Rótulo de início do loop
        cond_repr = self.visit(ctx.expressao())  # Avalia a condição
        # Salta para o fim se a condição for falsa
        self.add_instruction(('IF_FALSE_GOTO', cond_repr, end_label))
        self.visit(ctx.bloco())  # Executa o corpo do loop
        self.add_instruction(('GOTO', start_label))  # Volta ao início para reavaliar
        self.add_instruction(('LABEL', end_label))  # Rótulo de fim do loop
        return None

    # For: FOR ( init ; cond ; incr ) bloco
    def visitInstrucaoFor(self, ctx: MOCParser.InstrucaoForContext):
        print(f"Visitando InstrucaoFor: {ctx.getText()}")
        # Estrutura típica: FOR( init ; cond ; incr ) body
        # init, cond, incr podem estar ausentes
        start_label = self.new_label("FOR_START")
        end_label = self.new_label("FOR_END")

        # 1. Executa inicialização (se existir)
        if ctx.expressaoOuAtribuicao(0):
            print("  -> Processando init do FOR")
            self.visit(ctx.expressaoOuAtribuicao(0))  # Gera código para a inicialização

        # 2. Rótulo de início do loop (verificação da condição)
        self.add_instruction(('LABEL', start_label))

        # 3. Avalia condição (se existir), senão considera true (loop infinito sem break)
        cond_repr = True  # Default se não houver condição
        if ctx.expressao():
            print("  -> Processando cond do FOR")
            cond_repr = self.visit(ctx.expressao())
            # 4. Salta para o fim se a condição for falsa
            self.add_instruction(('IF_FALSE_GOTO', cond_repr, end_label))
        # else: Loop infinito se não houver condição

        # 5. Executa o corpo do loop
        print("  -> Processando corpo do FOR")
        self.visit(ctx.bloco())

        # 6. Executa incremento (se existir)
        if ctx.expressaoOuAtribuicao(1):
            print("  -> Processando incr do FOR")
            self.visit(ctx.expressaoOuAtribuicao(1))  # Gera código para o incremento

        # 7. Volta ao início do loop (para reavaliar condição)
        self.add_instruction(('GOTO', start_label))

        # 8. Rótulo de fim do loop
        self.add_instruction(('LABEL', end_label))
        return None

    # Expressão ou Atribuição (usado no FOR init/incr)
    def visitExpressaoOuAtribuicao(self, ctx: MOCParser.ExpressaoOuAtribuicaoContext):
        print(f"Visitando ExpressaoOuAtribuicao: {ctx.getText()}")
        # Verifica se é uma atribuição (ID = expr) ou apenas uma expressão
        if ctx.ATRIBUICAO():
            # É uma atribuição, vamos gerar o código para ela
            target_repr = ('VAR', ctx.IDENTIFICADOR().getText())
            expr_result_repr = self.visit(ctx.expressao())
            self.add_instruction(('ASSIGN', target_repr, expr_result_repr))
            return None  # Atribuição não retorna valor aqui
        else:
            # É apenas uma expressão, visita-a (pode ter efeitos colaterais como chamadas de função)
            return self.visit(ctx.expressao())  # Retorna a representação da expressão

    # If/Else - Gramática parece lidar com ambiguidade "dangling else"
    # InstrucaoEmparelhada é um if com else garantido (ou um bloco)
    def visitInstrucaoEmparelhada(self, ctx: MOCParser.InstrucaoEmparelhadaContext):
        print(f"Visitando InstrucaoEmparelhada: {ctx.getText()}")
        if ctx.IF():  # É um IF com ELSE
            cond_repr = self.visit(ctx.expressao())
            else_label = self.new_label("IF_ELSE")
            end_if_label = self.new_label("IF_END")

            self.add_instruction(('IF_FALSE_GOTO', cond_repr, else_label))
            print("  -> Processando Bloco THEN")
            self.visit(ctx.bloco())  # Bloco do THEN
            self.add_instruction(('GOTO', end_if_label))
            self.add_instruction(('LABEL', else_label))
            print("  -> Processando Bloco ELSE")
            self.visit(ctx.instrucaoEmparelhada())  # O ELSE contém outra instrução emparelhada
            self.add_instruction(('LABEL', end_if_label))
        elif ctx.bloco():  # É apenas um bloco (caso base da recursão do else?)
            self.visit(ctx.bloco())
        return None

    # InstrucaoPorEmparelhar é um if sem else, ou um if com else que termina numa instrução sem else
    def visitInstrucaoPorEmparelhar(self, ctx: MOCParser.InstrucaoPorEmparelharContext):
        print(f"Visitando InstrucaoPorEmparelhar: {ctx.getText()}")
        # Tem sempre IF
        cond_repr = self.visit(ctx.expressao())
        end_if_label = self.new_label("IF_END")  # Usado se não houver else

        if ctx.ELSE():  # IF com ELSE (mas o else é "por emparelhar")
            else_label = self.new_label("IF_ELSE")
            self.add_instruction(('IF_FALSE_GOTO', else_label))
            print("  -> Processando Bloco THEN (Por Emparelhar)")
            self.visit(ctx.bloco())  # Bloco do THEN
            # NÃO temos GOTO end_if aqui, pois o else segue
            self.add_instruction(('LABEL', else_label))
            print("  -> Processando ELSE (Por Emparelhar)")
            self.visit(ctx.instrucaoPorEmparelhar())  # Visita a instrução do ELSE
            # O end_if_label deste if interno será tratado recursivamente
        else:  # IF sem ELSE
            self.add_instruction(('IF_FALSE_GOTO', end_if_label))
            print("  -> Processando Bloco THEN (Sem Else)")
            self.visit(ctx.bloco())  # Bloco do THEN
            self.add_instruction(('LABEL', end_if_label))
        return None

    # Return: RETURN expressao ;
    def visitInstrucaoReturn(self, ctx: MOCParser.InstrucaoReturnContext):
        print(f"Visitando InstrucaoReturn: {ctx.getText()}")
        value_repr = self.visit(ctx.expressao())
        self.add_instruction(('RETURN', value_repr))
        return None

    # Chamadas de função explícitas (READ, READC, READS) - tratadas como primárias
    # O visitor visitará visitChamadaFuncao quando encontrar READ()/etc numa expressão
    def visitChamadaFuncao(self, ctx: MOCParser.ChamadaFuncaoContext):
        print(f"Visitando ChamadaFuncao (Leitura): {ctx.getText()}")
        temp_var = self.new_temp()
        if ctx.READ():
            self.add_instruction(('READ_INT', temp_var))
        elif ctx.READC():
            self.add_instruction(('READ_CHAR', temp_var))
        elif ctx.READS():
            self.add_instruction(('READ_STR', temp_var))  # Renomeado para clareza
        return ('TEMP', temp_var)  # Retorna o temporário onde o valor lido está

    # Instruções de escrita
    def visitInstrucaoEscrita(self, ctx: MOCParser.InstrucaoEscritaContext):
        print(f"Visitando InstrucaoEscrita: {ctx.getText()}")
        if ctx.WRITE() or ctx.WRITEC():  # write(expr); writec(expr);
            value_repr = self.visit(ctx.expressao())
            op_code = 'WRITE_INT' if ctx.WRITE() else 'WRITE_CHAR'
            self.add_instruction((op_code, value_repr))
        elif ctx.WRITEV():  # writev(ID); Assume ID é array
            var_name = ctx.IDENTIFICADOR().getText()
            self.add_instruction(('WRITE_VAR_ARRAY', ('VAR', var_name)))  # Instrução específica
        elif ctx.WRITES():  # writes(string_arg);
            arg_repr = self.visit(ctx.argumentoString())
            # visitArgumentoString retorna string literal ou ('VAR_STRING_ARG?', name)
            if isinstance(arg_repr, tuple):  # É uma variável
                self.add_instruction(('WRITE_VAR_STRING', arg_repr))  # Assumindo var contém string
            else:  # É literal
                self.add_instruction(('WRITE_STRING', arg_repr))
        return None

    # Outros métodos visit já implementados na resposta anterior:
    # visitNumero, visitNumeroReal, visitIdComPrefixo, visitArgumentos,
    # visitParenteses, visitAdicao, visitSubtracao, visitMultiplicacao,
    # visitDivisao, visitModulo, visitNegacao, visitUnarioNegativo

    # Métodos que apenas delegam (podem ser omitidos se não fizerem nada extra):
    # visitExpressao, visitExpressaoOr, visitExpressaoAnd, visitExpressaoEquality,
    # visitExpressaoAdd, visitExpressaoMul, visitExpressaoUnaria, visitCastExpr, visitPrimary
    # A implementação padrão (self.visitChildren) já faz a travessia correta devido à
    # forma como sobrescrevemos os métodos específicos das alternativas rotuladas (Adicao, Subtracao etc)

    # Método para o tipo (usado em declarações, etc.)
    def visitTipo(self, ctx: MOCParser.TipoContext):
        # Apenas retorna o nome do tipo como string
        return ctx.getText()

    # Nota: Muitos outros métodos visit... existem no MOCVisitor.py base.
    # Se não os sobrescrevermos, eles simplesmente chamarão self.visitChildren(ctx),
    # o que pode ser suficiente para muitas regras estruturais (como blocos,
    # listas de instruções, etc.), mas insuficiente para regras que exigem
    # geração de código específica.

    # Literal Número Inteiro
    def visitNumero(self, ctx: MOCParser.NumeroContext):
        print(f"Visitando Numero: {ctx.getText()}")
        # ctx.NUMERO() retorna o nó do token, .getText() pega o texto
        return int(ctx.NUMERO().getText())

    # Literal Número Real
    def visitNumeroReal(self, ctx: MOCParser.NumeroRealContext):
        print(f"Visitando NumeroReal: {ctx.getText()}")
        return float(ctx.NUM_REAL().getText())

    # Literal String
    def visitArgumentoString(self, ctx: MOCParser.ArgumentoStringContext):
         print(f"Visitando ArgumentoString: {ctx.getText()}")
         if ctx.STRINGLITERAL():
             # Remove as aspas do início e fim
             text = ctx.STRINGLITERAL().getText()
             return text[1:-1]
         # Se for IDENTIFICADOR (ex: nome de array para 'writes'), tratar diferente?
         # Por agora, vamos assumir que queremos o valor literal.
         # Se precisar do ID, pode ter lógica condicional aqui.
         elif ctx.IDENTIFICADOR():
             # Retorna representação de variável, talvez? Depende do uso.
             return ('VAR_STRING_ARG?', ctx.IDENTIFICADOR().getText())
         return None


    # Expressão Primária: ID seguido (ou não) de [] ou ()
    # Esta regra parece agregar vários casos, vamos tratar aqui
    def visitIdComPrefixo(self, ctx: MOCParser.IdComPrefixoContext):
        print(f"Visitando IdComPrefixo: {ctx.getText()}")
        identificador = ctx.IDENTIFICADOR().getText()
        # O nó 'primaryRest' diz-nos o que vem a seguir ao ID
        rest = ctx.primaryRest()

        if isinstance(rest, MOCParser.AcessoVetorContext):
            # É um acesso a array: ID [ expressao ]
            print(f"  -> Acesso a Vetor: {identificador}")
            index_repr = self.visit(rest.expressao())
            # Poderia gerar código para calcular endereço aqui se fosse o caso
            # Por agora, retorna uma representação estruturada
            return ('ARRAY_ACCESS', identificador, index_repr)
        elif isinstance(rest, MOCParser.ChamadaGenericaContext):
            # É uma chamada de função: ID ( argumentos )
            print(f"  -> Chamada de Função: {identificador}")
            args_repr_list = []
            if rest.argumentos():
                 args_repr_list = self.visit(rest.argumentos()) # visitArgumentos retorna a lista
            # Retorna representação da chamada
            return ('FUNC_CALL', identificador, args_repr_list)
        elif isinstance(rest, MOCParser.SemSufixoContext):
            # É uma variável simples: ID
            print(f"  -> Variável Simples: {identificador}")
            return ('VAR', identificador)
        else:
            # Caso inesperado
            print(f"  AVISO: Tipo de primaryRest desconhecido após {identificador}")
            return ('VAR', identificador) # Palpite

    # Argumentos de uma função (lista de expressões)
    def visitArgumentos(self, ctx: MOCParser.ArgumentosContext):
        print(f"Visitando Argumentos: {ctx.getText()}")
        args_list = []
        for expr_ctx in ctx.expressao(): # ctx.expressao() retorna lista de contextos
            args_list.append(self.visit(expr_ctx))
        return args_list # Retorna a lista de representações dos argumentos

    # Expressão entre Parênteses
    def visitParenteses(self, ctx: MOCParser.ParentesesContext):
        print(f"Visitando Parenteses: {ctx.getText()}")
        # Visita e retorna o resultado da expressão interior
        return self.visit(ctx.expressao())

    # Operações Aditivas
    def visitAdicao(self, ctx: MOCParser.AdicaoContext):
        print(f"Visitando Adicao: {ctx.getText()}")
        left_repr = self.visit(ctx.expressaoAdd())  # Operando esquerdo (recursivo no mesmo nível)
        right_repr = self.visit(ctx.expressaoMul()) # Operando direito (nível de precedência abaixo)
        temp_var = self.new_temp()
        instruction = ('ADD', temp_var, left_repr, right_repr)
        self.intermediate_code.append(instruction)
        print(f"  -> Gerado CI: {instruction}")
        return ('TEMP', temp_var) # Retorna o temporário onde o resultado está

    def visitSubtracao(self, ctx: MOCParser.SubtracaoContext):
        print(f"Visitando Subtracao: {ctx.getText()}")
        left_repr = self.visit(ctx.expressaoAdd())
        right_repr = self.visit(ctx.expressaoMul())
        temp_var = self.new_temp()
        instruction = ('SUB', temp_var, left_repr, right_repr)
        self.intermediate_code.append(instruction)
        print(f"  -> Gerado CI: {instruction}")
        return ('TEMP', temp_var)

    # Operações Multiplicativas
    def visitMultiplicacao(self, ctx: MOCParser.MultiplicacaoContext):
        print(f"Visitando Multiplicacao: {ctx.getText()}")
        left_repr = self.visit(ctx.expressaoMul()) # Operando esquerdo (recursivo)
        right_repr = self.visit(ctx.expressaoUnaria()) # Operando direito (nível abaixo)
        temp_var = self.new_temp()
        instruction = ('MUL', temp_var, left_repr, right_repr)
        self.intermediate_code.append(instruction)
        print(f"  -> Gerado CI: {instruction}")
        return ('TEMP', temp_var)

    def visitDivisao(self, ctx: MOCParser.DivisaoContext):
        print(f"Visitando Divisao: {ctx.getText()}")
        left_repr = self.visit(ctx.expressaoMul())
        right_repr = self.visit(ctx.expressaoUnaria())
        temp_var = self.new_temp()
        instruction = ('DIV', temp_var, left_repr, right_repr)
        self.intermediate_code.append(instruction)
        print(f"  -> Gerado CI: {instruction}")
        return ('TEMP', temp_var)

    def visitModulo(self, ctx: MOCParser.ModuloContext):
        print(f"Visitando Modulo: {ctx.getText()}")
        left_repr = self.visit(ctx.expressaoMul())
        right_repr = self.visit(ctx.expressaoUnaria())
        temp_var = self.new_temp()
        instruction = ('MOD', temp_var, left_repr, right_repr)
        self.intermediate_code.append(instruction)
        print(f"  -> Gerado CI: {instruction}")
        return ('TEMP', temp_var)

    # Operações Unárias
    def visitNegacao(self, ctx: MOCParser.NegacaoContext):
        print(f"Visiting Negacao: {ctx.getText()}")
        operand_repr = self.visit(ctx.expressaoUnaria()) # Visita a expressão que está a ser negada
        temp_var = self.new_temp()
        instruction = ('NOT', temp_var, operand_repr)
        self.intermediate_code.append(instruction)
        print(f"  -> Gerado CI: {instruction}")
        return ('TEMP', temp_var)

    def visitUnarioNegativo(self, ctx: MOCParser.UnarioNegativoContext):
        print(f"Visiting UnarioNegativo: {ctx.getText()}")
        operand_repr = self.visit(ctx.expressaoUnaria())
        # Poderia gerar instrução ou tentar otimizar (ex: return -valor se operando for literal)
        temp_var = self.new_temp()
        instruction = ('NEG', temp_var, operand_repr) # Menos unário
        self.intermediate_code.append(instruction)
        print(f"  -> Gerado CI: {instruction}")
        return ('TEMP', temp_var)

    # --- Implementar Visit para outras regras: ---
    # visitDeclaracao, visitInstrucaoWhile, visitInstrucaoFor, visitInstrucaoEmparelhada (If/Else),
    # visitInstrucaoReturn, visitChamadaFuncao, visitInstrucaoEscrita, etc.
    # A lógica dependerá do código intermédio que quer gerar para estas estruturas.

# --- Função main (inalterada, chama o visitor) ---
def main(argv):
    # ... (setup lexer, parser, get tree) ...
    input_file_path = argv[1]
    input_stream = FileStream(input_file_path, encoding='utf-8')
    lexer = MOCLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MOCParser(stream)
    tree = parser.programa()

    if parser.getNumberOfSyntaxErrors() > 0:
        print("\n!!! Erros de sintaxe encontrados. Abortando geração de código intermédio. !!!")
        sys.exit(1)

    print("\n--- A iniciar Geração de Código Intermédio ---")
    visitor = IntermediateCodeGeneratorVisitor()
    codigo_intermedio_final = visitor.visit(tree) # Começa a visita
    print("--- Geração de Código Intermédio Concluída ---")

    print("\n--- Código Intermédio Resultante ---")
    if codigo_intermedio_final: # Que é a lista self.intermediate_code
        for instrucao in codigo_intermedio_final:
            print(instrucao)
    else:
        print("(Nenhuma instrução gerada ou retornada pelo visitor principal)")

if __name__ == '__main__':
    main(sys.argv)