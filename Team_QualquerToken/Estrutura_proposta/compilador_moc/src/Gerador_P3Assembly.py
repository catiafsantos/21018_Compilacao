# Gerador_P3Assembly.py
# Geração de código Assembly P3 a partir de TAC otimizado

class GeradorP3Assembly:
    def __init__(self):
        # Lista para armazenar as declarações de dados (variáveis, arrays)
        self.data_declarations = []
        # Lista para armazenar as linhas de código assembly geradas
        self.assembly_lines = []
        # Dicionário para mapear nomes de variáveis para labels P3
        self.var_labels = {}
        # Contador para gerar labels únicos (usado em saltos e condições)
        self.label_counter = 0
        # Ponto de entrada do programa (label inicial)
        self.program_entry_point = "_start"

    @staticmethod
    def _format_line(col1: str, col2: str = "", col3: str = "", col4: str = "") -> str:
        """
        Formata quatro strings em uma linha única com colunas em posições fixas:
        """
        return f"{col1:<16}{col2:<8}{col3:<16}{col4}"

    @staticmethod
    def _sanitize_var(name):
        """
        Limpa e adapta o nome da variável para ser usado como label no Assembly P3.
        Substitui caracteres especiais e garante unicidade.
        """
        if name is None:
            return None
        if isinstance(name, (int, float)):
            return str(name)
        if not isinstance(name, str):
            return None
        name = (name.
                replace('$', 't_').
                replace('[', '_').
                replace(']', '').
                replace('"', '')
                )
        return name

    def _get_var_label(self, name):
        """
        Devolve o label P3 associado a uma variável.
        Se ainda não existir, cria a declaração no segmento de dados.
        """
        name = self._sanitize_var(name)
        if name is None:
            return None
        if name not in self.var_labels:
            label = f"VAR_{name.upper()}"
            self.var_labels[name] = label
            self.data_declarations.append(self._format_line(label, "WORD", "0", f"; {name}"))
        return self.var_labels[name]

    def _declare_array(self, name, size):
        """
        Declara um array no segmento de dados.
        Remove declarações anteriores do mesmo nome para evitar duplicação.
        """
        name = self._sanitize_var(name)
        label = f"VAR_{name.upper()}"
        decl = f"{label} TAB {size} ; Array {name}"  # sem dois pontos!
        # Remove possíveis declarações anteriores da mesma variável
        self.data_declarations = [d for d in self.data_declarations if not d.startswith(f"{label} ")]
        self.data_declarations.append(decl)
        self.var_labels[name] = label
        return label

    def _gen_label(self, base="L"):
        """
        Gera um label único para saltos condicionais ou blocos de código.
        """
        self.label_counter += 1
        return f"{base}{self.label_counter}"

    def translate_tac_instruction(self, instr):
        """
        Traduz uma instrução TAC (dicionário) para Assembly P3 e adiciona as linhas geradas.
        """
        op = instr.get('op', '').upper()
        arg1 = instr.get('arg1')
        arg2 = instr.get('arg2')
        res = instr.get('res')

        arg1_label = self._get_var_label(arg1)
        arg2_label = self._get_var_label(arg2)
        res_label = self._get_var_label(res)

        # Operações aritméticas e atribuição
        if op in ('ASSIGN_CONST', '(DOUBLE)', '='):
            # res = arg1
            self.assembly_lines.append(self._format_line("","MOV", f"R1, {arg1_label}"))
            self.assembly_lines.append(self._format_line("","MOV", f"{res_label}, R1"))
        elif op in ('ADD', '+'):
            # res = arg1 + arg2
            self.assembly_lines.append(self._format_line("","MOV", f"R1, {arg1_label}"))
            self.assembly_lines.append(self._format_line("","MOV", f"R2, {arg2_label}"))
            self.assembly_lines.append(self._format_line("","ADD", "R1, R2"))
            self.assembly_lines.append(self._format_line("","MOV", f"{res_label}, R1"))
        elif op in ('SUB', '-'):
            # res = arg1 - arg2
            self.assembly_lines.append(self._format_line("","MOV", f"R1, {arg1_label}"))
            self.assembly_lines.append(self._format_line("","MOV", f"R2, {arg2_label}"))
            self.assembly_lines.append(self._format_line("","SUB", "R1, R2"))
            self.assembly_lines.append(self._format_line("","MOV", f"{res_label}, R1"))
        elif op in ('MUL', '*'):
            # res = arg1 * arg2
            self.assembly_lines.append(self._format_line("","MOV", f"R1, {arg1_label}"))
            self.assembly_lines.append(self._format_line("","MOV", f"R2, {arg2_label}"))
            self.assembly_lines.append(self._format_line("","MUL", "R1, R2"))
            self.assembly_lines.append(self._format_line("","MOV", f"{res_label}, R1"))
        elif op in ('DIV', '/'):
            # res = arg1 / arg2
            self.assembly_lines.append(self._format_line("","MOV", f"R1, {arg1_label}"))
            self.assembly_lines.append(self._format_line("","MOV", f"R2, {arg2_label}"))
            self.assembly_lines.append(self._format_line("","DIV", "R1, R2"))
            self.assembly_lines.append(self._format_line("","MOV", f"{res_label}, R1"))
        elif op == 'NEG':
            # res = -arg1
            self.assembly_lines.append(self._format_line("","MOV", f"R1, {arg1_label}"))
            self.assembly_lines.append(self._format_line("","NEG", "R1"))
            self.assembly_lines.append(self._format_line("","MOV", f"{res_label}, R1"))

        # Operações lógicas
        elif op in ('AND',):
            # res = arg1 AND arg2
            self.assembly_lines.append(self._format_line("","MOV", f"R1, {arg1_label}"))
            self.assembly_lines.append(self._format_line("","MOV", f"R2, {arg2_label}"))
            self.assembly_lines.append(self._format_line("","AND", "R1, R2"))
            self.assembly_lines.append(self._format_line("","MOV", f"{res_label}, R1"))
        elif op in ('OR',):
            # res = arg1 OR arg2
            self.assembly_lines.append(self._format_line("","MOV", f"R1, {arg1_label}"))
            self.assembly_lines.append(self._format_line("","MOV", f"R2, {arg2_label}"))
            self.assembly_lines.append(self._format_line("","OR",  "R1, R2"))
            self.assembly_lines.append(self._format_line("","MOV", f"{res_label}, R1"))
        elif op in ('XOR',):
            # res = arg1 XOR arg2
            self.assembly_lines.append(self._format_line("","MOV", f"R1, {arg1_label}"))
            self.assembly_lines.append(self._format_line("","MOV", f"R2, {arg2_label}"))
            self.assembly_lines.append(self._format_line("","XOR", "R1, R2"))
            self.assembly_lines.append(self._format_line("","MOV", f"{res_label}, R1"))

        # Comparações (CMP + saltos)
        elif op in ('=', '<>', '<', '<=', '>', '>='):
            # res = (arg1 op arg2) ? 1 : 0
            self.assembly_lines.append(self._format_line("","MOV", f"R1, {arg1_label}"))
            self.assembly_lines.append(self._format_line("","MOV", f"R2, {arg2_label}"))
            self.assembly_lines.append(self._format_line("","CMP", "R1, R2"))
            true_label = self._gen_label("TRUE")
            end_label = self._gen_label("END")
            # Mapeamento do operador TAC para o salto P3 correspondente
            jump = {
                '=' : 'JMP.Z',   # igual
                '<>': 'JMP.NZ',  # diferente
                '<' : 'JMP.N',   # menor
                '<=': 'JMP.NP',  # menor ou igual
                '>' : 'JMP.P',   # maior
                '>=': 'JMP.NN'   # maior ou igual
            }[op]
            self.assembly_lines.append(self._format_line("",jump, true_label))
            self.assembly_lines.append(self._format_line("","MOV", res_label, "0"))
            self.assembly_lines.append(self._format_line("","JMP", end_label))
            self.assembly_lines.append(self._format_line(true_label+":", "NOP"))
            self.assembly_lines.append(self._format_line("","MOV", res_label, "1"))
            self.assembly_lines.append(self._format_line(end_label+":", "NOP"))

        # Saltos e labels
        elif op == 'LABEL':
            # Marca um label no código
            self.assembly_lines.append(self._format_line(res+":", "NOP"))
        elif op == 'GOTO':
            # Salto incondicional
            self.assembly_lines.append(self._format_line("", "JMP", res))
        elif op == 'IFGOTO':
            # Salto se arg1 != 0
            self.assembly_lines.append(self._format_line("", "MOV", f"R1, {arg1_label}"))
            self.assembly_lines.append(self._format_line("", "CMP", "R1", "0"))
            self.assembly_lines.append(self._format_line("", "JMP.NZ", res))

        # Arrays
        elif op == 'ALLOC':
            # Declaração de array (já tratada na primeira passagem)
            self._declare_array(arg1, arg2)
        elif op == 'LOAD_ARRAY':
            # res = arg1[arg2]
            arr = self._get_var_label(arg1)
            idx = self._get_var_label(arg2)
            self.assembly_lines.append(self._format_line("", "MOV", "R1", idx))
            self.assembly_lines.append(self._format_line("", "MOV", "R2", arr+"[R1]"))
            self.assembly_lines.append(self._format_line("", "MOV", res_label, "R2"))
        elif op == 'STORE_ARRAY':
            # arg1[arg2] = res
            arr = self._get_var_label(arg1)
            idx = self._get_var_label(arg2)
            val = self._get_var_label(res)
            self.assembly_lines.append(self._format_line("", "MOV", "R1", idx))
            self.assembly_lines.append(self._format_line("", "MOV", "R2", val))
            self.assembly_lines.append(self._format_line("", "MOV", arr+"[R1]", "R2"))

        # Pilha (stack)
        elif op == 'PUSH':
            # Empilha valor de arg1
            self.assembly_lines.append(self._format_line("", "PUSH", arg1_label))
        elif op == 'POP':
            # Retira valor do topo da pilha para res
            self.assembly_lines.append(self._format_line("", "POP", res_label))

        # Funções
        elif op == 'CALL':
            # Chamada de função (label)
            self.assembly_lines.append(self._format_line("", "CALL", res_label))
        elif op == 'RETURN':
            # Retorno de função
            self.assembly_lines.append(self._format_line("", "RET"))

        # Entrada/Saída (exemplo: print)
        elif op == 'WRITE':
            # Rui Menino // REVER. Está a imprimir o carater correspondente ao valor ascii que estiver na variável
            # Escreve valor de arg1 na janela de texto (endereço FFFEh)
            self.assembly_lines.append(self._format_line(f"; {op.lower()}", "-"*25))
            self.assembly_lines.append(self._format_line("", "MOV", f"R1, M[{arg1_label}]", "; Lê o carater apontado por R1"))
            self.assembly_lines.append(self._format_line("", "MOV", "M[FFFEh], R1", "; Escreve o carater no endereço de saída"))
        elif op == 'WRITES':
            # Rui Menino // OK -- REVER que a variável tem de ser do tipo STR e ter aspas
            self.assembly_lines.append(self._format_line(f"; {op.lower()}", "-"*25))
            self.assembly_lines.append(self._format_line("", "MOV", f"R1, {arg1_label}", "; R1 aponta para o início da string"))
            self.assembly_lines.append(self._format_line("", "CALL", f"{op.upper()}", "; Chama a rotina"))
        elif op == 'READ':
            # Lê valor da janela de texto (endereço FFFFh) para res
            self.assembly_lines.append(self._format_line("", "MOV", "R1", "M[FFFFh]"))
            self.assembly_lines.append(self._format_line("", "MOV", f"{res_label}, R1"))
        elif op == 'HALT':
            # TErmina a execução do programa
            self.assembly_lines.append(self._format_line("", "BR", "Fim"))
        else:
            # Caso não exista tradução, insere comentário de aviso
            self.assembly_lines.append(f";; AVISO: Operação TAC '{op}' não traduzida para P3.")

    def generate_from_tac_list(self, tac_list):
        """
        Gera o código Assembly P3 completo a partir de uma lista de instruções TAC.
        Retorna o código como uma string pronta a ser escrita num ficheiro .as.
        """
        self.data_declarations = []
        self.assembly_lines = []
        self.var_labels = {}
        self.label_counter = 0

        # Primeira passagem: declara arrays variáveis e constantes
        # for instr in tac_list:
        #     if instr.get('op', '').upper() == 'ALLOC':
        #         self._declare_array(instr.get('arg1'), instr.get('arg2'))
        #     else:
        #         self._get_var_label(instr.get('res'))
        #         self._get_var_label(instr.get('arg1'))
        #         self._get_var_label(instr.get('arg2'))
        for instr in tac_list:
            if instr.get('op', '').upper() == 'ALLOC':
                self._declare_array(instr.get('arg1'), instr.get('arg2'))
            else:
                # Trata o resultado (res) como variável normal
                self._get_var_label(instr.get('res'))

                # Trata arg1: se for constante numérica ou string literal, define como constante
                arg1 = instr.get('arg1')
                if arg1 is not None:
                    if (
                            isinstance(arg1, (int, float)) or
                            (isinstance(arg1, str) and arg1.isdigit()) or
                            (isinstance(arg1, str) and (arg1.startswith('"') and arg1.endswith('"')))
                    ):
                        # Aqui podes adicionar à tua estrutura de constantes, por exemplo:
                        #self._constantes[arg1] = arg1
                        self._get_var_label(arg1)
                    else:
                        self._get_var_label(arg1)

                # Trata arg2 como variável normal
                self._get_var_label(instr.get('arg2'))

        # Segunda passagem: traduz instruções TAC para assembly
        for instr in tac_list:
            self.translate_tac_instruction(instr)

        # Monta o código final
        output = []
        if self.data_declarations:
            output.append(self._format_line(";" + "=" * 14, "Região de Dados (inicia no endereço 8000h)"))
            output.append(self._format_line("", "ORIG", "8000h"))
            output.append("")
            output.extend(sorted(self.data_declarations))
            output.append("")
            output.append(self._format_line("SP_ADDRESS", "EQU", "FDFFh"))
            output.append("")
        output.append(self._format_line(";"+"="*14, "Região de Código (inicia no endereço 0000h)"))
        output.append(self._format_line("", "ORIG", "0000h"))

        output.append(self._format_line("", "JMP", "_start","; jump to main"))
        output.append("")
        output.append(self._format_line(";"+"-"*14, "Rotinas"))
        output.append("")
        output.append(self._format_line("WRITES:", "NOP", "","; escreve uma string na consola"))
        output.append(self._format_line("MostraChar:", "MOV", "R2, M[R1]","; Lê o carater apontado por R1"))
        output.append(self._format_line("", "CMP", "R2, 0","; Compara com o terminador"))
        output.append(self._format_line("", "JMP.Z", "FimChar","; Se for zero, salta para o fim"))
        output.append(self._format_line("", "MOV", "M[FFFEh], R2","; Escreve o carater no endereço de saída"))
        output.append(self._format_line("", "INC", "R1","; Avança para o próximo carater"))
        output.append(self._format_line("", "BR", "MostraChar","; Repete o ciclo"))
        output.append(self._format_line("FimChar:", "RET",  "",""))
        output.append("")
        output.append(self._format_line(";"+"-"*14, "Programa Principal "))

        output.append(self._format_line(f"{self.program_entry_point}:", "NOP"))
        output.append(self._format_line("", "MOV", "R7, SP_ADDRESS"))
        output.append(self._format_line("", "MOV", "SP, R7", "; Define o Stack Pointer"))
        output.append("")
        output.extend(self.assembly_lines)
        output.append("")
        output.append(self._format_line("Fim:", "BR", "Fim"))
        output.append("")
        return "\n".join(output)
