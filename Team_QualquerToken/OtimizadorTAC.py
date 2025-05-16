import copy

DEBUG_MODE_OTIMIZADOR_TAC = True

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



class OtimizadorTAC:
    def __init__(self, tac_quadruplos, variaveis_utilizador=None):
        # Cria uma cópia profunda dos quadruplos para garantir que os dados originais não são alterados durante a otimização
        self.quadruplos = copy.deepcopy(tac_quadruplos)

        # Conjunto de variáveis que devem ser preservadas mesmo que pareçam não ser usadas (ex: outputs do utilizador)
        self.variaveis_utilizador = variaveis_utilizador or set()

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
        constantes_resolvidas = {}        # Mapeia variáveis para os seus valores constantes
        constantes = {}
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
                        novos_quadruplos.append({"op":"=", "arg1": resultado, "res": res})
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
                            changed_in_pass = True
                    else:  # Atribuindo um valor não constante (variável ou expressão não dobrada)
                        if res in constantes_resolvidas:
                            #print(f"[DEBUG]  [ConstProp] Pass {nr_iteracoes}, Quad {i}: {res} removido do mapa de constantes (instrução: {q})")
                            del constantes_resolvidas[res]
                            changed_in_pass = True
#                elif op == "_": # Indice de array
#                    novos_quadruplos.append(q)
#                    continue
#                    if c1:  # Atribuindo uma constante
#                        if res not in constantes_resolvidas or constantes_resolvidas[res] != str(v1) + "*" + str(v2):
#                            #print(f"[DEBUG]  [ConstProp] Pass {nr_iteracoes}, Quad {i}: {res} ← {v1} (de {arg1})")
#                            constantes_resolvidas[res] = str(v1) + "*" + str(v2)
#                            changed_in_pass = True
#                    else:  # Atribuindo um valor não constante (variável ou expressão não dobrada)
#                        if res in constantes_resolvidas:
#                            #print(f"[DEBUG]  [ConstProp] Pass {nr_iteracoes}, Quad {i}: {res} removido do mapa de constantes (instrução: {q})")
#                            del constantes_resolvidas[res]
#                            changed_in_pass = True
#                elif op in {"-", "*", "/", "%"}:
#                    continue
                elif op in {"label"}:
                    #funcoes ou main
                    novos_quadruplos.append(q)
                    continue
                else:
                    print(f" op não tratado: {op}")

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

    # Método eliminar_codigo_inatingivel: remove instruções que nunca poderão ser executadas (por exemplo, após um return ou goto)
    def eliminar_codigo_inatingivel(self):
        novos_quadruplos = []  # Lista de instruções que devem ser mantidas
        ignorar = False        # Flag para indicar se estamos num bloco de código inatingível
        eliminadas = []        # Guardar instruções eliminadas para debug

        for q in self.quadruplos:
            if ignorar:
                if q["op"] == "label":
                    ignorar = False
                    novos_quadruplos.append(q)
                else:
                    eliminadas.append(q)  # <-- Guarda a instrução eliminada
                    continue
            else:
                novos_quadruplos.append(q)
                if q["op"] in {"goto", "return"}:
                    ignorar = True

        # DEBUG: Mostrar o que foi eliminado
        for q in eliminadas:
            debug_print(f"[DEBUG]  [Inatingível] Eliminada: {q}")

        self.quadruplos = novos_quadruplos
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

# Função de conveniência otimizar_completo: aplica todas as otimizações ao código TAC fornecido
def otimizar_completo(tac_quadruplos, variaveis_utilizador=None):
    otimizador = OtimizadorTAC(tac_quadruplos, variaveis_utilizador)

    print("\n=== Início das Otimizações ===")

    print("\n[1] Constant Folding (primeira passagem)")
    otimizador.constant_folding()
    
    print("\n[2] Propagação de Cópias")
    otimizador.propagacao_copias()

    print("\n[3] Eliminação de Subexpressões Comuns (CSE)")
    otimizador.eliminar_subexpressoes_comuns_CSE()

    print("\n[4] Loop Invariant Code Motion")
    otimizador.mover_invariantes()

    print("\n[5] Constant Folding (segunda passagem)")
    otimizador.constant_folding()

    print("\n[6] Propagação de Cópias(segunda passagem)")
    otimizador.propagacao_copias()

    print("\n[7] Eliminação de Código Inatingível")
    otimizador.eliminar_codigo_inatingivel()

    print("\n[8] Eliminação de Código Morto (com iterações)")
    # Fase 2 — aplicar eliminação de código morto até estabilizar (ponto fixo)
    prev = None
    atual = otimizador.eliminar_codigo_morto()
    iteracao = 1
    while prev != atual:
        print(f"[8.{iteracao}] - Iteração de código morto")
        prev = atual
        atual = otimizador.eliminar_codigo_morto()
        iteracao += 1

    print("\n=== Fim das Otimizações ===")
    return atual