from MOCVisitor import MOCVisitor
from TabelaSimbolos import TabelaDeSimbolos


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

        if ctx.parametros():
            for p in ctx.parametros().parametro():
                if p.IDENTIFICADOR():
                    nome = p.IDENTIFICADOR().getText()
                    if nome in self.contexto[-1]:
                        self.lista_erros.append(f"[Erro semântico] Parâmetro '{nome}' já foi declarado.")
                    self.contexto[-1].add(nome)  # Adiciona o parâmetro ao contexto

        self.visitBloco(ctx.bloco(), novo_contexto=False)  # NÃO cria novo contexto aqui

        self.contexto.pop()  # Sai do contexto após a função terminar

    def visitTipo(self, ctx) -> str:
        """
        Visita um nó de tipo e retorna sua representação em string.
        """
        if not ctx: return "tipo_desconhecido" # Caso o contexto do tipo seja nulo
        if hasattr(ctx, 'INT') and ctx.INT(): return "int"
        if hasattr(ctx, 'DOUBLE') and ctx.FLOAT(): return "double"
        if hasattr(ctx, 'STRING') and ctx.STRING(): return "string"
        if hasattr(ctx, 'VOID') and ctx.VOID(): return "void"
        return ctx.getText() # Fallback

    def visitTipoRetorno(self, ctx) -> str:
        """Visita o nó do tipo de retorno de uma função."""
        if not ctx: return "tipo_retorno_desconhecido"
        if hasattr(ctx, 'tipo') and ctx.tipo():
            return self.visit(ctx.tipo())
        elif hasattr(ctx, 'VOID') and ctx.VOID():
            return "void"
        return "tipo_retorno_desconhecido_na_regra"

    def visitParametro(self, ctx):
        nome_parametro = ctx.IDENTIFICADOR().getText()
        tipo_parametro = ctx.tipo().getText()
        linha_declaracao = ctx.IDENTIFICADOR().getSymbol().line

    def visitParametros(self, ctx) -> list[dict]:
        """
        Visita os parâmetros de uma função/protótipo.
        Retorna uma lista de dicionários, cada um contendo 'nome' e 'tipo' do parâmetro.
        Adapte conforme a sua gramática para parâmetros.
        """
        parametros_info = []
        if ctx and hasattr(ctx, 'parametro') and ctx.parametro():
            for p_idx, p_ctx in enumerate(ctx.parametro()):  # Adicionado p_idx para rastrear o índice se necessário
                nome_param = f"param_{p_idx}"  # Nome padrão se não houver identificador
                tipo_param = "tipo_param_desconhecido"
                linha_param = p_ctx.start.line  # Linha do início da declaração do parâmetro
                coluna_param = p_ctx.start.column

                if hasattr(p_ctx, 'IDENTIFICADOR') and p_ctx.IDENTIFICADOR():
                    nome_param = p_ctx.IDENTIFICADOR().getText()
                    linha_param = p_ctx.IDENTIFICADOR().getSymbol().line
                    coluna_param = p_ctx.IDENTIFICADOR().getSymbol().column

                if hasattr(p_ctx, 'tipo') and p_ctx.tipo():
                    tipo_param = self.visit(p_ctx.tipo())

                parametros_info.append({
                    'nome': nome_param,
                    'tipo': tipo_param,
                    'linha': linha_param,  # Guardar a linha para mensagens de erro
                    'coluna': coluna_param  # Guardar a coluna
                })
        return parametros_info


    # Visita uma função comum (não principal)
    def visitFuncao(self, ctx):
        self.contexto.append(set())  # Cria um novo contexto para corpo + parâmetros

        nome_funcao = ctx.IDENTIFICADOR().getText()
        tipo_funcao = ctx.tipo().getText()
        linha_declaracao = ctx.IDENTIFICADOR().getSymbol().line
        tipo_retorno_definicao = "void"  # Valor padrão se não especificado ou não encontrado
        if hasattr(ctx, 'tipo') and ctx.tipo():  # Verifica se o nó 'tipo' existe no contexto do protótipo
            tipo_retorno_definicao = ctx.tipo().getText()  # self.visit(ctx.tipo())

        # Obtém os tipos dos parâmetros
        parametros_definicao_info = []
        tipos_parametros=''
        if hasattr(ctx, 'parametros') and ctx.parametros():  # Verifica se o nó 'parametros' existe
            tipos_parametros = ctx.parametros().getText()  # self.visitParametros(ctx.parametros())
            parametros_definicao_info = self.visitParametros(ctx.parametros())

        tipos_parametros_definicao_str = [p_info['tipo'] for p_info in parametros_definicao_info]
        assinatura_definida = f"funcao({','.join(tipos_parametros_definicao_str)})->{tipo_retorno_definicao}"

        self.funcao_atual_info = {
            'nome': nome_funcao,
            'tipo_retorno_esperado': tipo_retorno_definicao
        }

        simbolo_existente = self.tabela_simbolos.buscar_simbolo_no_contexto_atual(nome_funcao)

        if simbolo_existente:
            if simbolo_existente['info'].get('natureza') == 'prototipo_funcao':
                if simbolo_existente['tipo'] == assinatura_definida:
                    # Protótipo corresponde à definição, atualizar para 'funcao_definida'
                    simbolo_existente['info']['natureza'] = 'funcao_definida'
                    simbolo_existente['info'][
                        'parametros'] = parametros_definicao_info  # Atualiza com nomes dos params da definição
                    simbolo_existente['linha_declaracao'] = linha_declaracao  # Atualiza para linha da definição
                    print(f"DEBUG: Definição da função '{nome_funcao}' corresponde ao protótipo. Símbolo atualizado.")
                else:
                    self.lista_erros.append(
                        f"Definição da função '{nome_funcao}' (assinatura: {assinatura_definida}) não corresponde ao protótipo declarado (assinatura: {simbolo_existente['tipo']}).")
                    # Não prosseguir com a análise do corpo se a assinatura for incompatível com protótipo crítico
                    self.funcao_atual_info = None
                    return
            elif simbolo_existente['info'].get('natureza') == 'funcao_definida':
                self.lista_erros.append(f"Redefinição da função '{nome_funcao}'.")
                self.funcao_atual_info = None
                return  # Não analisar corpo de função redefinida
            else:
                self.lista_erros.append(
                    f"Identificador '{nome_funcao}' já declarado como outra coisa (não protótipo/função).")
                self.funcao_atual_info = None
                return
        else:
            # Nenhuma declaração anterior (nem protótipo), declara como nova função definida

            # ERRO - ISTO NAO ACONTECE NA NOSSA LINGUAGEM
            info_adicional = {
                'natureza': 'funcao_definida',
                'tipo_retorno': tipo_retorno_definicao,
                'parametros': parametros_definicao_info
            }
            if not self.tabela_simbolos.declarar_simbolo(nome_funcao, assinatura_definida, linha_declaracao,
                                                         info_adicional):
                # Esta situação não deveria ocorrer se buscar_simbolo_no_contexto_atual retornou None
                self.lista_erros.append(f"Erro inesperado ao declarar a nova função '{nome_funcao}'.")
                self.funcao_atual_info = None
                return
            print(f"DEBUG: Função '{nome_funcao}' definida sem protótipo prévio (assinatura: {assinatura_definida}).")

        # Entrar no contexto da função e declarar parâmetros
        self.tabela_simbolos.entrar_contexto()

        # Declarar cada parâmetro na tabela de símbolos dentro do novo escopo da função
        nomes_parametros_neste_escopo = set() # Para verificar parâmetros duplicados dentro da mesma função
        for p_info in parametros_definicao_info:
            nome_param = p_info['nome']
            tipo_param = p_info['tipo']
            linha_param = p_info['linha'] # Usar a linha do parâmetro obtida em visitParametros

            if nome_param in nomes_parametros_neste_escopo:
                self._adicionar_erro(f"Parâmetro '{nome_param}' redeclarado na lista de parâmetros da função '{nome_funcao}'.", linha_param)
                continue # Não tenta declarar um parâmetro duplicado

            info_param = {'natureza': 'parametro'}
            if not self.tabela_simbolos.declarar_simbolo(nome_param, tipo_param, linha_param, info_param):
                # Este erro é mais para o caso de o nome do parâmetro colidir com algo
                # que não deveria estar no escopo da função ainda (improvável se o escopo é novo).
                # A verificação de duplicados acima é mais específica para parâmetros.
                self._adicionar_erro(f"Erro ao declarar o parâmetro '{nome_param}' na função '{nome_funcao}'. Pode já existir.", linha_param)
            else:
                nomes_parametros_neste_escopo.add(nome_param)
                print(f"DEBUG: Parâmetro '{nome_param}' (tipo: {tipo_param}) declarado para a função '{nome_funcao}'.")

        # Isto deve estar mal... se o nome das var for igual a uma ja definida estará a dar erro e nao é
        if ctx.parametros():
            for p in ctx.parametros().parametro():
                if p.IDENTIFICADOR():
                    nome = p.IDENTIFICADOR().getText()
                    if nome in self.contexto[-1]:
                        self.lista_erros.append(f"[Erro semântico] Parâmetro '{nome}' já foi declarado.")
                    self.contexto[-1].add(nome)

        self.visitBloco(ctx.bloco(), novo_contexto=False)  # NÃO cria novo contexto aqui

        self.contexto.pop()
        self.tabela_simbolos.sair_contexto()
        self.funcao_atual_info = None # Limpar info da função atual

    # Visita um bloco de código entre chavetas
    def visitBloco(self, ctx, novo_contexto=True):
       if novo_contexto:
           self.tabela_simbolos.entrar_contexto()
           self.contexto.append(set())  # Novo contexto local (ex: dentro de if/while)

       if ctx.instrucoes():
           self.visit(ctx.instrucoes())

       if novo_contexto:
           self.contexto.pop()  # Fim do contexto local
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

    # Visita uma declaração de variáveis
    def visitDeclaracao(self, ctx):
        for var in ctx.listaVariaveis().variavel():
            nome = var.IDENTIFICADOR().getText()
            if nome in self.contexto[-1]:
               self.lista_erros.append(f"[Erro semântico] Variável '{nome}' já foi declarada.")
            else:
                self.contexto[-1].add(nome)
            self.visit(var)  # Visita a possível inicialização

    def visitDeclaracao_aqui(self, ctx):
        """
        Visita uma declaração de variável (ex: int x, y[10];).
        As variáveis são adicionadas ao escopo ATUAL na tabela de símbolos.
        Este escopo pode ser o global, o de uma função, ou de um bloco aninhado
        (if, while, for, etc.), dependendo de onde a declaração ocorre.
        O método visitBloco (ou visitFuncao) é responsável por criar o escopo apropriado
        antes que este método seja chamado para declarações dentro desses blocos/funções.
        """
        tipo_base_variavel = self.visit(ctx.tipo())

        for var_ctx in ctx.listaVariaveis().variavel():  # Supondo que sua gramática tem listaVariaveis().variavel()
            nome_var = var_ctx.IDENTIFICADOR().getText()
            linha_var = var_ctx.IDENTIFICADOR().getSymbol().line
            tipo_final_var = tipo_base_variavel
            info_adicional = {'natureza': 'variavel'}

            # Verifica se é uma declaração de vetor
            # Adapte esta lógica conforme a sua gramática para declaração de vetores
            if hasattr(var_ctx, 'ABRECOLCH') and var_ctx.ABRECOLCH():
                info_adicional['eh_vetor'] = True
                tipo_final_var = f"vetor_de_{tipo_base_variavel}"  # Ou uma representação mais estruturada
                if hasattr(var_ctx, 'expressao') and var_ctx.expressao():  # Tamanho do vetor
                    # Poderia visitar a expressão do tamanho para análise adicional
                    # self.visit(var_ctx.expressao())
                    info_adicional['tamanho_expr'] = var_ctx.expressao().getText()
                else:
                    info_adicional['tamanho_indefinido'] = True

            print(
                f"DEBUG: Tentando declarar variável '{nome_var}' (tipo: {tipo_final_var}) na linha {linha_var} no escopo atual.")
            if not self.tabela_simbolos.declarar_simbolo(nome_var, tipo_final_var, linha_var, info_adicional):
                self._adicionar_erro(f"Variável '{nome_var}' já foi declarada neste escopo.", linha_var)

            # Visita a possível inicialização da variável
            # Adapte conforme a sua gramática para inicialização na declaração
            if hasattr(var_ctx, 'IGUAL') and var_ctx.IGUAL():
                if hasattr(var_ctx, 'expressao_inicializacao') and var_ctx.expressao_inicializacao():
                    self.visit(var_ctx.expressao_inicializacao())
                elif hasattr(var_ctx, 'blocoArray') and var_ctx.blocoArray():
                    self.visit(var_ctx.blocoArray())

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
        nome = ctx.IDENTIFICADOR().getText()
        if not any(nome in contexto for contexto in reversed(self.contexto)):
           self.lista_erros.append(f"[Erro semântico] Variável '{nome}' usada antes de ser declarada.")
        self.visit(ctx.expressao(0))  # Valor atribuído
        if ctx.ABRECOLCH():
            self.visit(ctx.expressao(1))  # Índice, se for acesso a Vetor

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
            if not any(nome in contexto for contexto in reversed(self.contexto)):
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
        resto = ctx.primaryRest()
    
        # Tem sufixo? Pode ser chamada ou acesso a vetor
        if resto and resto.getChildCount() > 0:
            primeiro = resto.getChild(0).getText()

            if primeiro == "(":  # chamada a função
                if nome not in self.funcoes_declaradas and nome not in self.variaveis_com_erro:
                    self.lista_erros.append(f"[Erro semântico] Função '{nome}' chamada mas não foi declarada.")
                    self.variaveis_com_erro.add(nome)
                # Visitamos todos os argumentos (se houver)
                if resto.getChildCount() > 2:  # Há algo entre parênteses
                    argumentos = resto.getChild(1)
                    if hasattr(argumentos, "expressao"):
                        for expr in argumentos.expressao():
                            self.visit(expr)
                return

            elif primeiro == "[":  # acesso a vetor
                self.visit(resto.expressao())  # visitar o índice
                return

        # Caso contrário: é apenas uma variável isolada
        if nome not in self.funcoes_declaradas and not any(nome in contexto for contexto in reversed(self.contexto)):
            if nome not in self.variaveis_com_erro:
                self.lista_erros.append(f"[Erro semântico] Variável '{nome}' usada antes de ser declarada.")
                self.variaveis_com_erro.add(nome)


    def visitChamadaFuncao(self, ctx):
        pass  # Funções built-in como read(), readc(), reads() não precisam de validação aqui

    def visitChamadaReads(self, ctx):
        pass

    def visitAcessoVetor(self, ctx):
        nome = ctx.IDENTIFICADOR().getText()
        if not any(nome in contexto for contexto in reversed(self.contexto)):
           self.lista_erros.append(f"[Erro semântico] Vetor '{nome}' usado antes de ser declarado.")
        self.visit(ctx.expressao())  # Verifica o índice

    # Visita um protótipo de função e regista o nome
    def visitPrototipo(self, ctx):
        nome_funcao = ctx.IDENTIFICADOR().getText()
        tipo_funcao = ctx.tipo().getText()
        linha_declaracao = ctx.IDENTIFICADOR().getSymbol().line
        self.funcoes_declaradas.add(nome_funcao)

        # Obtém o tipo de retorno usando o método visitTipo para consistência
        # Assumindo que ctx.tipo() retorna o contexto do nó do tipo de retorno
        tipo_retorno_str = "void" # Valor padrão se não especificado ou não encontrado
        if hasattr(ctx, 'tipo') and ctx.tipo(): # Verifica se o nó 'tipo' existe no contexto do protótipo
            tipo_retorno_str = ctx.tipo().getText() #self.visit(ctx.tipo())
        # Obtém os tipos dos parâmetros
        tipos_parametros = []
        if hasattr(ctx, 'parametros') and ctx.parametros():  # Verifica se o nó 'parametros' existe
            tipos_parametros = ctx.parametros().getText()# self.visitParametros(ctx.parametros())

        # Constrói uma representação da assinatura/tipo da função
        # Exemplo: "funcao(inteiro,string)->flutuante"
        assinatura_funcao = f"funcao({tipos_parametros})->{tipo_retorno_str}"

        # Informações adicionais para armazenar na tabela de símbolos
        info_adicional = {
            'natureza': 'prototipo_funcao',
            'tipo_retorno': tipo_retorno_str,
            'tipos_parametros': tipos_parametros  # Lista dos tipos dos parâmetros
        }
        # Tenta declarar o protótipo da função na tabela de símbolos
        # O método declarar_simbolo da TabelaDeSimbolos (do artefato) já verifica
        # se o símbolo existe no escopo atual. Para protótipos, que geralmente
        # estão no escopo global, isso é o comportamento desejado.
        if not self.tabela_simbolos.declarar_simbolo(nome_funcao, assinatura_funcao, linha_declaracao, info_adicional):
            # Se declarar_simbolo retornar False, significa que já existe no escopo atual.
            # Você pode querer verificar se a redeclaração é compatível.
            simbolo_existente = self.tabela_simbolos.buscar_simbolo_no_contexto_atual(nome_funcao)
            if simbolo_existente and simbolo_existente['tipo'] == assinatura_funcao and simbolo_existente['info'].get('natureza') == 'prototipo_funcao':
                # É uma redeclaração idêntica do mesmo protótipo, pode ser um aviso ou ignorado.
                print(f"AVISO (Linha {linha_declaracao}): Protótipo da função '{nome_funcao}' redeclarado identicamente.")
            else:
                self.lista_erros.append(f"Redeclaração incompatível ou conflito de nome para o protótipo da função '{nome_funcao}'.")
        else:
            # Sucesso na declaração do protótipo
            # self.funcoes_declaradas.add(nome_funcao) # Não é mais necessário se a tabela de símbolos for a fonte da verdade
            print(f"DEBUG: Protótipo da função '{nome_funcao}' (tipo: {assinatura_funcao}) declarado na linha {linha_declaracao}.")


    # Visita o protótipo da função principal (main)
    def visitPrototipoPrincipal(self, ctx):

        nome_funcao = ctx.MAIN().getText()
        tipo_funcao = ctx.tipo().getText()
        linha_declaracao = ctx.MAIN().getSymbol().line
        self.funcoes_declaradas.add("main")

        # Obtém o tipo de retorno usando o método visitTipo para consistência
        # Assumindo que ctx.tipo() retorna o contexto do nó do tipo de retorno
        tipo_retorno_str = "void"  # Valor padrão se não especificado ou não encontrado
        if hasattr(ctx, 'tipo') and ctx.tipo():  # Verifica se o nó 'tipo' existe no contexto do protótipo
            tipo_retorno_str = ctx.tipo().getText()  # self.visit(ctx.tipo())
        # Obtém os tipos dos parâmetros
        tipos_parametros = []
        if hasattr(ctx, 'parametros') and ctx.parametros():  # Verifica se o nó 'parametros' existe
            tipos_parametros = ctx.parametros().getText()  # self.visitParametros(ctx.parametros())

        # Constrói uma representação da assinatura/tipo da função
        # Exemplo: "funcao(inteiro,string)->flutuante"
        assinatura_funcao = f"funcao({tipos_parametros})->{tipo_retorno_str}"

        # Informações adicionais para armazenar na tabela de símbolos
        info_adicional = {
            'natureza': 'prototipo_funcao',
            'tipo_retorno': tipo_retorno_str,
            'tipos_parametros': tipos_parametros  # Lista dos tipos dos parâmetros
        }
        # Tenta declarar o protótipo da função na tabela de símbolos
        # O método declarar_simbolo da TabelaDeSimbolos (do artefato) já verifica
        # se o símbolo existe no escopo atual. Para protótipos, que geralmente
        # estão no escopo global, isso é o comportamento desejado.
        if not self.tabela_simbolos.declarar_simbolo(nome_funcao, assinatura_funcao, linha_declaracao, info_adicional):
            # Se declarar_simbolo retornar False, significa que já existe no escopo atual.
            # Você pode querer verificar se a redeclaração é compatível.
            simbolo_existente = self.tabela_simbolos.buscar_simbolo_no_escopo_atual(nome_funcao)
            if simbolo_existente and simbolo_existente['tipo'] == assinatura_funcao and simbolo_existente['info'].get(
                    'natureza') == 'prototipo_funcao':
                # É uma redeclaração idêntica do mesmo protótipo, pode ser um aviso ou ignorado.
                print(
                    f"AVISO (Linha {linha_declaracao}): Protótipo da função '{nome_funcao}' redeclarado identicamente.")
            else:
                self.lista_erros.append(
                    f"Redeclaração incompatível ou conflito de nome para o protótipo da função '{nome_funcao}'.")
        else:
            # Sucesso na declaração do protótipo
            # self.funcoes_declaradas.add(nome_funcao) # Não é mais necessário se a tabela de símbolos for a fonte da verdade
            print(
                f"DEBUG: Protótipo da função '{nome_funcao}' (tipo: {assinatura_funcao}) declarado na linha {linha_declaracao}.")

