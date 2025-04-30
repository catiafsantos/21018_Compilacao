from antlr4.error.ErrorListener import ErrorListener

# Os erros estao ordenados pela ordem que ocorrem cronologicamente, sem agrupamentos logicos (exemplo leexicos e depois sintaticos)
class MOCErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.erros = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        simbolo = getattr(offendingSymbol, "text", "(simbolo invalido)")

        if "token recognition error" in msg:
            char_errado = msg.split("at:")[-1].strip()
            mensagem = f"[Erro Lexico] Token invalido {char_errado} na linha {line}, coluna {column}."

        elif "extraneous input" in msg:
            mensagem = f"[Erro Sintatico] O simbolo '{simbolo}' e inesperado nesta posicao (linha {line}, coluna {column})."

        elif "no viable alternative" in msg:
            expressao = msg.split("input")[-1].strip().strip("'")
            mensagem = f"[Erro Sintatico] Expressão mal formada: {expressao} (linha {line}, coluna {column})."
        
        elif "missing" in msg:
            esperado = msg.split("missing")[-1].split("at")[0].strip().strip("'")
            mensagem = f"[Erro Sintatico] Falta o elemento '{esperado}' perto de '{simbolo}' (linha {line}, coluna {column})."

        elif "mismatched input" in msg and "expecting" in msg:
            esperados_legiveis = formatar_esperados(recognizer, e)
            mensagem = f"[Erro Sintatico] O símbolo '{simbolo}' não era esperado. Espera-se: {esperados_legiveis} (linha {line}, coluna {column})."

        else:
            mensagem = f"[Erro Sintatico] Erro de sintaxe perto de '{simbolo}' (linha {line}, coluna {column}): {msg}"

        self.erros.append(mensagem)
        print(mensagem)

# Função auxiliar para transformar os tokens esperados num formato legível
def formatar_esperados(recognizer, e):
    if not e or not hasattr(e, 'getExpectedTokens'):
        return "desconhecido"

    expected_token_indexes = list(e.getExpectedTokens())
    expected = []

    for i in expected_token_indexes:
        nome_literal = recognizer.literalNames[i] if i < len(recognizer.literalNames) else None
        nome_simbolico = recognizer.symbolicNames[i] if i < len(recognizer.symbolicNames) else None

        if nome_literal is not None:
            expected.append(nome_literal)
        elif nome_simbolico is not None:
            expected.append(nome_simbolico)
        else:
            expected.append(str(i))  # fallback caso não exista nenhum nome

    return ', '.join(expected)