from ..antrl.MOCVisitor import MOCVisitor
from ..utils.TabelaSimbolos import TabelaDeSimbolos, Variavel, Funcao


# Classe responsável pela análise semântica do programa
class VisitorSemantico(MOCVisitor):
    def __init__(self, tabela_simbolos: TabelaDeSimbolos):
        self.contexto = []             # Pilha de contexto de variáveis
        self.lista_erros = []               # Lista de mensagens de erro semântico
        self.funcoes_declaradas = set()  # Guarda os nomes de funções declaradas (prototipos + definidas)
        self.variaveis_com_erro = set()  # # Guarda os nomes de funções declaradas (prototipos + definidas)
        self.tabela_simbolos = tabela_simbolos # Tabela de simbolos
        self.funcao_atual_info = None  # Para rastrear informações da função atual (ex: tipo de retorno)

    def erros(self, arvore):
        self.visit(arvore)
        if self.lista_erros:
            raise Exception("\n".join(self.lista_erros))

    # Visita o nó 'programa' (nó raiz da árvore)
    def visitPrograma(self, ctx):
        if ctx.prototipos():
            self.visit(ctx.prototipos())
        if ctx.corpo():
            self.visit(ctx.corpo())

    # Visita o corpo principal do programa (funções + função principal)
    def visitCorpo(self, ctx):
        for unidade in ctx.unidade():
            self.visit(unidade)
        self.visit(ctx.funcaoPrincipal())

    # Visita a função principal
    def visitFuncaoPrincipal(self, ctx):
        self.contexto.append(set())  # Cria um novo contexto para toda a função principal
        self.tabela_simbolos.entrar_contexto()

        if ctx.parametros():
            parametros = self.visitParametros(ctx.parametros())
            for param in parametros:
                if not self.tabela_simbolos.declarar(param):
                    self.lista_erros.append(
                        f"[Erro semântico] Parâmetro '{param.nome}' já foi declarado."
                    )
                self.contexto[-1].add(param.nome)  # Facultativo, se ainda usares `self.contexto` para lookup

        self.visitBloco(ctx.bloco(), novo_contexto=False)  # NÃO cria novo contexto aqui

        self.contexto.pop()  # Sai do contexto após a função terminar

    def visitTipo(self, ctx) -> str:
        """
        Visita um nó de tipo e retorna sua representação em string.
        """
        if not ctx: return "tipo_desconhecido" # Caso o contexto do tipo seja nulo
        if hasattr(ctx, 'INT') and ctx.INT(): return "int"
        if hasattr(ctx, 'DOUBLE') and ctx.DOUBLE(): return "double"
        if hasattr(ctx, 'STRING') and ctx.STRING(): return "string"
        if hasattr(ctx, 'VOID') and ctx.VOID(): return "void"
        return ctx.getText() # Fallback

    def visitParametro(self, ctx):
        """Processa um único parâmetro, retornando objeto Variavel"""
        nome = ctx.IDENTIFICADOR().getText() if ctx.IDENTIFICADOR() else f"param_{ctx.start.line}"
        tipo = self.visit(ctx.tipo()) if ctx.tipo() else "void"
        linha = ctx.start.line

        return Variavel(
            nome=nome,
            tipo=tipo,
            linha_declaracao=linha,
            eh_parametro=True,
            posicao=len(self.tabela_simbolos.pilha_contextos[-1]) + 1
        )

    def visitParametros(self, ctx) -> list[Variavel]:
        """Retorna uma lista de objetos Variavel representando os parâmetros."""
        parametros = []
        if ctx and hasattr(ctx, 'parametro') and ctx.parametro():
            for i, p_ctx in enumerate(ctx.parametro(), start=1):
                nome = p_ctx.IDENTIFICADOR().getText() if p_ctx.IDENTIFICADOR() else f"param_{i}"
                tipo = self.visit(p_ctx.tipo()) if hasattr(p_ctx, 'tipo') and p_ctx.tipo() else "unknown"
                linha = p_ctx.IDENTIFICADOR().getSymbol().line if p_ctx.IDENTIFICADOR() else 0

                parametros.append(
                    Variavel(
                        nome=nome,
                        tipo=tipo,
                        linha_declaracao=linha,
                        # Remove natureza daqui e define na classe Variavel
                        eh_parametro=True,
                        posicao=i
                    )
                )
        elif ctx and hasattr(ctx, 'tipo') and ctx.tipo(): #só um parametro
            tipo = self.visit(ctx.tipo())

            nome = f"param_1" #p_ctx.IDENTIFICADOR().getText() if p_ctx.IDENTIFICADOR() else f"param_1"
            tipo = self.visit(ctx.tipo()) if hasattr(ctx, 'tipo') and ctx.tipo() else "unknown"

            linha = ctx.start.line  # Fallback padrão

            # Verificação completa em 2 etapas:
            if (hasattr(ctx, 'IDENTIFICADOR') and ctx.IDENTIFICADOR()):
                linha = ctx.IDENTIFICADOR().getSymbol().line

            parametros.append(
                Variavel(
                    nome=nome,
                    tipo=tipo,
                    linha_declaracao=linha,
                    # Remove natureza daqui e define na classe Variavel
                    eh_parametro=True,
                    posicao=1
                )
            )

        return parametros

    # Visita uma função comum (não principal)
    def visitFuncao(self, ctx):
        # Cria novo contexto léxico (já tratado na tabela de símbolos)
        nome_funcao = ctx.IDENTIFICADOR().getText()
        linha_declaracao = ctx.IDENTIFICADOR().getSymbol().line

        self.funcao_atual_info=nome_funcao # colocar a none no return

        # Determina tipo de retorno
        tipo_retorno = "void"
        if hasattr(ctx, 'tipo') and ctx.tipo():
            tipo_retorno = ctx.tipo().getText()

        # Processa parâmetros
        parametros = []
        if hasattr(ctx, 'parametros') and ctx.parametros():
            parametros = self.visitParametros(ctx.parametros())  # Retorna lista de dicionários

        # Declara parâmetros no escopo:
        for param in parametros:
            if isinstance(param, dict):  # Se usar a versão com dicionários
                var_param = Variavel(
                    nome=param['nome'],
                    tipo=param['tipo'],
                    linha_declaracao=param['linha'],
                    natureza="parametro",
                    valor_inicial=0
                )
            else:  # Se usar a versão com classes
                var_param = param

            self.tabela_simbolos.declarar(var_param)

        # Cria objeto Funcao
        nova_funcao = Funcao(
            nome=nome_funcao,
            tipo_retorno=tipo_retorno,
            parametros=parametros,
            linha_declaracao=linha_declaracao,
            natureza="funcao_definida"  # Assume definição direta (verificamos protótipo depois)
        )

        # Verifica se já existe declaração
        simbolo_existente = self.tabela_simbolos.buscar(nome_funcao)

        if simbolo_existente:
            # Caso 1: Já existe um protótipo
            if isinstance(simbolo_existente, Funcao) and simbolo_existente.natureza == "prototipo_funcao":
                # Compara tipos de retorno
                if simbolo_existente.tipo_retorno != tipo_retorno:
                    self.lista_erros.append(
                                        f"[Erro semântico] Tipo de retorno incompatível para '{nome_funcao}' (esperado: {simbolo_existente.tipo_retorno}, obtido: {tipo_retorno})")
                    return
                # Compara APENAS os tipos dos parâmetros (ignorando nomes)
                tipos_esperados = [p.tipo if isinstance(p, Variavel) else p['tipo'] for p in
                                   simbolo_existente.parametros]
                tipos_recebidos = [p.tipo if isinstance(p, Variavel) else p['tipo'] for p in parametros]

                if tipos_esperados != tipos_recebidos:
                    self.lista_erros.append(
                                        f"[Erro semântico] Parâmetros incompatíveis para '{nome_funcao}'\n"
                                        f"Esperado: ({', '.join(tipos_esperados)})\n"
                                        f"Recebido: ({', '.join(tipos_recebidos)})")
                    return

                    # Atualiza o protótipo para implementação
                simbolo_existente.natureza = "funcao_definida"
                simbolo_existente.linha_declaracao = linha_declaracao
                simbolo_existente.parametros = parametros  # Agora com nomes dos parâmetros


            # Caso 2: Redefinição inválida
            else:
                self.lista_erros.append(
                    f"[Erro semântico] Redefinição inválida de '{nome_funcao}' (já declarado como {simbolo_existente.natureza})"
                )
                return
        else:
            # Declara nova função
            if not self.tabela_simbolos.declarar(nova_funcao):
                self.lista_erros.append(
                    f"[Erro semântico] Erro ao declarar função '{nome_funcao}'"
                )
                return

        # Entra no escopo da função
        self.tabela_simbolos.entrar_contexto()

        # Declara parâmetros como variáveis locais
        for param in parametros:

            if not self.tabela_simbolos.declarar(param):
                self.lista_erros.append(
                    f"[Erro semântico] Parâmetro '{param['nome']}' redeclarado"
                )

        # Visita bloco da função
        self.visitBloco(ctx.bloco(), False)

        # Sai do escopo
        self.tabela_simbolos.sair_contexto()

    # Visita um bloco de código entre chavetas
    def visitBloco(self, ctx, novo_contexto=True):
       if novo_contexto:
           self.contexto.append(set())  # Novo contexto local (ex: dentro de if/while)
           # Entra no contexto do bloco
           self.tabela_simbolos.entrar_contexto()

       if ctx.instrucoes():
           self.visit(ctx.instrucoes())

       if novo_contexto:
           self.contexto.pop()  # Fim do contexto local
           # Entra no contexto do bloco
           self.tabela_simbolos.sair_contexto()

    # Visita todas as instruções dentro de um bloco
    def visitInstrucoes(self, ctx):
        for instr in ctx.instrucao():
            self.visit(instr)

    # Encaminha a visita para o tipo de instrução correto
    def visitInstrucao(self, ctx):
        if ctx.instrucaoEmparelhada():
            self.visit(ctx.instrucaoEmparelhada())
        elif ctx.instrucaoPorEmparelhar():
            self.visit(ctx.instrucaoPorEmparelhar())
        elif ctx.outraInstrucao():
            self.visit(ctx.outraInstrucao())

    # Visita uma instrução 'if...else'
    def visitInstrucaoEmparelhada(self, ctx):
        if ctx.expressao():
            self.visit(ctx.expressao())               # Verifica a condição
            self.visit(ctx.instrucaoEmparelhada())    # Verifica os blocos if/else
        else:
            self.visit(ctx.bloco())                   # Apenas bloco else

    # Visita uma instrução 'if' sem 'else'
    def visitInstrucaoPorEmparelhar(self, ctx):
        self.visit(ctx.expressao())  # Verifica a condição
        self.visit(ctx.bloco())      # Verifica o bloco 'then'

    # Trata instruções genéricas
    def visitOutraInstrucao(self, ctx):
        if ctx.declaracao():
            self.visit(ctx.declaracao())
        elif ctx.instrucaoAtribuicao():
            self.visit(ctx.instrucaoAtribuicao())
        elif ctx.bloco():
            self.visit(ctx.bloco())
        elif ctx.instrucaoWhile():
            self.visit(ctx.instrucaoWhile())
        elif ctx.instrucaoFor():
            self.visit(ctx.instrucaoFor())
        elif ctx.instrucaoReturn():
            self.visit(ctx.instrucaoReturn())
        elif ctx.instrucaoEscrita():
            self.visit(ctx.instrucaoEscrita())

    def obter_dimensoes(self, var_ctx):
        """Extrai as dimensões de um array considerando todas as formas possíveis da gramática"""
        tamanhos = []

        # Caso 1: Array com tamanho explícito (ex: v[10])
        if hasattr(var_ctx, 'NUMERO') and var_ctx.NUMERO():
            try:
                tamanho = int(var_ctx.NUMERO().getText())
                if tamanho <= 0:
                    self.lista_erros.append( "[Erro semântico] Tamanho de array deve ser positivo")
                    tamanho = 1  # Valor padrão para continuar análise
                tamanhos.append(tamanho)
            except ValueError:
                self.lista_erros.append( "[Erro semântico] Tamanho de array inválido")
                tamanhos.append(1)

        # Caso 2: Array com inicialização (ex: v[] = {1,2,3})
        elif hasattr(var_ctx, 'blocoArray') and var_ctx.blocoArray():
            if hasattr(var_ctx.blocoArray(), 'listaValores'):
                num_elementos = len(var_ctx.blocoArray().listaValores().expressao())
                tamanhos.append(num_elementos)

        # Caso 3: Array sem tamanho especificado (ex: s[] = reads())
        elif var_ctx.getChildCount() > 0 and var_ctx.getChild(0).getText() == '[':
            tamanhos.append(1)  # Tamanho padrão para arrays sem dimensão especificada

        return tamanhos

    # Visita uma declaração de variáveis
    def visitDeclaracao(self, ctx):
        tipo_var = ctx.tipo().getText()  # Obtém o tipo da declaração
        linha_declaracao = ctx.start.line  # Linha da declaração

        for var_ctx in ctx.listaVariaveis().variavel():
            nome_var = var_ctx.IDENTIFICADOR().getText()
            linha_var = var_ctx.IDENTIFICADOR().getSymbol().line
            eh_vetor = bool(var_ctx.ABRECOLCH())
            tamanhos = []

            if eh_vetor:
                # Processa dimensões do vetor
                tamanhos = self.obter_dimensoes(var_ctx) if eh_vetor else []
                #for dim in var_ctx.listaDimensoes().expressao():
                #    tamanhos.append(self.avaliar_constante(dim))  # Implemente este método

            # Verifica se a variável já foi declarada no contexto atual
            if self.tabela_simbolos.buscar_no_contexto_atual(nome_var):
                self.lista_erros.append( f"[Erro semântico] Variável '{nome_var}' já declarada neste contexto")
                continue

            # Cria objeto Variavel
            nova_var = Variavel(
                nome=nome_var,
                tipo=tipo_var,
                linha_declaracao=linha_var,
                eh_vetor=eh_vetor,
                dimensoes=len(tamanhos),
                tamanhos=tamanhos,
                valor_inicial=0
            )

            # Declara na tabela de símbolos
            if not self.tabela_simbolos.declarar(nova_var):
                self.lista_erros.append( f"[Erro semântico] Erro ao declarar variável '{nome_var}'")
                continue

            # Processa inicialização se existir
            if var_ctx.expressao():
                self.visit(var_ctx.expressao())

                # Verificação de tipo (opcional)
                if hasattr(self, 'verificar_tipos'):
                    tipo_expr = self.obter_tipo_expressao(var_ctx.expressao())
                    if tipo_expr and tipo_expr != tipo_var:
                        self.lista_erros.append(
                            f"[Erro semântico] Inicialização com tipo incompatível para '{nome_var}' (esperado: {tipo_var}, obtido: {tipo_expr})"
                        )

    # Visita uma Variável dentro de uma declaração (com ou sem inicialização)
    def visitVariavel(self, ctx):
        if ctx.expressao():
            self.visit(ctx.expressao())
        elif ctx.blocoArray():
            self.visit(ctx.blocoArray())
        elif ctx.chamadaReads():
            self.visit(ctx.chamadaReads())

    # Visita um bloco de inicialização de Vetor (ex: {1,2,3})
    def visitBlocoArray(self, ctx):
        if ctx.listaValores():
            for expr in ctx.listaValores().expressao():
                self.visit(expr)

    # Verifica se a Variável usada numa atribuição foi declarada
    def visitInstrucaoAtribuicao(self, ctx):
        nome_variavel = ctx.IDENTIFICADOR().getText()
        linha = ctx.IDENTIFICADOR().getSymbol().line

        # 1. Verifica se a variável foi declarada
        simbolo = self.tabela_simbolos.buscar(nome_variavel)

        if not simbolo:
            self.lista_erros.append(f"[Erro semântico] Variável '{nome_variavel}' não declarada")
            return

        # 2. Verifica se é um vetor (acesso com colchetes)
        if ctx.ABRECOLCH():
            if not isinstance(simbolo, Variavel) or not simbolo.eh_vetor:
                self.lista_erros.append( f"[Erro semântico] Índice aplicado a não-vetor '{nome_variavel}'")
                return

            # Visita a expressão do índice
            self.visit(ctx.expressao(1))

        # 3. Visita a expressão do valor atribuído - aqui temos que obter o valor atribuido
        self.visit(ctx.expressao(0))
        valor = ctx.expressao(0).getText()
        simbolo.valor_inicial = valor

         # 4. Verificação de tipo entre variável e expressão atribuída
        tipo_expressao = self.obter_tipo_expressao(ctx.expressao(0))
        if tipo_expressao and tipo_expressao != simbolo.tipo:
            self.lista_erros.append(
                f"[Erro semântico] Atribuição de tipo incompatível em '{nome_variavel}' "
                f"(esperado: {simbolo.tipo}, obtido: {tipo_expressao})"
            )

    # Visita uma instrução 'while'
    def visitInstrucaoWhile(self, ctx):
        self.visit(ctx.expressao())  # Condição
        self.visit(ctx.bloco())      # Corpo do ciclo

    # Visita uma instrução 'for'
    def visitInstrucaoFor(self, ctx):
        if ctx.expressaoOuAtribuicao(0):
            self.visit(ctx.expressaoOuAtribuicao(0))  # Inicialização
        if ctx.expressao():
            self.visit(ctx.expressao())               # Condição
        if ctx.expressaoOuAtribuicao(1):
            self.visit(ctx.expressaoOuAtribuicao(1))  # Passo
        self.visit(ctx.bloco())                       # Corpo do ciclo

    # Visita uma instrução 'return'
    def visitInstrucaoReturn(self, ctx):
        self.visit(ctx.expressao())

    # Visita uma instrução de escrita (write, writec, etc.)
    def visitInstrucaoEscrita(self, ctx):
        if ctx.expressao():
            self.visit(ctx.expressao())
        elif ctx.WRITEV():
            nome = ctx.IDENTIFICADOR().getText()
            if not self.tabela_simbolos.buscar(nome):
               self.lista_erros.append(f"[Erro semântico] Vetor '{nome}' usado antes de ser declarado.")

    # Visita expressões usadas isoladamente ou em atribuições
    def visitExpressaoOuAtribuicao(self, ctx):
        if ctx.expressao():
            self.visit(ctx.expressao())

    # Encaminha a visita da expressão para os filhos
    def visitExpressao(self, ctx):
        self.visitChildren(ctx)

    def visitIdComPrefixo(self, ctx):
        nome = ctx.IDENTIFICADOR().getText()
        linha = ctx.IDENTIFICADOR().getSymbol().line
        resto = ctx.primaryRest()

        # Verifica se tem sufixo (chamada de função ou acesso a vetor)
        if resto and resto.getChildCount() > 0:
            primeiro = resto.getChild(0).getText()

            if primeiro == "(":  # Chamada de função
                simbolo = self.tabela_simbolos.buscar(nome)

                if not simbolo or not isinstance(simbolo, Funcao):
                    self.lista_erros.append( f"[Erro semântico] Função '{nome}' não declarada")
                    return

                # Verifica argumentos se houver
                if resto.getChildCount() > 2:  # Tem argumentos
                    argumentos = resto.getChild(1)
                    if hasattr(argumentos, "expressao"):
                        for expr in argumentos.expressao():
                            self.visit(expr)
                return

            elif primeiro == "[":  # Acesso a vetor
                simbolo = self.tabela_simbolos.buscar(nome)

                if not simbolo or not isinstance(simbolo, Variavel):
                    self.lista_erros.append( f"[Erro semântico] Variável '{nome}' não declarada")
                    return

                if not simbolo.eh_vetor:
                    self.lista_erros.append( f"[Erro semântico] Acesso a índice em não-vetor '{nome}'")
                    return

                self.visit(resto.expressao())  # Visita a expressão do índice
                return

      # Caso simples: referência a variável
        simbolo = self.tabela_simbolos.buscar(nome)
        if not simbolo or not isinstance(simbolo, (Variavel, Funcao)):
            if nome not in self.variaveis_com_erro:
                self.lista_erros.append(f"[Erro semântico] Identificador '{nome}' não declarado (linha {linha})")
                self.variaveis_com_erro.add(nome)

    def visitChamadaFuncao(self, ctx):
        pass  # Funções built-in como read(), readc(), reads() não precisam de validação aqui

    def visitChamadaReads(self, ctx):
        pass

    def visitAcessoVetor(self, ctx):
        nome = ctx.IDENTIFICADOR().getText()
        if not self.tabela_simbolos.buscar(nome):
           self.lista_erros.append(f"[Erro semântico] Vetor '{nome}' usado antes de ser declarado.")
        self.visit(ctx.expressao())  # Verifica o índice

    # Visita um protótipo de função e regista o nome
    def visitPrototipo(self, ctx):
        nome_funcao = ctx.IDENTIFICADOR().getText()
        linha_declaracao = ctx.IDENTIFICADOR().getSymbol().line

        # Determina tipo de retorno
        tipo_retorno = "void"
        if hasattr(ctx, 'tipo') and ctx.tipo():
            tipo_retorno = ctx.tipo().getText()

        # Processa parâmetros
        parametros = []
        if hasattr(ctx, 'parametros') and ctx.parametros():
            parametros = self.visitParametros(ctx.parametros())  # Retorna lista de objetos Variavel

        # Cria objeto Funcao para o protótipo
        prototipo = Funcao(
            nome=nome_funcao,
            tipo_retorno=tipo_retorno,
            parametros=parametros,
            linha_declaracao=linha_declaracao,
            natureza="prototipo_funcao",
            eh_prototipo=True  # Campo adicional para diferenciar protótipos
        )

        # Verifica se já existe declaração
        simbolo_existente = self.tabela_simbolos.buscar_no_contexto_atual(nome_funcao)

        if simbolo_existente:
            # Caso 1: Redefinição idêntica de protótipo
            if (isinstance(simbolo_existente, Funcao) and
                    simbolo_existente.natureza == "prototipo_funcao" and
                    simbolo_existente.tipo == prototipo.tipo):
                self.lista_erros.append(
                    f"[Erro semântico] Protótipo '{nome_funcao}' redeclarado identicamente"
                )
            # Caso 2: Conflito com declaração existente
            else:
                self.lista_erros.append(
                    f"[Erro semântico] Conflito na declaração de '{nome_funcao}' (já declarado como {simbolo_existente.natureza})"
                )
        else:
            # Declara novo protótipo
            if not self.tabela_simbolos.declarar(prototipo):
                self.lista_erros.append(
                    f"[Erro semântico] Erro inesperado ao declarar protótipo '{nome_funcao}'"
                )

    # Visita o protótipo da função principal (main)
    def visitPrototipoPrincipal(self, ctx):
        nome_funcao = "main"  # Nome fixo para a função principal
        linha_declaracao = ctx.MAIN().getSymbol().line

        # Determina tipo de retorno
        tipo_retorno = "void"
        if hasattr(ctx, 'tipo') and ctx.tipo():
            tipo_retorno = ctx.tipo().getText()

        # Processa parâmetros (se existirem)
        parametros = []
        if hasattr(ctx, 'parametros') and ctx.parametros():
            parametros = self.visitParametros(ctx.parametros())  # Retorna lista de objetos Variavel

        # Cria objeto Funcao especial para main
        main_funcao = Funcao(
            nome=nome_funcao,
            tipo_retorno=tipo_retorno,
            parametros=parametros,
            linha_declaracao=linha_declaracao,
            natureza="funcao_principal",
            eh_principal=True
        )

        # Verifica se já existe declaração
        simbolo_existente = self.tabela_simbolos.buscar(nome_funcao)

        if simbolo_existente:
            # Caso 1: Redefinição da função main
            self.lista_erros.append(
                f"[Erro semântico] Redefinição da função principal '{nome_funcao}' (já declarada na linha {simbolo_existente.linha_declaracao})"
            )
        else:
            # Declara a função main
            if not self.tabela_simbolos.declarar(main_funcao):
                self.lista_erros.append(
                    f"[Erro semântico] Erro inesperado ao declarar função principal '{nome_funcao}'"
                )

    def obter_tipo_expressao(self, ctx):
        texto = ctx.getText()  # Obtém o texto completo da expressão (ex: "2.5", "a")

        # 1. Verificação de literais numéricos
        try:
            if "." in texto:
                float(texto)  # Tenta converter para float
                return "double"
            else:
                int(texto)  # Tenta converter para inteiro
                return "int"
        except ValueError:
            pass  # Não é um literal numérico — pode ser uma variável ou expressão complexa

        # 2. Verificação de variáveis (identificadores)
        if hasattr(ctx, 'IDENTIFICADOR') and ctx.IDENTIFICADOR():
            nome = ctx.IDENTIFICADOR().getText()
            simbolo = self.tabela_simbolos.buscar(nome)

            if simbolo and hasattr(simbolo, 'tipo'):
                return simbolo.tipo

        # 3. Se não for possível determinar, assume tipo desconhecido
        return None