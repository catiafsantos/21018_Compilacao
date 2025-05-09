# Exemplo muito simplificado de uma Tabela de Símbolos
class TabelaDeSimbolos:
    def __init__(self):
        # Uma lista de dicionários para representar a pilha de contextos.
        # O primeiro dicionário é o contexto global.
        self.contextos = [{}] 
        print("Tabela de Símbolos inicializada.")

    def __str__(self):
        """Retorna uma representação em string da tabela de símbolos (para debugging)."""
        representation = "--- Tabela de Símbolos (Pilha de Escopos) ---\n"
        for i, contexto in enumerate(reversed(self.contextos)): # Imprime do mais interno para o mais externo
            nivel_real = len(self.contextos) - i
            representation += f"  Nível {nivel_real} (Índice {len(self.contextos) - 1 - i}):\n"
            if contexto:
                for nome, info in contexto.items():
                    representation += f"    '{nome}': {info}\n"
            else:
                representation += "    <contexto vazio>\n"
        representation += "-------------------------------------------\n"
        return representation

    def entrar_contexto(self):
        """Adiciona um novo contexto (nível) à pilha."""
        self.contextos.append({})
        print(f"DEBUG: Entrou em novo contexto. Nível atual: {len(self.contextos)}")

    def sair_contexto(self):
        """Remove o contexto atual (mais interno) da pilha."""
        if len(self.contextos) > 1: # Não remove o contexto global
            self.contextos.pop()
            print(f"DEBUG: Saiu do contexto. Nível atual: {len(self.contextos)}")
        else:
            print("DEBUG: Tentativa de sair do contexto global (ignorado).")

    def declarar_simbolo(self, nome: str, tipo: str, linha: int, info_adicional=None):
        """
        Declara um novo símbolo no contexto atual.
        Retorna True se declarado com sucesso, False se já existe no contexto atual.
        """
        contexto_atual = self.contextos[-1]
        if nome in contexto_atual:
            print(f"ERRO: Símbolo '{nome}' já declarado no contexto atual (linha {linha}).")
            return False
        contexto_atual[nome] = {'tipo': tipo, 'linha_declaracao': linha, 'info': info_adicional or {}}
        #print(f"DEBUG: Declarado '{nome}' (tipo: {tipo}, linha: {linha}) no contexto atual.")
        return True

    def buscar_simbolo(self, nome: str):
        """
        Busca um símbolo na pilha de contextos, do mais interno para o mais externo.
        Retorna as informações do símbolo se encontrado, caso contrário None.
        """
        # Itera da última (mais interna) tabela para a primeira (global)
        for contexto in reversed(self.contextos):
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
        contexto_atual = self.contextos[-1]
        if nome in contexto_atual:
            print(f"DEBUG: Símbolo '{nome}' encontrado no contexto ATUAL (nível {len(self.contextos)}).")
            return contexto_atual[nome]

        print(f"DEBUG: Símbolo '{nome}' NÃO encontrado no contexto ATUAL (nível {len(self.contextos)}).")
        return None

