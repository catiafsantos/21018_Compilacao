from typing import List, Dict, Optional, Union

DEBUG_MODE_TABELA_SIMBOLOS = False

def debug_print(*args, **kwargs):
    """Imprime apenas se DEBUG_MODE for True."""
    if DEBUG_MODE_TABELA_SIMBOLOS:
        print("DEBUG:", *args, **kwargs)

class Simbolo:
    """Classe base para todos os símbolos (variáveis, funções, parâmetros, etc.)."""

    def __init__(
            self,
            nome: str,
            tipo: str,
            linha_declaracao: int,
            natureza: str,
            #localizacao: str,   #nome do local onde surge main, funcao, ciclo, if...
            #nivel: int,
            **atributos_adicionais
    ):
        self.nome = nome
        self.tipo = tipo
        self.linha_declaracao = linha_declaracao
        self.natureza = natureza  # 'variavel', 'funcao', 'parametro', 'constante'
        self.atributos = atributos_adicionais  # Ex.: valor_inicial, etc.


    def __repr__(self):
         # Adiciona mais detalhes na representação para facilitar o debug
        attrs_str = ', '.join(f"{k}={v}" for k, v in self.atributos.items() if k not in ['nome', 'tipo', 'linha_declaracao', 'natureza'])
        return f"<Simbolo {self.nome} (Tipo: {self.tipo}, Natureza: {self.natureza}, Linha: {self.linha_declaracao}{', ' + attrs_str if attrs_str else ''})>"

class Funcao(Simbolo):
    def __init__(self, nome: str, tipo_retorno: str, parametros: list, linha_declaracao: int,
                 natureza: str = "funcao", **kwargs):
        super().__init__(
            nome=nome,
            tipo=self._gerar_tipo(tipo_retorno, parametros),
            linha_declaracao=linha_declaracao,
            natureza=natureza,
            **kwargs
        )
        self.tipo_retorno = tipo_retorno
        self.parametros = parametros
        self.eh_prototipo = natureza == "prototipo_funcao"
        self.eh_principal = kwargs.get('eh_principal', False)

    @staticmethod
    def _gerar_tipo(tipo_retorno: str, parametros: list) -> str:
        tipos_params = [p.tipo if isinstance(p, Variavel) else p['tipo'] for p in parametros]
        return f"funcao({','.join(tipos_params)})->{tipo_retorno}"

    def __repr__(self):
        params_repr = []
        for p in self.parametros:
            if isinstance(p, Variavel):
                params_repr.append(f"{p.nome}:{p.tipo}")
            elif isinstance(p, dict):  # Para protótipos
                params_repr.append(f"{p.get('nome', '?')}:{p.get('tipo', '?')}")
            else:
                params_repr.append(str(p))

        return (f"<Funcao {self.nome} (Retorno: {self.tipo_retorno}, "
                f"Params: [{', '.join(params_repr)}], Linha: {self.linha_declaracao}, "
                f"Principal: {self.eh_principal}, Prototipo: {self.eh_prototipo})>")

class Variavel(Simbolo):
    def __init__(self, nome: str, tipo: str, linha_declaracao: int,
                 eh_parametro: bool = False,
                 eh_vetor: bool = False,
                 dimensoes: int = 0,
                 posicao: int = 0,
                 **kwargs):
        natureza = "parametro" if eh_parametro else "variavel"
        super().__init__(
            nome=nome,
            tipo=tipo,
            linha_declaracao=linha_declaracao,
            natureza=natureza,
            **kwargs
        )
        self.eh_parametro = eh_parametro
        self.eh_vetor = eh_vetor
        self.dimensoes = dimensoes
        self.posicao = posicao
        self.valor_inicial = kwargs.get('valor_inicial')
        self.tamanhos = kwargs.get('tamanhos', [])  # Para vetores multidimensionais

    def __repr__(self):
        detalhes = [
            f"Tipo: {self.tipo}",
            f"Natureza: {self.natureza}",
            f"Linha: {self.linha_declaracao}"
        ]
        if self.eh_parametro:
            detalhes.append(f"Param: Sim (Pos: {self.posicao})")
        if self.eh_vetor:
            detalhes.append(f"Vetor: Sim (Tamanhos: {self.tamanhos}, Dims: {self.dimensoes})")
        if self.valor_inicial is not None:
            detalhes.append(f"ValorInicial: {self.valor_inicial}")

        return f"<Variavel {self.nome} ({', '.join(detalhes)})>"

class TabelaDeSimbolos:
    def __init__(self):
        # Uma lista de dicionários para representar a pilha de contextos.
        # O primeiro dicionário é o contexto global.
        self.pilha_contextos: List[Dict[str, Union[Simbolo, Funcao, Variavel]]] = [{}]
        self.historico_contextos = []  # Armazena todos os contextos já processados

    def __str__(self):
        """Retorna uma representação em string da tabela de símbolos incluindo histórico"""
        representation = "=== Tabela de Símbolos Completa ===\n"

        # 1. Pilha de contextos atuais (como já está)
        representation += "--- Contextos Ativos (Pilha) ---\n"
        for i, contexto in enumerate(reversed(self.pilha_contextos)):
            nivel_real = len(self.pilha_contextos) - i
            representation += f"  Nível {nivel_real} (Índice {len(self.pilha_contextos) - 1 - i}):\n"
            if contexto:
                for nome, info in contexto.items():
                    representation += f"    '{nome}': {info}\n"
            else:
                representation += "    <contexto vazio>\n"
        representation += "-------------------------------------------\n"

        # 2. Histórico de contextos (se existir)
        if hasattr(self, 'historico_contextos') and self.historico_contextos:
            representation += "\n--- Histórico de Contextos (já fechados) ---\n"
            for i, contexto in enumerate(self.historico_contextos):
                representation += f"  Contexto Histórico #{i + 1}:\n"
                if contexto:
                    for nome, simbolo in contexto.items():
                        representation += f"    '{nome}': {simbolo}\n"
                else:
                    representation += "    <contexto vazio>\n"

        representation += "=================================\n"
        return representation

    def entrar_contexto(self):
        """Adiciona um novo contexto (nível) à pilha."""
        self.pilha_contextos.append({})
        debug_print(f"Entrou num novo contexto. Nível atual: {len(self.pilha_contextos)}")

    def sair_contexto(self):
        """Remove o contexto atual (mais interno) da pilha."""
        if len(self.pilha_contextos) > 1:
            contexto_removido = self.pilha_contextos.pop()
            self.historico_contextos.append(contexto_removido)  # Preserva
            debug_print(f"Saiu do contexto. Nível atual: {len(self.pilha_contextos)}")
        else:
            debug_print("Tentativa de sair do contexto global (ignorado).")
            raise RuntimeError("Não é possível remover o contexto global.")

    def declarar(self, simbolo: Union[Simbolo, Funcao, Variavel]) -> bool:
        """Declara um símbolo no escopo atual. Retorna False se já existir."""
        if simbolo.nome in self.pilha_contextos[-1]:
            print(f"ERRO: Símbolo '{simbolo.nome}' já declarado (linha {simbolo.linha_declaracao}).")
            return False
        self.pilha_contextos[-1][simbolo.nome] = simbolo
        return True

    def buscar(self, nome: str) -> Optional[Union[Simbolo, Funcao, Variavel]]:
        """Busca um símbolo do escopo atual até o global."""
        for contexto in reversed(self.pilha_contextos):
            if nome in contexto:
                return contexto[nome]
        return None

    def buscar_no_contexto_atual(self, nome: str) -> Optional[Union[Simbolo, Funcao, Variavel]]:
        """
        Busca um símbolo APENAS no contexto atual (não procura nos contexto pais).
        Retorna None se não encontrado.
        """
        return self.pilha_contextos[-1].get(nome)

    def declarar_simbolo(self, nome: str, tipo: str, linha: int, info_adicional=None):
        """
        Declara um novo símbolo no contexto atual.
        Retorna True se declarado com sucesso, False se já existe no contexto atual.
        """
        contexto_atual = self.pilha_contextos[-1]
        if nome in contexto_atual:
            print(f"ERRO: Símbolo '{nome}' já declarado no contexto atual (linha {linha}).")
            return False
        contexto_atual[nome] = {'tipo': tipo, 'linha_declaracao': linha, 'info': info_adicional or {}}
        return True

    def buscar_simbolo(self, nome: str):
        """
        Busca um símbolo na pilha de contextos, do mais interno para o mais externo.
        Retorna as informações do símbolo se encontrado, caso contrário None.
        """
        # Itera da última (mais interna) tabela para a primeira (global)
        for contexto in reversed(self.pilha_contextos):
            if nome in contexto:
                return contexto[nome]
        return None

    def buscar_simbolo_no_contexto_atual(self, nome: str) -> dict | None:
        """
        Busca um símbolo APENAS no contexto atual (o último da pilha).
        Útil para verificar redeclarações ou para lógica que não deve
        considerar sombreamento de contextos mais externos.

        Args:
            nome (str): O nome do símbolo a ser buscado.

        Returns:
            dict | None: Um dicionário contendo as informações do símbolo se encontrado
                         APENAS no contexto atual, caso contrário, None.
        """
        contexto_atual = self.pilha_contextos[-1]
        if nome in contexto_atual:
            debug_print(f"Símbolo '{nome}' encontrado no contexto ATUAL (nível {len(self.pilha_contextos)}).")
            return contexto_atual[nome]
        debug_print(f"Símbolo '{nome}' NÃO encontrado no contexto ATUAL (nível {len(self.pilha_contextos)}).")
        return None

    def atualizar_valor_inicial(self, nome_simbolo: str, novo_valor_inicial) -> bool:
        """
        Atualiza o valor inicial de um símbolo (Variavel) na tabela.
        Busca o símbolo em todos os contextos.

        Args:
            nome_simbolo (str): O nome do símbolo a ser atualizado.
            novo_valor_inicial: O novo valor inicial a ser atribuído.

        Returns:
            bool: True se o valor foi atualizado com sucesso, False caso contrário.
        """
        simbolo = self.buscar_simbolo_no_contexto_atual(nome_simbolo)

        if simbolo:
            if isinstance(simbolo, Variavel):
                valor_antigo = simbolo.valor_inicial
                simbolo.valor_inicial = novo_valor_inicial
                # Se o símbolo tem outros atributos que dependem do valor,
                # pode ser necessário atualizá-los aqui também.
                # Por exemplo, se o tipo pudesse ser inferido do valor.
                debug_print(f"Valor inicial de '{nome_simbolo}' atualizado de '{valor_antigo}' para '{novo_valor_inicial}'.")
                return True
            else:
                debug_print(f"ERRO: Símbolo '{nome_simbolo}' encontrado, mas não é uma Variavel (tipo: {type(simbolo).__name__}). Não é possível atualizar valor inicial.")
                return False
        else:
            debug_print(f"ERRO: Símbolo '{nome_simbolo}' não encontrado. Não é possível atualizar valor inicial.")
            return False