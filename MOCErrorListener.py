from antlr4.error.ErrorListener import ErrorListener

class MOCErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print(f"[Erro de Sintaxe] linha {line}, coluna {column}: {msg}")
        raise Exception("Erro de sintaxe detectado.")
