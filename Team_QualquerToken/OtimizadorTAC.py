# Elimina instruções TAC com resultados em temporários que nunca são usados
def otimizar_tac(lista_quadruplos):
    usados = set()

    # Recolhe os temporários que são usados como argumento em algum quadruplo
    for q in lista_quadruplos:
        for campo in ["arg1", "arg2"]:
            v = q.get(campo)
            if v and isinstance(v, str) and v.startswith("t"):
                usados.add(v)

    # Remove as instruções cujo resultado é um temporário não usado
    return [
        q for q in lista_quadruplos
        if not (isinstance(q.get("res"), str) and q["res"].startswith("t") and q["res"] not in usados)
    ]

# Elimina variáveis que foram atribuídas mas nunca usadas (versão mais segura)
def eliminar_variaveis_mortas(quadruplos):
    usados = set()

    # Recolhe todas as variáveis que aparecem como argumento em alguma operação
    for q in quadruplos:
        for campo in ["arg1", "arg2"]:
            v = q.get(campo)
            if v:
                usados.add(v)

    resultado = []
    for q in quadruplos:
        res = q.get("res")
        op  = q.get("op")

        # Instruções sem destino devem ser mantidas (por exemplo: goto, label, return)
        if res is None:
            resultado.append(q)

        # Se o resultado é um temporário, mantém a instrução
        elif isinstance(res, str) and res.startswith("t"):
            resultado.append(q)

        # Se a variável atribuída for usada em algum outro lugar, mantém
        elif res in usados:
            resultado.append(q)

        # Também mantém instruções com efeitos laterais mesmo que o resultado não seja usado
        elif op in {"param", "call", "return", "write", "writes", "writec", "writev", "label", "goto", "ifFalse", "ifgoto"}:
            resultado.append(q)

        # Caso contrário, a atribuição é inútil e é eliminada

    return resultado

# Aplica propagação de cópias no TAC (substitui variáveis redundantes)
def propagacao_copias(quadruplos):
    tabela_copias = {}

    # Etapa 1: constrói uma tabela com cópias diretas do tipo x = y
    for q in quadruplos:
        if q["op"] == "=" and q.get("arg2") is None:
            arg1 = q.get("arg1")
            res = q.get("res")
            if arg1 and res and arg1 != res:
                tabela_copias[res] = arg1

    # Etapa 2: resolve cadeias de cópias (ex: x = y, y = z → x = z)
    def resolver(v):
        while v in tabela_copias:
            v = tabela_copias[v]
        return v

    for k in list(tabela_copias):
        tabela_copias[k] = resolver(tabela_copias[k])

    resultado = []
    for q in quadruplos:
        novo = dict(q)  # Cópia do quadruplo atual

        # Substitui argumentos por versões finais
        if novo.get("arg1"):
            novo["arg1"] = resolver(novo["arg1"])
        if novo.get("arg2"):
            novo["arg2"] = resolver(novo["arg2"])

        # Se for uma cópia direta (x = y), substitui também o destino se for temporário
        if q["op"] == "=" and q.get("arg2") is None:
            destino = novo.get("res")
            origem = novo.get("arg1")
            if destino and origem and destino != origem:
                final = resolver(origem)
                if destino.startswith("t"):
                    # Substitui completamente a variável temporária redundante
                    novo["res"] = final
                else:
                    # Mantém nome visível do programa original (ex: total)
                    novo["res"] = destino
                    novo["arg1"] = final

        resultado.append(novo)

    return resultado

# Elimina instruções que definem variáveis temporárias que nunca são usadas posteriormente
def remover_definicoes_inuteis(quadruplos):
    usados = set()

    # Recolhe todas as variáveis usadas como argumentos em qualquer instrução
    for q in quadruplos:
        for campo in ("arg1", "arg2"):
            v = q.get(campo)
            if v:
                usados.add(v)

    resultado = []

    # Percorre os quadruplos de trás para a frente (análise backward)
    for q in reversed(quadruplos):
        res = q.get("res")

        # Ignora definições de temporários que não são usados
        if res and res.startswith("t") and res not in usados:
            continue

        # Mantém a instrução e regista o destino como usado
        resultado.insert(0, q)
        if res:
            usados.add(res)

    return resultado

# Realiza "constant folding": avalia expressões constantes em tempo de compilação
def constant_folding(quadruplos):
    resultado = []

    for q in quadruplos:
        op = q['op']
        a1 = q.get('arg1')
        a2 = q.get('arg2')
        res = q.get('res')

        # Verifica se é uma operação aritmética binária e ambos os argumentos são constantes inteiras
        if op in {"+", "-", "*", "/", "%"} and a1 and a2:
            if a1.isdigit() and a2.isdigit():
                v1 = int(a1)
                v2 = int(a2)
                try:
                    # Avalia a operação e gera um novo quadruplo como atribuição direta do valor calculado
                    if op == "+": val = str(v1 + v2)
                    elif op == "-": val = str(v1 - v2)
                    elif op == "*": val = str(v1 * v2)
                    elif op == "/" and v2 != 0: val = str(v1 // v2)
                    elif op == "%" and v2 != 0: val = str(v1 % v2)
                    else:
                        resultado.append(q)  # Não otimiza se houver divisão por zero ou casos inválidos
                        continue

                    # Substitui por instrução simples: res = val
                    resultado.append({"op": "=", "arg1": val, "arg2": None, "res": res})
                    continue  # Avança para o próximo quadruplo
                except:
                    pass  # Em caso de erro (ex: divisão por zero), mantém original

        # Se não for possível otimizar, mantém o quadruplo original
        resultado.append(q)

    return resultado

# Aplica todas as otimizações conhecidas até o código estabilizar
def otimizar_completo(quadruplos):
    """ Aplica todas as otimizações de forma iterativa até estabilizar """

    anterior = None
    atual = quadruplos

    while True:
        anterior = atual

        # Executa as otimizações em cadeia
        atual = propagacao_copias(atual)               # Propaga variáveis redundantes
        atual = constant_folding(atual)                # Avalia expressões com constantes
        atual = eliminar_variaveis_mortas(atual)       # Remove variáveis atribuídas mas não usadas
        atual = remover_definicoes_inuteis(atual)      # Elimina temporários nunca usados
        atual = otimizar_tac(atual)                    # Limpeza final de temporários não usados

        # Se não houve mudanças desde a última iteração, termina
        if atual == anterior:
            break

    return atual
