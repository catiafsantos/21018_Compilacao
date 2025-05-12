from MOCVisitor import MOCVisitor # Supondo que esta é a sua classe base de visitante ANTLR
from TabelaSimbolos import TabelaDeSimbolos # Supondo que esta é a sua classe de Tabela de Símbolos

# Classe responsável pela análise semântica do programa
class VisitorSemantico_comtabela(MOCVisitor):
    def __init__(self, tabela_simbolos: TabelaDeSimbolos):
        self.tabela_simbolos = tabela_simbolos
        # self.contexto = [] # Esta pilha de contexto local pode ser redundante se a tabela de símbolos já gere escopos
        self.lista_erros = []               # Lista de mensagens de erro semântico
        # self.funcoes_declaradas = set() # Pode ser gerenciado pela tabela de símbolos (verificando tipo 'funcao')
        # self.variaveis_com_erro = set() # Para evitar erros duplicados, pode ser útil

    def erros(self, arvore):
        """
        Método principal para iniciar a visita e levantar uma exceção agregada se erros forem encontrados.
        """
        self.lista_erros = [] # Limpa erros de execuções anteriores
        # self.variaveis_com_erro = set() # Resetar se usar
        self.visit(arvore)
        if self.lista_erros:
            # Considerar levantar uma exceção customizada que contenha a lista de erros
            # em vez de uma Exception genérica.
            mensagens_formatadas = [str(erro) for erro in self.lista_erros] # Se lista_erros contiver objetos de erro
            raise Exception("Erros semânticos encontrados:\n" + "\n".join(mensagens_formatadas))

    def _adicionar_erro(self, mensagem: str, linha: int = None, coluna: int = None):
        """
        Método auxiliar para adicionar erros.
        Poderia ser expandido para usar objetos de erro customizados.
        """
        local_info = ""
        if linha is not None:
            local_info += f" (Linha {linha}"
            if coluna is not None:
                local_info += f", Coluna {coluna}"
            local_info += ")"
        self.lista_erros.append(f"[Erro Semântico]{local_info}: {mensagem}")


    # Visita o nó 'programa' (nó raiz da árvore)
    def visitPrograma(self, ctx):
        # O escopo global já deve ter sido criado na inicialização da TabelaDeSimbolos
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
        nome_funcao = "main" # Nome implícito da função principal
        linha_funcao = ctx.start.line # Linha onde a função principal começa
        
        # Declara a função 'main' no escopo atual (global)
        # Assumindo que o tipo de 'main' é 'funcao_principal' ou similar
        # e que não tem parâmetros que precisem ser listados no tipo aqui.
        # O tipo de retorno também pode ser parte da informação.
        if not self.tabela_simbolos.declarar_simbolo(nome_funcao, "funcao_principal", linha_funcao, info_adicional={'retorno': 'void_ou_int'}):
            self._adicionar_erro(f"Redefinição da função principal '{nome_funcao}' não permitida.", linha_funcao)
            # Mesmo com erro, podemos tentar analisar o corpo
            
        self.tabela_simbolos.entrar_escopo()  # Novo escopo para a função principal

        if ctx.parametros():
            # Se main tiver parâmetros (ex: argc, argv), eles seriam declarados aqui
            for p_idx, p_ctx in enumerate(ctx.parametros().parametro()):
                if p_ctx.IDENTIFICADOR():
                    nome_param = p_ctx.IDENTIFICADOR().getText()
                    tipo_param = self.visit(p_ctx.tipo()) # Supondo que visitTipo retorna uma string do tipo
                    linha_param = p_ctx.IDENTIFICADOR().getSymbol().line
                    if not self.tabela_simbolos.declarar_simbolo(nome_param, tipo_param, linha_param, info_adicional={'natureza': 'parametro'}):
                        self._adicionar_erro(f"Parâmetro '{nome_param}' já declarado na função '{nome_funcao}'.", linha_param)

        self.visitBloco(ctx.bloco(), novo_escopo_bloco=False)  # O escopo da função já foi criado

        self.tabela_simbolos.sair_escopo() # Sai do escopo da função principal

    # Visita uma função comum (não principal)
    def visitFuncao(self, ctx):
        nome_funcao = ctx.IDENTIFICADOR().getText()
        linha_funcao = ctx.IDENTIFICADOR().getSymbol().line
        tipo_retorno = self.visit(ctx.tipoRetorno()) # Supondo que visitTipoRetorno retorna string do tipo

        # Coletar informações dos parâmetros para compor o tipo da função
        tipos_parametros = []
        if ctx.parametros():
            for p_ctx in ctx.parametros().parametro():
                tipos_parametros.append(self.visit(p_ctx.tipo()))
        
        tipo_funcao_str = f"funcao({', '.join(tipos_parametros)}) -> {tipo_retorno}"

        if not self.tabela_simbolos.declarar_simbolo(nome_funcao, tipo_funcao_str, linha_funcao, info_adicional={'natureza': 'funcao', 'retorno': tipo_retorno}):
            # Verificar se é uma declaração compatível com um protótipo existente
            simbolo_existente = self.tabela_simbolos.buscar_simbolo_no_escopo_atual(nome_funcao) # Precisa de um método que busque só no escopo atual
            if not (simbolo_existente and simbolo_existente['tipo'] == tipo_funcao_str and simbolo_existente['info'].get('natureza') == 'prototipo_funcao'):
                 self._adicionar_erro(f"Função '{nome_funcao}' já declarada com assinatura incompatível ou não como protótipo.", linha_funcao)
        
        self.tabela_simbolos.entrar_escopo()  # Novo escopo para corpo + parâmetros
        
        if ctx.parametros():
            for p_idx, p_ctx in enumerate(ctx.parametros().parametro()):
                if p_ctx.IDENTIFICADOR():
                    nome_param = p_ctx.IDENTIFICADOR().getText()
                    tipo_param = tipos_parametros[p_idx] # Já obtido acima
                    linha_param = p_ctx.IDENTIFICADOR().getSymbol().line
                    if not self.tabela_simbolos.declarar_simbolo(nome_param, tipo_param, linha_param, info_adicional={'natureza': 'parametro'}):
                        self._adicionar_erro(f"Parâmetro '{nome_param}' já declarado na função '{nome_funcao}'.", linha_param)

        self.visitBloco(ctx.bloco(), novo_escopo_bloco=False) # O escopo da função já foi criado

        self.tabela_simbolos.sair_escopo()  # Sai do escopo da função

    # Visita um bloco de código entre chavetas
    def visitBloco(self, ctx, novo_escopo_bloco=True): # Renomeado para clareza
       if novo_escopo_bloco:
           self.tabela_simbolos.entrar_escopo()  # Novo escopo local (ex: dentro de if/while)

       if ctx.instrucoes():
           self.visit(ctx.instrucoes())

       if novo_escopo_bloco:
           self.tabela_simbolos.sair_escopo()  # Fim do escopo local

    # Visita todas as instruções dentro de um bloco
    def visitInstrucoes(self, ctx):
        for instr_ctx in ctx.instrucao(): # Renomeado para evitar conflito com 'instr' como possível palavra-chave
            self.visit(instr_ctx)

    # Encaminha a visita para o tipo de instrução correto
    def visitInstrucao(self, ctx):
        # Delega para o filho específico (instrucaoEmparelhada, outraInstrucao, etc.)
        return self.visitChildren(ctx)


    # Visita uma instrução 'if...else'
    def visitInstrucaoEmparelhada(self, ctx):
        # Exemplo: if (ctx.SE() and ctx.SENAO()):
        self.visit(ctx.expressao()) # Condição do if
        
        # Bloco 'then'
        # ctx.instrucao(0) ou ctx.bloco(0) dependendo da gramática para o 'then'
        # Supondo que a gramática para 'then' é o primeiro 'instrucaoEmparelhada' ou 'bloco'
        if hasattr(ctx, 'instrucao') and len(ctx.instrucao()) > 0:
             self.visit(ctx.instrucao(0)) # Bloco 'then'
        elif hasattr(ctx, 'bloco') and len(ctx.bloco()) > 0:
             self.visit(ctx.bloco(0)) # Bloco 'then'


        # Bloco 'else'
        # Supondo que a gramática para 'else' é o segundo 'instrucaoEmparelhada' ou 'bloco'
        if hasattr(ctx, 'instrucao') and len(ctx.instrucao()) > 1:
             self.visit(ctx.instrucao(1)) # Bloco 'else'
        elif hasattr(ctx, 'bloco') and len(ctx.bloco()) > 1:
             self.visit(ctx.bloco(1)) # Bloco 'else'
        
        return None


    # Visita uma instrução 'if' sem 'else' ou outras estruturas
    def visitInstrucaoPorEmparelhar(self, ctx):
        # Exemplo: if (ctx.SE() and not ctx.SENAO()):
        self.visit(ctx.expressao())  # Verifica a condição
        
        # Bloco 'then'
        # Supondo que a gramática para 'then' é 'instrucao' ou 'bloco'
        if hasattr(ctx, 'instrucao') and ctx.instrucao():
            self.visit(ctx.instrucao())
        elif hasattr(ctx, 'bloco') and ctx.bloco():
            self.visit(ctx.bloco())
        return None

    # Trata instruções genéricas
    def visitOutraInstrucao(self, ctx):
        # Delega para o filho específico (declaracao, atribuicao, etc.)
        return self.visitChildren(ctx)


    # Visita uma declaração de variáveis
    def visitDeclaracao(self, ctx):
        tipo_base_variavel = self.visit(ctx.tipo()) # Supondo que visitTipo retorna a string do tipo

        for var_ctx in ctx.listaVariaveis().variavel():
            nome_var = var_ctx.IDENTIFICADOR().getText()
            linha_var = var_ctx.IDENTIFICADOR().getSymbol().line
            tipo_final_var = tipo_base_variavel # Assume tipo base por padrão

            info_adicional = {'natureza': 'variavel'}

            # Verifica se é uma declaração de vetor
            if var_ctx.ABRECOLCH() and var_ctx.FECHACOLCH(): # Ex: int v[10];
                if var_ctx.expressao(): # Se houver uma expressão para o tamanho
                    tamanho_expr_ctx = var_ctx.expressao()
                    # Aqui você pode querer avaliar a expressão de tamanho se for constante
                    # ou apenas registrar que é um vetor e o tipo dos elementos.
                    # tipo_final_var = f"vetor_de_{tipo_base_variavel}" # Ou uma representação mais estruturada
                    info_adicional['eh_vetor'] = True
                    # info_adicional['tamanho_expr'] = tamanho_expr_ctx.getText() # Para análise posterior
                else: # Ex: int v[]; (se permitido pela linguagem, talvez como parâmetro)
                    # tipo_final_var = f"vetor_de_{tipo_base_variavel}_sem_tamanho_definido"
                    info_adicional['eh_vetor'] = True
                    info_adicional['tamanho_indefinido'] = True


            if not self.tabela_simbolos.declarar_simbolo(nome_var, tipo_final_var, linha_var, info_adicional):
               self._adicionar_erro(f"Variável '{nome_var}' já foi declarada neste escopo.", linha_var)
            
            # Visita a possível inicialização da variável (se houver uma expressão após '=')
            if var_ctx.IGUAL(): # Verifica se há um sinal de atribuição na declaração
                # A gramática precisaria ter uma 'expressao' após o IGUAL dentro de 'variavel'
                # Ex: variavel: IDENTIFICADOR (ABRECOLCH expressao FECHACOLCH)? (IGUAL expressao)?;
                if hasattr(var_ctx, 'expressao_inicializacao') and var_ctx.expressao_inicializacao(): # Nome hipotético do nó
                    self.visit(var_ctx.expressao_inicializacao())
                elif hasattr(var_ctx, 'blocoArray') and var_ctx.blocoArray(): # Para inicialização de array tipo {1,2,3}
                    self.visit(var_ctx.blocoArray())


    # Visita uma Variável dentro de uma declaração (com ou sem inicialização)
    # Este método pode ser simplificado se a lógica de declaração for toda em visitDeclaracao
    def visitVariavel(self, ctx):
        # A declaração do nome e tipo já deve ter sido feita em visitDeclaracao.
        # Esta visita seria para a parte da inicialização, se houver.
        if ctx.expressao(): # Ex: int x = expressao;
            self.visit(ctx.expressao())
        elif ctx.blocoArray(): # Ex: int arr[] = {1, 2, 3};
            self.visit(ctx.blocoArray())
        elif ctx.chamadaReads(): # Ex: string s = reads();
            self.visit(ctx.chamadaReads())

    # Visita um bloco de inicialização de Vetor (ex: {1,2,3})
    def visitBlocoArray(self, ctx):
        if ctx.listaValores():
            for expr_ctx in ctx.listaValores().expressao():
                self.visit(expr_ctx)

    # Verifica se a Variável usada numa atribuição foi declarada
    def visitInstrucaoAtribuicao(self, ctx):
        nome_var_atribuida = ctx.IDENTIFICADOR().getText()
        linha_uso = ctx.IDENTIFICADOR().getSymbol().line
        
        simbolo = self.tabela_simbolos.buscar_simbolo(nome_var_atribuida)
        if not simbolo:
           self._adicionar_erro(f"Variável '{nome_var_atribuida}' usada antes de ser declarada.", linha_uso)
        # else:
            # Aqui você pode adicionar verificações de tipo:
            # tipo_variavel = simbolo['tipo']
            # tipo_expressao = self.visit(ctx.expressao(0)) # Supondo que visitExpressao retorna o tipo
            # if not self.tipos_compativeis(tipo_variavel, tipo_expressao):
            #    self._adicionar_erro(f"Tipos incompatíveis na atribuição à variável '{nome_var_atribuida}'.", linha_uso)

        self.visit(ctx.expressao(0))  # Valor atribuído
        
        if ctx.ABRECOLCH(): # Se for acesso a Vetor (ex: nome_var[indice] = valor)
            if simbolo and not simbolo['info'].get('eh_vetor', False):
                self._adicionar_erro(f"Variável '{nome_var_atribuida}' não é um vetor e não pode ser indexada.", linha_uso)
            self.visit(ctx.expressao(1))  # Visita a expressão do índice

    # Visita uma instrução 'while'
    def visitInstrucaoWhile(self, ctx):
        self.visit(ctx.expressao())  # Condição
        self.visit(ctx.bloco())      # Corpo do ciclo

    # Visita uma instrução 'for'
    def visitInstrucaoFor(self, ctx):
        # Para loops 'for', pode ser necessário um escopo dedicado se a linguagem permitir
        # declaração de variáveis na inicialização do for (ex: for (int i = 0; ...))
        # Se for o caso: self.tabela_simbolos.entrar_escopo()
        
        if ctx.expressaoOuAtribuicao(0): # A gramática pode ter nós diferentes aqui
            self.visit(ctx.expressaoOuAtribuicao(0))  # Inicialização
        if ctx.expressao():
            self.visit(ctx.expressao())               # Condição
        if len(ctx.expressaoOuAtribuicao()) > 1 and ctx.expressaoOuAtribuicao(1):
            self.visit(ctx.expressaoOuAtribuicao(1))  # Passo
        
        self.visit(ctx.bloco())                       # Corpo do ciclo
        # Se entrou em escopo para o for: self.tabela_simbolos.sair_escopo()


    # Visita uma instrução 'return'
    def visitInstrucaoReturn(self, ctx):
        if ctx.expressao(): # Se houver uma expressão de retorno
            self.visit(ctx.expressao())
        # Aqui você pode querer verificar se o tipo da expressão de retorno
        # é compatível com o tipo de retorno da função atual.
        # Isso requer rastrear em qual função estamos.

    # Visita uma instrução de escrita (write, writec, etc.)
    def visitInstrucaoEscrita(self, ctx):
        if ctx.expressao():
            self.visit(ctx.expressao())
        elif ctx.WRITEV(): # Supondo que WRITEV é um token específico para escrita de vetor
            nome_vetor = ctx.IDENTIFICADOR().getText()
            linha_uso = ctx.IDENTIFICADOR().getSymbol().line
            simbolo = self.tabela_simbolos.buscar_simbolo(nome_vetor)
            if not simbolo:
               self._adicionar_erro(f"Vetor '{nome_vetor}' usado antes de ser declarado para escrita.", linha_uso)
            elif not simbolo['info'].get('eh_vetor', False):
               self._adicionar_erro(f"Identificador '{nome_vetor}' não é um vetor (uso em WRITEV).", linha_uso)


    # Visita expressões usadas isoladamente ou em atribuições
    def visitExpressaoOuAtribuicao(self, ctx):
        # Delega para o filho (que será uma 'expressao' ou uma 'instrucaoAtribuicao' específica)
        return self.visitChildren(ctx)

    # Encaminha a visita da expressão para os filhos
    # Este método é genérico; as verificações de tipo e uso de variáveis
    # ocorreriam nos métodos mais específicos que compõem uma expressão (ex: visitIdComPrefixo, visitLiteral, etc.)
    def visitExpressao(self, ctx):
        # A lógica aqui dependerá muito da estrutura da sua gramática para expressões.
        # Exemplo: Se for uma operação binária:
        # if ctx.operador_binario():
        #     tipo_esq = self.visit(ctx.expressao(0))
        #     tipo_dir = self.visit(ctx.expressao(1))
        #     verificar_compatibilidade_tipos(ctx.operador_binario(), tipo_esq, tipo_dir)
        #     return tipo_resultante
        return self.visitChildren(ctx) # Delegação padrão

    # Este método é crucial para verificar o uso de identificadores em expressões.
    def visitIdComPrefixo(self, ctx): # Nome da regra ANTLR pode variar
        nome_id = ctx.IDENTIFICADOR().getText()
        linha_uso = ctx.IDENTIFICADOR().getSymbol().line
        
        # Verifica se é uma chamada de função ou acesso a vetor
        # A lógica exata depende da estrutura da sua regra 'primaryRest'
        eh_chamada_funcao = False
        eh_acesso_vetor = False

        if ctx.primaryRest():
            # Exemplo: Se primaryRest tiver '(' para chamada de função
            if ctx.primaryRest().LPAREN(): # Supondo LPAREN para '('
                eh_chamada_funcao = True
            # Exemplo: Se primaryRest tiver '[' para acesso a vetor
            elif ctx.primaryRest().ABRECOLCH(): # Supondo ABRECOLCH para '['
                eh_acesso_vetor = True
        
        simbolo = self.tabela_simbolos.buscar_simbolo(nome_id)

        if eh_chamada_funcao:
            if not simbolo:
                self._adicionar_erro(f"Função '{nome_id}' chamada mas não foi declarada.", linha_uso)
            elif not simbolo['tipo'].startswith("funcao"): # Ou uma verificação mais robusta do tipo de função
                self._adicionar_erro(f"Identificador '{nome_id}' não é uma função e não pode ser chamado.", linha_uso)
            # else:
                # Verificar número e tipos de argumentos passados vs. esperados (da tabela de símbolos)
                # self.visit(ctx.primaryRest().listaArgumentos()) # Visitar argumentos
            if ctx.primaryRest().listaArgumentos(): # Supondo que listaArgumentos é o nó para os args
                self.visit(ctx.primaryRest().listaArgumentos())

        elif eh_acesso_vetor:
            if not simbolo:
                self._adicionar_erro(f"Vetor '{nome_id}' usado antes de ser declarado.", linha_uso)
            elif not simbolo['info'].get('eh_vetor', False):
                self._adicionar_erro(f"Variável '{nome_id}' não é um vetor e não pode ser indexada.", linha_uso)
            # else:
                # self.visit(ctx.primaryRest().expressao()) # Visitar a expressão do índice
            if ctx.primaryRest().expressao(): # Supondo que expressao é o nó para o índice
                self.visit(ctx.primaryRest().expressao())
        
        else: # É um uso simples de variável
            if not simbolo:
                self._adicionar_erro(f"Variável '{nome_id}' usada antes de ser declarada.", linha_uso)
            # else:
                # Poderia retornar simbolo['tipo'] se este método fosse usado para inferência de tipo
                pass
        
        return None # Ou o tipo do identificador, se aplicável

    # Não é mais necessário se visitIdComPrefixo tratar chamadas de função
    # def visitChamadaFuncao(self, ctx):
    #     pass

    # Funções built-in como read(), readc(), reads() podem não precisar de validação aqui
    # se não estiverem na tabela de símbolos como funções regulares.
    def visitChamadaReads(self, ctx):
        # Geralmente não há muito a validar semanticamente aqui, a menos que haja restrições de tipo de atribuição
        pass

    # Não é mais necessário se visitIdComPrefixo tratar acesso a vetores
    # def visitAcessoVetor(self, ctx):
    #    pass


    # Visita um protótipo de função e regista o nome e tipo na tabela de símbolos
    def visitPrototipo(self, ctx):
        nome_funcao = ctx.IDENTIFICADOR().getText()
        linha_proto = ctx.IDENTIFICADOR().getSymbol().line
        tipo_retorno = self.visit(ctx.tipoRetorno()) # Supondo que retorna string do tipo

        tipos_parametros = []
        if ctx.parametros():
            for p_ctx in ctx.parametros().parametro():
                # Para protótipos, os nomes dos parâmetros podem ser opcionais,
                # mas os tipos são importantes.
                tipos_parametros.append(self.visit(p_ctx.tipo()))
        
        tipo_funcao_str = f"funcao({', '.join(tipos_parametros)}) -> {tipo_retorno}"

        if not self.tabela_simbolos.declarar_simbolo(nome_funcao, tipo_funcao_str, linha_proto, info_adicional={'natureza': 'prototipo_funcao', 'retorno': tipo_retorno}):
            self._adicionar_erro(f"Redeclaração do protótipo da função '{nome_funcao}'.", linha_proto)

    # Visita o protótipo da função principal (main)
    def visitPrototipoPrincipal(self, ctx):
        nome_funcao = "main"
        linha_proto = ctx.start.line # Linha onde o protótipo de main começa
        # O tipo de retorno de main pode ser fixo (ex: void ou int)
        tipo_retorno_main = "void_ou_int" # Ou determinado pela sua linguagem
        
        # Protótipo de main geralmente não tem parâmetros listados desta forma,
        # ou tem uma assinatura específica (void) ou (int, char**).
        # Para simplificar, vamos assumir uma assinatura sem parâmetros aqui.
        tipo_funcao_str = f"funcao() -> {tipo_retorno_main}"

        if not self.tabela_simbolos.declarar_simbolo(nome_funcao, tipo_funcao_str, linha_proto, info_adicional={'natureza': 'prototipo_funcao_principal', 'retorno': tipo_retorno_main}):
            self._adicionar_erro(f"Redeclaração do protótipo da função principal '{nome_funcao}'.", linha_proto)

    # Métodos para visitar tipos (exemplos, precisam ser adaptados à sua gramática)
    def visitTipo(self, ctx) -> str:
        # Retorna uma string representando o tipo
        if ctx.INT(): return "inteiro"
        if ctx.FLOAT(): return "flutuante"
        if ctx.STRING(): return "string"
        if ctx.BOOLEAN(): return "booleano"
        if ctx.VOID(): return "void" # Se 'void' for um tipo que pode ser retornado por este método
        # Adicione outros tipos básicos ou complexos da sua linguagem
        return "tipo_desconhecido"

    def visitTipoRetorno(self, ctx) -> str:
        if ctx.tipo():
            return self.visit(ctx.tipo())
        elif ctx.VOID(): # Se VOID for um token separado para tipo de retorno
            return "void"
        return "tipo_retorno_desconhecido"

    # Adicione métodos visit para outros nós da sua AST conforme necessário
    # Ex: visitLiteralInteiro, visitLiteralFlutuante, visitOperacaoBinaria, etc.
    # Estes métodos seriam importantes para a verificação e inferência de tipos.

