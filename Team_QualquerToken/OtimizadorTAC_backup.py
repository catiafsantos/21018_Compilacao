import copy

# Classe OtimizadorTAC: responsável por aplicar otimizações ao código intermédio em formato de quadruplos (TAC)
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

        # Primeiro passo: identificar todas as variáveis que são utilizadas como argumentos nos quadruplos
        usados = set()
        for q in self.quadruplos:
            for arg in ("arg1", "arg2"):
                if isinstance(q.get(arg), str):  # Só se for string (nome de variável)
                    usados.add(q[arg])           # Adiciona ao conjunto de variáveis potencialmente relevantes

        # Segundo passo: percorre os quadruplos de trás para a frente (técnica comum para análise de liveness)
        for q in reversed(self.quadruplos):
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

        # Por ter sido percorrido de trás para a frente, é necessário inverter a lista final para restaurar a ordem original
        self.quadruplos_otimizados = list(reversed(otimizados))

        # Devolve a lista de quadruplos depois da otimização
        return self.quadruplos_otimizados

     # Método propagacao_copias: substitui variáveis copiadas por outras equivalentes quando é seguro fazê-lo
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
                q["arg1"] = substituicoes[arg1]
            if isinstance(arg2, str) and arg2 in substituicoes:
                q["arg2"] = substituicoes[arg2]

            # Propagação direta de cópia: se for uma atribuição simples (res = arg1)
            if op == "=" and arg1 and res:
                # Só propaga se:
                # - a variável de destino (res) foi atribuída **apenas uma vez**
                # - **não** foi usada em instruções de controlo de fluxo (ciclos)
                if atribuicoes.get(res, 0) == 1 and res not in modificadas_em_ciclos:
                    # Adiciona a substituição: res ≡ arg1 (usa-se o valor original de arg1)
                    substituicoes[res] = substituicoes.get(arg1, arg1)
                else:
                    # Se não for seguro, remove substituição existente para evitar erro
                    if res in substituicoes:
                        del substituicoes[res]
            else:
                # Qualquer operação que escreva em `res` invalida substituições anteriores
                if res and res in substituicoes:
                    del substituicoes[res]

            # Adiciona a instrução (eventualmente com substituições aplicadas)
            resultado.append(q)

        # Atualiza a lista de quadruplos otimizada
        self.quadruplos = resultado
        return self.quadruplos
    
    # Método constant_folding: avalia operações com constantes em tempo de compilação, substituindo-as pelo valor calculado
    def constant_folding(self):
        novos_quadruplos = []             # Lista final de quadruplos com constantes já resolvidas
        constantes_resolvidas = {}        # Dicionário que associa variáveis a valores constantes já avaliados

        for q in self.quadruplos:
            op = q["op"]
            arg1 = q.get("arg1")
            arg2 = q.get("arg2")
            res = q.get("res")

            # Aplica a operadores binários com dois operandos constantes (ex: 3 + 4)
            if op in {"+", "-", "*", "/", "%"} and self._is_const(arg1) and self._is_const(arg2):
                try:
                    # Converte os valores para inteiro ou float
                    val1 = float(arg1) if "." in arg1 else int(arg1)
                    val2 = float(arg2) if "." in arg2 else int(arg2)

                    # Calcula o resultado da operação entre constantes
                    resultado = self._avaliar_constante(op, val1, val2)

                    # Guarda o resultado como valor constante associado à variável res
                    constantes_resolvidas[res] = resultado

                    # Substitui a operação pelo resultado direto: res = valor
                    novos_quadruplos.append({"op": "=", "arg1": str(resultado), "res": res})
                    continue  # Passa ao próximo quadruplo
                except ZeroDivisionError:
                    pass  # Em caso de divisão por zero, mantém a instrução original

            # Substitui índices de vetor se o índice (arg1) já tiver sido resolvido como constante
            elif op == "[]=" and arg1 in constantes_resolvidas:
                idx = constantes_resolvidas[arg1]
                novos_quadruplos.append({"op": "[]=", "arg1": str(idx), "arg2": arg2, "res": res})
                continue

            # Caso não se aplique nenhuma substituição, mantém a instrução original
            novos_quadruplos.append(q)

        # Atualiza os quadruplos com os novos, otimizados
        self.quadruplos = novos_quadruplos
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
                    resultado.append({"op": "=", "arg1": res_antigo, "res": res})
                else:
                    # Caso contrário, regista esta nova expressão como já vista
                    expressoes_vistas[expr_com_versao] = res
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

        for q in self.quadruplos:
            if ignorar:
                if q["op"] == "label":
                    # Encontrou uma label — é um ponto de entrada possível via salto → volta a aceitar código
                    ignorar = False
                    novos_quadruplos.append(q)
                else:
                    # Está num bloco inatingível (após um salto ou return) → ignora esta instrução
                    continue
            else:
                # Está num bloco executável — mantém a instrução
                novos_quadruplos.append(q)
                if q["op"] in {"goto", "return"}:
                    # Após um salto ou return, presume que o próximo código é inatingível até encontrar uma label
                    ignorar = True

        # Atualiza os quadruplos com os que ainda são atingíveis
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

    # Fase 1 — aplica várias otimizações independentes
    otimizador.constant_folding()                     # Substitui expressões com constantes
    otimizador.propagacao_copias()                    # Substitui variáveis copiadas por originais
    otimizador.eliminar_subexpressoes_comuns_CSE()    # Evita repetir expressões redundantes
    otimizador.mover_invariantes()                   # Move invariantes para fora de loops
    otimizador.constant_folding()                     # Aplica folding novamente após mover invariantes
    otimizador.eliminar_codigo_inatingivel()          # Remove código após saltos sem label

    

    # Fase 2 — aplica a eliminação de código morto em loop até estabilizar (ponto fixo)
    prev = None
    atual = otimizador.eliminar_codigo_morto()
    while prev != atual:
        prev = atual
        atual = otimizador.eliminar_codigo_morto()

    # Retorna o código otimizado final
    return atual