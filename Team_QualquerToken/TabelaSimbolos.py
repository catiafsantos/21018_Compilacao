from typing import List, Dict, Optional, Union


class Simbolo:
    """Classe base para todos os símbolos (variáveis, funções, parâmetros, etc.)."""

    def __init__(
            self,
            nome: str,
            tipo: str,
            linha_declaracao: int,
            natureza: str,
            **atributos_adicionais
    ):
        self.nome = nome
        self.tipo = tipo
        self.linha_declaracao = linha_declaracao
        self.natureza = natureza  # 'variavel', 'funcao', 'parametro', 'constante'
        self.atributos = atributos_adicionais  # Ex.: valor_inicial, escopo, etc.

    def __repr__(self):
        return f"<Simbolo {self.nome} ({self.tipo}) @{self.linha_declaracao}>"


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


class TabelaDeSimbolos:
    def __init__(self):
        # Uma lista de dicionários para representar a pilha de contextos.
        # O primeiro dicionário é o contexto global.
        #self.pilha_contextos = [{}]
        self.pilha_contextos: List[Dict[str, Union[Simbolo, Funcao, Variavel]]] = [{}]

        print("Tabela de Símbolos inicializada.")

    def __str__(self):
        """Retorna uma representação em string da tabela de símbolos (para debugging)."""
        representation = "--- Tabela de Símbolos (Pilha de Contexto) ---\n"
        for i, contexto in enumerate(reversed(self.pilha_contextos)):  # Imprime do mais interno para o mais externo
            nivel_real = len(self.pilha_contextos) - i
            representation += f"  Nível {nivel_real} (Índice {len(self.pilha_contextos) - 1 - i}):\n"
            if contexto:
                for nome, info in contexto.items():
                    representation += f"    '{nome}': {info}\n"
            else:
                representation += "    <contexto vazio>\n"
        representation += "-------------------------------------------\n"
        return representation

    def entrar_contexto(self):
        """Adiciona um novo contexto (nível) à pilha."""
        #self.pilha_contextos.append({})
        self.pilha_contextos.append({})
        print(f"DEBUG: Entrou num novo contexto. Nível atual: {len(self.pilha_contextos)}")

    def sair_contexto(self):
        """Remove o contexto atual (mais interno) da pilha."""
        if len(self.pilha_contextos) > 1:
            self.pilha_contextos.pop()
            print(f"DEBUG: Saiu do contexto. Nível atual: {len(self.pilha_contextos)}")
        else:
            print("DEBUG: Tentativa de sair do contexto global (ignorado).")
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
        # print(f"DEBUG: Declarado '{nome}' (tipo: {tipo}, linha: {linha}) no contexto atual.")
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
            print(f"DEBUG: Símbolo '{nome}' encontrado no contexto ATUAL (nível {len(self.pilha_contextos)}).")
            return contexto_atual[nome]

        print(f"DEBUG: Símbolo '{nome}' NÃO encontrado no contexto ATUAL (nível {len(self.pilha_contextos)}).")
        return None
