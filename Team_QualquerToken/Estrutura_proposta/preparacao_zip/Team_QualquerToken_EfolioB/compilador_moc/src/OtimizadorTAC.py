import copy
from typing import List, Tuple, Dict, Set, Optional

DEBUG_MODE_OTIMIZADOR_TAC = False

def debug_print(*args, **kwargs):
    """Imprime apenas se DEBUG_MODE for True."""
    if DEBUG_MODE_OTIMIZADOR_TAC:
        print("DEBUG:", *args, **kwargs)

# Classe OtimizadorTAC: responsável por aplicar otimizações ao código intermédio em formato de quadruplos (TAC)
def is_literal_constant(operand):
    """Verifica se um operando é um literal constante (número ou booleano)."""
    return isinstance(operand, (int, float, bool))

def resolve_operand(operand, constant_map):
    """
    Resolve um operando.
    Retorna (valor_do_operando, é_constante_conhecida).
    """
    # 1) Se for string que representa número, converte a int/float e diz que é constante
    if isinstance(operand, str):
        try:
            # tenta inteiro primeiro
            val = int(operand)
        except ValueError:
            try:
                val = float(operand)
            except ValueError:
                val = None
        else:
            return val, True  # era string numérica, agora int

        if val is not None:
            return val, True  # era float válido

    # 2) Se for já int/float/bool
    if is_literal_constant(operand):
        return operand, True

    # 3) Se for nome de variável já resolvida
    if isinstance(operand, str) and operand in constant_map:
        return constant_map[operand], True

    return operand, False


class BlocoBasico:
    """Representa um bloco básico no Grafo de Fluxo de Controlo."""
    def __init__(self, id_bloco: int, inicio_idx: int):
        self.id_bloco: int = id_bloco
        self.inicio_idx: int = inicio_idx # Índice da primeira quádrupla no TAC original
        self.fim_idx: int = -1          # Índice da última quádrupla no TAC original
        self.quadruplas: TAC = []
        self.sucessores: List[int] = [] # Lista de IDs de blocos sucessores
        self.predecessores: List[int] = [] # Lista de IDs de blocos predecessores (preenchimento opcional)

    def __repr__(self):
        return (f"Bloco(id={self.id_bloco}, "
                f"quads=[{self.inicio_idx}-{self.fim_idx}], "
                f"sucessores={self.sucessores})")

# Define o tipo para uma quádrupla
Quadrupla = Tuple[str, Optional[str], Optional[str], Optional[str]]
# Define o tipo para uma lista de quádruplas (TAC)
TAC = List[Quadrupla]


class OtimizadorTAC:
    def __init__(self, tac_quadruplos, variaveis_utilizador=None):
        # Cria uma cópia profunda dos quadruplos para garantir que os dados originais não são alterados durante a otimização
        self.quadruplos = copy.deepcopy(tac_quadruplos)

        # Conjunto de variáveis que devem ser preservadas mesmo que pareçam não ser usadas (ex: outputs do utilizador)
        self.variaveis_utilizador = variaveis_utilizador or set()
        # O estado dos blocos pode ser armazenado na instância se for útil para múltiplas otimizações
        self.blocos: List[BlocoBasico] = []
        self.mapa_labels_para_id_bloco: Dict[str, int] = {}
        self.mapa_idx_lider_para_id_bloco: Dict[int, int] = {}


    # Método eliminar_codigo_morto: remove instruções cujo resultado não tem impacto no restante do programa
    def eliminar_codigo_morto(self):
        vivas = set()      # Conjunto de variáveis "vivas", ou seja, cujo valor ainda vai ser utilizado mais à frente
        otimizados = []    # Lista de quadruplos que serão mantidos após a otimização
        eliminadas = []  # Lista de instruções eliminadas

        # Primeiro passo: identificar todas as variáveis que são utilizadas como argumentos nos quadruplos
        usados = set()
        for q in self.quadruplos:
            for arg in ("arg1", "arg2"):
                if isinstance(q.get(arg), str):  # Só se for string (nome de variável)
                    usados.add(q[arg])           # Adiciona ao conjunto de variáveis potencialmente relevantes
        debug_print(f"[DEBUG]  [Morto] Variáveis usadas na primeira fase: {usados}")

        # Segundo passo: percorre os quadruplos de trás para a frente (técnica comum para análise de liveness)
        for q in reversed(self.quadruplos):
            debug_print(f"[DEBUG]  [Morto] Vivas antes de {q}: {vivas}")
            op = q["op"]
            res = q.get("res")    # Resultado do quadruplo (variável que recebe o valor)
            arg1 = q.get("arg1")  # Primeiro argumento (ex: operando esquerdo)
            arg2 = q.get("arg2")  # Segundo argumento (ex: operando direito)

            # Define se a operação tem efeitos colaterais — neste caso, a instrução deve ser sempre preservada
            efeito_colateral = op in {
                "call", "return", "write", "writes", "writec", "writev",
                "goto", "ifgoto", "ifFalse", "label", "alloc", "[]="
            }

            # Verifica se a instrução é uma atribuição direta desnecessária, ou seja:
            # - do tipo `res = arg1`
            # - `res` não está em uso
            # - não tem efeito colateral
            atribuicao_direta_inutil = (
                op == "=" and
                isinstance(res, str) and
                res not in usados and
                not efeito_colateral
            )

            # Três casos principais em que a instrução é preservada:

            # 1. Se tiver efeito colateral, ou a variável de resultado for usada, ou estiver na lista de variáveis do utilizador
            if efeito_colateral or (res and res in vivas) or (res in self.variaveis_utilizador):
                otimizados.append(q)
                # Atualiza o conjunto de variáveis vivas com os argumentos da operação
                if isinstance(arg1, str):
                    vivas.add(arg1)
                if isinstance(arg2, str):
                    vivas.add(arg2)

            # 2. Se a instrução não tem resultado (como labels, goto, etc.), assume-se que tem utilidade estrutural
            elif not res:
                otimizados.append(q)
                if isinstance(arg1, str):
                    vivas.add(arg1)
                if isinstance(arg2, str):
                    vivas.add(arg2)

            # 3. Se não for uma atribuição direta inútil (ou seja, tem alguma utilidade), também é mantida
            elif not atribuicao_direta_inutil:
                otimizados.append(q)
                if isinstance(arg1, str):
                    vivas.add(arg1)
                if isinstance(arg2, str):
                    vivas.add(arg2)
            
            else:
                eliminadas.append(q)  # Marcar como eliminada

        # DEBUG: imprime o que foi removido
        for q in eliminadas:
            debug_print(f"[DEBUG]  [Morto] Eliminado: {q}")

        # Por ter sido percorrido de trás para a frente, é necessário inverter a lista final para restaurar a ordem original
        self.quadruplos_otimizados = list(reversed(otimizados))

        # Devolve a lista de quadruplos depois da otimização
        return self.quadruplos_otimizados

    # Método propagacao_copias: substitui variáveis copiadas por outras equivalentes 
    def propagacao_copias(self):
        substituicoes = {}              # Mapeia variáveis de destino para o valor original copiado (ex: b = a → substituicoes[b] = a)
        resultado = []                  # Lista final de quadruplos com as substituições aplicadas
        atribuicoes = {}                # Conta quantas vezes cada variável é atribuída (útil para saber se é seguro substituir)
        modificadas_em_ciclos = set()  # Conjunto de variáveis que são modificadas dentro de ciclos (ramos, saltos, etc.)

        # 1. Recolher estatísticas sobre atribuições
        for q in self.quadruplos:
            res = q.get("res")
            if res:
                # Conta quantas vezes cada variável foi atribuída
                atribuicoes[res] = atribuicoes.get(res, 0) + 1

            # Se a operação estiver relacionada com controlo de fluxo,
            # considera que a variável foi modificada num ciclo
            if q["op"] in {"goto", "ifFalse", "ifgoto", "label"}:
                if res:
                    modificadas_em_ciclos.add(res)

        # 2. Substituir apenas variáveis seguras (atribuídas 1 vez e fora de ciclos)
        for q in self.quadruplos:
            op = q["op"]
            arg1 = q.get("arg1")
            arg2 = q.get("arg2")
            res = q.get("res")

            # Substitui os argumentos se forem variáveis com cópia conhecida (já propagada)
            if isinstance(arg1, str) and arg1 in substituicoes:
                # Debug de propragação de cópias
                debug_print(f"[DEBUG]  [Substituição] {arg1} → {substituicoes[arg1]} na operação {q}")
                q["arg1"] = substituicoes[arg1]
            if isinstance(arg2, str) and arg2 in substituicoes:
                debug_print(f"[DEBUG]  [Substituição] {arg2} → {substituicoes[arg2]} na operação {q}")
                q["arg2"] = substituicoes[arg2]    

            # Propagação direta de cópia: se for uma atribuição simples (res = arg1)
            if op == "=" and arg1 and res:
                # Só propaga se:
                # - a variável de destino (res) foi atribuída **apenas uma vez**
                # - **não** foi usada em instruções de controlo de fluxo (ciclos)
                if atribuicoes.get(res, 0) == 1 and res not in modificadas_em_ciclos:
                    # Adiciona a substituição: res ≡ arg1 (usa-se o valor original de arg1)
                    substituicoes[res] = substituicoes.get(arg1, arg1)
                    # Debug de propragação de cópias
                    debug_print(f"[DEBUG]  [Cópia] {res} ← {arg1}")

                else:
                    # Se não for seguro, remove substituição existente para evitar erro
                    if res in substituicoes:
                        # Debug de propragação de cópias
                        debug_print(f"[DEBUG]  Substituição de {res} invalidada por operação {op}")
                        del substituicoes[res]
            else:
                # Qualquer operação que escreva em `res` invalida substituições anteriores
                if res and res in substituicoes:
                    # Debug de propragação de cópias
                    debug_print(f"[DEBUG]  Substituição de {res} invalidada por operação '{op}'")
                    del substituicoes[res]

            # Adiciona a instrução (eventualmente com substituições aplicadas)
            resultado.append(q)

        # Atualiza a lista de quadruplos otimizada
        self.quadruplos = resultado
        return self.quadruplos

    # Método constant_folding: avalia operações com constantes em tempo de compilação, substituindo-as pelo valor calculado
    def constant_folding(self):
        """
        Dobra expressões binárias de constantes e propaga atribuições de constantes.
        """
        novos_quadruplos = []             # Lista final de quadruplos com constantes já resolvidas
        constantes_resolvidas = {}        # Mapeia variáveis para os seus valores constantes        constantes = {}
        fez_alteracoes = True

        while fez_alteracoes:
            fez_alteracoes = False
            novos_quadruplos.clear()

            for q in self.quadruplos:
                op   = q["op"]
                arg1 = q.get("arg1")
                arg2 = q.get("arg2")
                res  = q.get("res")

                # Resolve operandos (literal ou já em constantes)
                v1, c1 = resolve_operand(arg1, constantes_resolvidas) if arg1 is not None else (None, False)
                v2, c2 = resolve_operand(arg2, constantes_resolvidas) if arg2 is not None else (None, False)

                # 1) Folding de binários constantes
                if op in {"+", "-", "*", "/", "%", "==", "!=", "<", "<=", ">", ">="} and c1 and c2:
                    try:
                        resultado = self._avaliar_constante(op, v1, v2)
                        constantes_resolvidas[res] = resultado
                        novos_quadruplos.append({"op":"=", "arg1": resultado, "res": res, "arg2": None})
                        debug_print(f"[DEBUG]  [Folding] {arg1} {op} {arg2} → {resultado}")
                        fez_alteracoes = True
                        continue
                    except ZeroDivisionError:
                        # mantém a instrução original se divisão por zero
                        pass

                # Substitui índices de vetor se o índice (arg1) já tiver sido resolvido como constante
                elif op == "[]=" and arg2 in constantes_resolvidas:
                    idx = constantes_resolvidas[arg2]
                    if c2:
                        aux = str(arg1) + "[" + str(arg2) + "]"
                        if aux not in constantes_resolvidas:
                            constantes_resolvidas[aux] = res
                            novos_quadruplos.append({"op": "[]=", "arg1": arg1, "arg2": str(idx), "res": res})

                    continue
                elif op == "=":
                    if c1:  # Atribuindo uma constante
                        if res not in constantes_resolvidas or constantes_resolvidas[res] != v1:
                            #print(f"[DEBUG]  [ConstProp] Pass {nr_iteracoes}, Quad {i}: {res} ← {v1} (de {arg1})")
                            constantes_resolvidas[res] = v1
                    else:  # Atribuindo um valor não constante (variável ou expressão não dobrada)
                        if res in constantes_resolvidas:
                            #print(f"[DEBUG]  [ConstProp] Pass {nr_iteracoes}, Quad {i}: {res} removido do mapa de constantes (instrução: {q})")
                            del constantes_resolvidas[res]
                elif op in {"label"}:
                    #funcoes ou main
                    novos_quadruplos.append(q)
                    continue
                else:
                    debug_print(f" op não tratado: {op}")

                # Senão mantém o quadruplo original
                novos_quadruplos.append(q)

            # Prepara próxima iteração
            self.quadruplos = novos_quadruplos.copy()

        return self.quadruplos


    # Método eliminar_subexpressoes_comuns_CSE: evita recalcular expressões já computadas anteriormente com os mesmos operandos
    def eliminar_subexpressoes_comuns_CSE(self):
        expressoes_vistas = {}   # Dicionário que mapeia expressão (com versão) para o resultado previamente calculado
        versao_vars = {}         # Registo das versões de cada variável (muda sempre que a variável é modificada)
        resultado = []           # Lista de quadruplos com subexpressões redundantes substituídas

        # Função auxiliar para normalizar expressões comutativas (ordem dos operandos não importa)
        def normalizar(op, arg1, arg2):
            if op in {"+", "*", "==", "!=", "<=", ">="} and arg1 and arg2:
                return (op, *sorted([arg1, arg2]))
            return (op, arg1, arg2)

        # Função auxiliar para gerar a chave única que representa uma expressão com a versão atual dos seus operandos
        def chave_versao(expr):
            op, a1, a2 = expr
            v1 = versao_vars.get(a1, 0) if isinstance(a1, str) else 0
            v2 = versao_vars.get(a2, 0) if isinstance(a2, str) else 0
            return (op, a1, v1, a2, v2)

        for q in self.quadruplos:
            op = q["op"]
            arg1 = q.get("arg1")
            arg2 = q.get("arg2")
            res = q.get("res")

            # Se for uma operação binária com resultado (elegível para eliminação de subexpressão)
            if op in {"+", "-", "*", "/", "%", "==", "!=", "<", "<=", ">", ">="} and res:
                expr = normalizar(op, arg1, arg2)
                expr_com_versao = chave_versao(expr)

                # Se já foi vista a mesma expressão com os mesmos operandos e versões,
                # então não vale a pena calcular de novo: usa o resultado anterior
                if expr_com_versao in expressoes_vistas:
                    res_antigo = expressoes_vistas[expr_com_versao]
                    # Debug de eliminação de subexpressões comuns
                    debug_print(f"[DEBUG]  [CSE] Subexpressão {expr} já vista → substitui por {res_antigo}")
                    resultado.append({"op": "=", "arg1": res_antigo, "res": res})
                else:
                    # Caso contrário, regista esta nova expressão como já vista
                    expressoes_vistas[expr_com_versao] = res
                    # Debug de eliminação de subexpressões comuns
                    debug_print(f"[DEBUG]  [CSE] Nova subexpressão {expr} registada → {res}")
                    resultado.append(q)
            else:
                # Se não for uma operação elegível, mantém a instrução como está
                resultado.append(q)

            # Se a variável res for modificada, incrementa a sua versão
            if res and isinstance(res, str):
                versao_vars[res] = versao_vars.get(res, 0) + 1

        # Substitui os quadruplos antigos pelos otimizados
        self.quadruplos = resultado
        return self.quadruplos

    # Método auxiliar _is_const: verifica se o argumento representa uma constante numérica (int ou float)
    def _is_const(self, val):
        if not isinstance(val, str): return False
        try:
            float(val)  # Tenta converter para número
            return True
        except ValueError:
            return False

    # Método auxiliar _avaliar_constante: realiza a operação entre duas constantes e devolve o resultado
    def _avaliar_constante(self, op, v1, v2):
        if op == "+": return v1 + v2
        if op == "-": return v1 - v2
        if op == "*": return v1 * v2
        if op == "/": return v1 / v2
        if op == "%": return v1 % v2
        if op == "==":  return v1 == v2
        if op == "!=":  return v1 != v2
        if op == "<":   return v1 < v2
        if op == "<=":  return v1 <= v2
        if op == ">":   return v1 > v2
        if op == ">=":  return v1 >= v2

    # Método mover_invariantes: Loop-Invariant Code Motion - move instruções que são invariantes dentro de ciclos para fora do loop
    def mover_invariantes(self):
        # 1) Construir um dicionário que associa o nome dos labels aos seus índices na lista de quadruplos
        label_idx = {
            q["res"]: i
            for i, q in enumerate(self.quadruplos)
            if q["op"] == "label" and isinstance(q.get("res"), str)
        }

        # Conjunto com operações que têm efeitos colaterais e que não podem ser movidas
        side_effects = {
            "call", "return", "write", "writes", "writec", "writev",
            "alloc", "[]=", "goto", "ifgoto", "ifFalse", "label"
        }

        # Lista onde vamos guardar instruções consideradas invariantes
        invariantes = []

        # 2) Procurar loops detetando saltos para trás (back-edges)
        for i, q in enumerate(self.quadruplos):
            op = q["op"]
            # Só nos interessam saltos (possíveis inícios de loops)
            if op not in {"goto", "ifgoto", "ifFalse"}:
                continue

            # Verificar qual campo da instrução contém o destino (label)
            possiveis = [
                (campo, q[campo])
                for campo in ("arg1", "arg2", "res")
                if isinstance(q.get(campo), str) and q[campo] in label_idx
            ]
            if not possiveis:
                continue

            # Extrair o campo que contém o rótulo de destino e o nome desse rótulo
            campo_label, target = possiveis[0]
            start, end = label_idx[target], i

            # Só consideramos loops com back-edge (target anterior ao salto)
            if start >= end:
                continue

            # 3) Recolher todas as variáveis que são atribuídas dentro do loop
            defs = {
                r["res"]
                for r in self.quadruplos[start:end+1]
                if isinstance(r.get("res"), str)
            }

            # 4) Procurar instruções que são invariantes no loop
            for j in range(start, end):
                instr = self.quadruplos[j]
                # Ignorar instruções com efeitos colaterais
                if instr["op"] in side_effects:
                    continue

                # Obter os argumentos usados na instrução
                args = [
                    a for a in (instr.get("arg1"), instr.get("arg2"))
                    if isinstance(a, str)
                ]

                # A instrução é invariante se nenhum dos argumentos for alterado no loop
                if all(a not in defs for a in args):
                    invariantes.append((start, j, instr))
                    # Debug de loop invariant code motion
                    debug_print(f"[DEBUG]  [Invariante] '{instr}' movida para fora do loop iniciado em label {self.quadruplos[start]['res']}")

        # 5) Remover instruções invariantes do corpo do loop (de trás para a frente)
        for _, j, instr in sorted(invariantes, key=lambda x: x[1], reverse=True):
            self.quadruplos.pop(j)

        # 6) Agrupar as instruções invariantes por label de início de loop
        from collections import defaultdict
        grupos = defaultdict(list)
        for start, _, instr in invariantes:
            grupos[start].append(instr)

        # Inserir cada grupo de instruções antes do início do loop respetivo
        for start, insts in grupos.items():
            offset = 0
            for instr in insts:
                idx = start + offset
                self.quadruplos.insert(idx, instr)
                offset += 1

        # Devolver a nova lista de quadruplos com as invariantes movidas
        return self.quadruplos

    def identificar_lideres(self) -> Set[int]:
        """
        Identifica os líderes no Código de Três Endereços (self.quadruplos).
        Um líder é a primeira instrução de um bloco básico.
        """
        lideres: Set[int] = set()
        if not self.quadruplos:
            return lideres

        lideres.add(0)  # Regra 1

        # Limpa e preenche o mapa de labels para uso interno e em construir_cfg
        self.mapa_labels_para_id_bloco.clear()  # Garante que está limpo se chamado múltiplas vezes
        temp_mapa_labels_idx: Dict[str, int] = {}  # Mapa temporário de nome de label para índice da quádrupla
        for i, quad in enumerate(self.quadruplos):
            if quad['op'] == "label" and quad['res'] is not None:
                temp_mapa_labels_idx[quad['res']] = i

        for i, quad in enumerate(self.quadruplos):

            # Regra 2: Alvo de um salto é um líder
            if quad['op'] in ("goto", "ifFalse"):
                if quad['res'] is not None and quad['res'] in temp_mapa_labels_idx:
                    lideres.add(temp_mapa_labels_idx[quad['res']])

            # Regra 3: Instrução após um salto ou return é um líder
            if quad['op'] in ("goto", "ifFalse", "return"):
                if i + 1 < len(self.quadruplos):
                    lideres.add(i + 1)
        return lideres

    def construir_blocos_basicos(self, lideres: Set[int]) -> List[BlocoBasico]:
        """
        Constrói os blocos básicos a partir do TAC (self.quadruplos) e dos líderes identificados.
        Armazena os blocos em self.blocos.
        """
        if not self.quadruplos:
            self.blocos = []
            return self.blocos

        self.blocos.clear()  # Limpa blocos anteriores
        self.mapa_idx_lider_para_id_bloco.clear()  # Limpa mapa de índices de líderes

        lideres_ordenados = sorted(list(lideres))

        id_bloco_atual = 0
        for i, inicio_lider_idx in enumerate(lideres_ordenados):
            bloco = BlocoBasico(id_bloco_atual, inicio_lider_idx)

            fim_bloco_idx: int
            if i + 1 < len(lideres_ordenados):
                fim_bloco_idx = lideres_ordenados[i + 1] - 1
            else:
                fim_bloco_idx = len(self.quadruplos) - 1

            bloco.fim_idx = fim_bloco_idx
            bloco.quadruplas = self.quadruplos[inicio_lider_idx: fim_bloco_idx + 1]

            self.blocos.append(bloco)
            self.mapa_idx_lider_para_id_bloco[bloco.inicio_idx] = bloco.id_bloco  # Preenche o mapa
            id_bloco_atual += 1

        return self.blocos

    def construir_cfg(self):
        """
        Constrói o Grafo de Fluxo de Controlo (CFG) adicionando arestas (sucessores)
        entre os blocos básicos armazenados em self.blocos.
        Preenche self.mapa_labels_para_id_bloco.
        """
        if not self.blocos:
            return

        # Preenche/atualiza mapa_labels_para_id_bloco com base nos blocos atuais
        self.mapa_labels_para_id_bloco.clear()
        for bloco in self.blocos:
            if bloco.quadruplas and bloco.quadruplas[0]['op'] == "label" and bloco.quadruplas[0]['res'] is not None:
                self.mapa_labels_para_id_bloco[bloco.quadruplas[0]['res']] = bloco.id_bloco

        for i, bloco_atual in enumerate(self.blocos):
            bloco_atual.sucessores.clear()  # Limpa sucessores antigos antes de recalcular
            if not bloco_atual.quadruplas:
                continue

            ultima_quad_bloco = bloco_atual.quadruplas[-1]
            op = ultima_quad_bloco['op']
            resultado_salto = ultima_quad_bloco['res']
            arg1= ultima_quad_bloco['arg1']
            arg2 = ultima_quad_bloco['arg2']
            if op == "goto":
                if resultado_salto is not None and resultado_salto in self.mapa_labels_para_id_bloco:
                    id_bloco_alvo = self.mapa_labels_para_id_bloco[resultado_salto]
                    if id_bloco_alvo not in bloco_atual.sucessores:
                        bloco_atual.sucessores.append(id_bloco_alvo)
            elif op == "ifFalse": # Se testa false e temos valor true nao faz a label destino
                if resultado_salto is not None and resultado_salto in self.mapa_labels_para_id_bloco:
                    if arg1 != True:
                        id_bloco_alvo_salto = self.mapa_labels_para_id_bloco[resultado_salto]
                        if id_bloco_alvo_salto not in bloco_atual.sucessores:
                            bloco_atual.sucessores.append(id_bloco_alvo_salto)
                if arg1 == True:
                    proximo_idx_instrucao = bloco_atual.fim_idx + 1
                    if proximo_idx_instrucao < len(self.quadruplos):
                        if proximo_idx_instrucao in self.mapa_idx_lider_para_id_bloco:
                            id_bloco_alvo_fallthrough = self.mapa_idx_lider_para_id_bloco[proximo_idx_instrucao]
                            if id_bloco_alvo_fallthrough not in bloco_atual.sucessores:
                                bloco_atual.sucessores.append(id_bloco_alvo_fallthrough)
            elif op == "ifTrue":
                if resultado_salto is not None and resultado_salto in self.mapa_labels_para_id_bloco:
                    if arg1 != False:
                        id_bloco_alvo_salto = self.mapa_labels_para_id_bloco[resultado_salto]
                        if id_bloco_alvo_salto not in bloco_atual.sucessores:
                            bloco_atual.sucessores.append(id_bloco_alvo_salto)
                if arg1 == False:
                    proximo_idx_instrucao = bloco_atual.fim_idx + 1
                    if proximo_idx_instrucao < len(self.quadruplos):
                        if proximo_idx_instrucao in self.mapa_idx_lider_para_id_bloco:
                            id_bloco_alvo_fallthrough = self.mapa_idx_lider_para_id_bloco[proximo_idx_instrucao]
                            if id_bloco_alvo_fallthrough not in bloco_atual.sucessores:
                                bloco_atual.sucessores.append(id_bloco_alvo_fallthrough)
            elif op != "return":
                proximo_idx_instrucao = bloco_atual.fim_idx + 1
                if proximo_idx_instrucao < len(self.quadruplos):
                    if proximo_idx_instrucao in self.mapa_idx_lider_para_id_bloco:
                        id_bloco_alvo_sequencial = self.mapa_idx_lider_para_id_bloco[proximo_idx_instrucao]
                        if id_bloco_alvo_sequencial not in bloco_atual.sucessores:
                            bloco_atual.sucessores.append(id_bloco_alvo_sequencial)

    def encontrar_blocos_alcancaveis(self, id_bloco_entrada: int = 0) -> Set[int]:
        """
        Executa uma análise de alcançabilidade (BFS) no CFG (usando self.blocos).
        Assume que o CFG já foi construído.
        """
        blocos_alcancaveis: Set[int] = set()
        if not self.blocos:
            debug_print("Aviso: Lista de blocos vazia em encontrar_blocos_alcancaveis.")
            return blocos_alcancaveis

        fila: List[int] = []

        bloco_de_partida = next((b for b in self.blocos if b.id_bloco == id_bloco_entrada), None)

        if bloco_de_partida:
            blocos_alcancaveis.add(bloco_de_partida.id_bloco)
            fila.append(bloco_de_partida.id_bloco)
        else:
            debug_print(
                f"Aviso: Bloco de entrada com ID {id_bloco_entrada} não encontrado. Nenhum código será considerado alcançável.")
            return blocos_alcancaveis

        while fila:
            id_bloco_atual = fila.pop(0)
            bloco_atual_obj = next((b for b in self.blocos if b.id_bloco == id_bloco_atual), None)

            if bloco_atual_obj is None:
                debug_print(f"Aviso Crítico: Bloco com ID {id_bloco_atual} na fila mas não encontrado.")
                continue

            for id_sucessor in bloco_atual_obj.sucessores:
                sucessor_obj = next((b for b in self.blocos if b.id_bloco == id_sucessor), None)
                if sucessor_obj is None:
                    debug_print(f"Aviso: Sucessor com ID {id_sucessor} do bloco {id_bloco_atual} não é um bloco válido.")
                    continue

                if id_sucessor not in blocos_alcancaveis:
                    blocos_alcancaveis.add(id_sucessor)
                    fila.append(id_sucessor)
        return blocos_alcancaveis

    def remover_codigo_inatingivel_metodo(self) -> TAC:
        """
        Função principal como método para remover código inatingível.
        """
        if not self.quadruplos:
            return []

        debug_print("--- TAC Original (dentro do método) ---")
        for i, q in enumerate(self.quadruplos): debug_print(f"{i:2d}: {q}")

        lideres = self.identificar_lideres()
        debug_print("\n--- Líderes Identificados (índices) (dentro do método) ---")
        debug_print(sorted(list(lideres)))

        self.construir_blocos_basicos(lideres)  # Atualiza self.blocos
        debug_print("\n--- Blocos Básicos Construídos (dentro do método) ---")
        for b in self.blocos: debug_print(b)

        self.construir_cfg()  # Atualiza sucessores em self.blocos e self.mapa_labels_para_id_bloco
        debug_print("\n--- CFG Construído (Sucessores por Bloco) (dentro do método) ---")
        for b in self.blocos: debug_print(
            f"Bloco {b.id_bloco} (quads {b.inicio_idx}-{b.fim_idx}) -> Sucessores: {b.sucessores}")

        ids_blocos_alcancaveis = self.encontrar_blocos_alcancaveis(0)
        debug_print("\n--- IDs de Blocos Alcançáveis (dentro do método) ---")
        debug_print(sorted(list(ids_blocos_alcancaveis)))

        tac_otimizado: TAC = []
        labels_alcancaveis_nos_blocos_otimizados: Set[str] = set()

        # Coleta labels que PERTENCEM a blocos alcançáveis
        for bloco in self.blocos:
            if bloco.id_bloco in ids_blocos_alcancaveis:
                if bloco.quadruplas and bloco.quadruplas[0]['op'] == "label":
                    label_name = bloco.quadruplas[0]['res']
                    if label_name:
                        labels_alcancaveis_nos_blocos_otimizados.add(label_name)

        debug_print("\n--- Labels que pertencem a blocos alcançáveis ---")
        debug_print(labels_alcancaveis_nos_blocos_otimizados)

        for bloco in sorted(self.blocos, key=lambda b: b.inicio_idx):
            if bloco.id_bloco in ids_blocos_alcancaveis:
                for quad in bloco.quadruplas:
                    op, arg1, arg2, res = quad['op'], quad['arg1'], quad['arg2'], quad['res']

                    # Verificação adicional para saltos: o label de destino deve ser de um bloco alcançável
                    if op in ("goto", "ifFalse", "ifTrue"):
                        if res is not None and res not in labels_alcancaveis_nos_blocos_otimizados:
                            debug_print(
                                f"Aviso: Salto em {quad} para label '{res}' que NÃO pertence a um bloco alcançável. A instrução será mantida, mas pode indicar um problema ou uma otimização perdida.")
                        else:
                            tac_otimizado.append(quad)
                    else:
                        tac_otimizado.append(quad)

        self.quadruplos = tac_otimizado
        debug_print("\n--- TAC Otimizado (Código Inatingível Removido) (dentro do método) ---")
        for i, q in enumerate(self.quadruplos): debug_print(f"{i:2d}: {q}")

        return self.quadruplos



# Função de conveniência otimizar_completo: aplica todas as otimizações ao código TAC fornecido
def otimizar_completo(tac_quadruplos, variaveis_utilizador=None):
    otimizador = OtimizadorTAC(tac_quadruplos, variaveis_utilizador)

    debug_print("\n=== Início das Otimizações ===")

    debug_print("\n[1] Constant Folding (primeira passagem)")
    otimizador.constant_folding()
    
    debug_print("\n[2] Propagação de Cópias")
    otimizador.propagacao_copias()

    debug_print("\n[3] Eliminação de Subexpressões Comuns (CSE)")
    otimizador.eliminar_subexpressoes_comuns_CSE()

    debug_print("\n[4] Loop Invariant Code Motion")
    otimizador.mover_invariantes()

    debug_print("\n[5] Constant Folding (segunda passagem)")
    otimizador.constant_folding()

    debug_print("\n[6] Propagação de Cópias(segunda passagem)")
    otimizador.propagacao_copias()

    debug_print("\n[7] Eliminação de Código Inatingível")
    otimizador.remover_codigo_inatingivel_metodo()

    debug_print("\n[8] Eliminação de Código Morto (com iterações)")
    # Fase 2 — aplicar eliminação de código morto até estabilizar (ponto fixo)
    prev = None
    atual = otimizador.eliminar_codigo_morto()
    iteracao = 1
    while prev != atual:
        debug_print(f"[8.{iteracao}] - Iteração de código morto")
        prev = atual
        atual = otimizador.eliminar_codigo_morto()
        iteracao += 1

    debug_print("\n=== Fim das Otimizações ===")
    return atual