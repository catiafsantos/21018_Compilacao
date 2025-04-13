from antlr4.error.ErrorListener import ErrorListener

class MOCErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.erros = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        simbolo = getattr(offendingSymbol, "text", "(simbolo invalido)")

        if "token recognition error" in msg:
            mensagem = f"[Erro Lexico] Caractere invalido '{simbolo}' na linha {line}, coluna {column}."

        elif "missing" in msg:
            mensagem = f"[Erro Sintatico] Falta um elemento na expressao perto de '{simbolo}' (linha {line}, coluna {column})."

        elif "extraneous input" in msg:
            mensagem = f"[Erro Sintatico] O simbolo '{simbolo}' e inesperado nesta posicao (linha {line}, coluna {column})."

        elif "mismatched input" in msg:
            if simbolo == "float":
                mensagem = (f"[Erro Sintatico] O tipo '{simbolo}' nao e suportado nesta posicao "
                            f"(linha {line}, coluna {column}). Tipos validos: int, double, void.")
            else:
                mensagem = f"[Erro Sintatico] O simbolo '{simbolo}' nao corresponde ao esperado (linha {line}, coluna {column})."

        elif "no viable alternative" in msg:
            mensagem = f"[Erro Sintatico] Expressao mal formada perto de '{simbolo}' (linha {line}, coluna {column})."

        else:
            mensagem = f"[Erro Sintatico] Erro de sintaxe perto de '{simbolo}' (linha {line}, coluna {column}): {msg}"

        self.erros.append(mensagem)
        print(mensagem)