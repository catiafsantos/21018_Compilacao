#!/bin/bash

echo "🔄 A limpar ficheiros gerados pelo ANTLR..."

rm -f MOCLexer.py 
rm -f MOCLexer.tokens 
rm -f MOCLexer.interp
rm -f MOCParser.py 
rm -f MOCParser.tokens 
rm -f MOCParser.interp
rm -f MOCVisitor.py 
rm -f MOCVisitor.interp
rm -f MOCListener.py 
rm -f MOCListener.interp
rm -rf .antlr

echo "✅ Limpeza completa."

echo "⚙️  A gerar novos ficheiros a partir de MOC.g4..."

# Verifica se antlr4 está instalado
if ! command -v antlr4 &> /dev/null; then
    echo "❌ Erro: antlr4 não está instalado ou não está no PATH."
    exit 1
fi

antlr4 -Dlanguage=Python3 MOC.g4

if [ $? -eq 0 ]; then
    echo "✅ Ficheiros gerados com sucesso!"
else
    echo "❌ Ocorreu um erro ao gerar os ficheiros ANTLR."
fi