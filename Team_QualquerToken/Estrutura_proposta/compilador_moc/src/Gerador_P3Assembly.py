# Gerador_P3Assembly.py
# Geração de código Assembly P3 a partir de TAC otimizado
import re

class GeradorP3Assembly:
    def __init__(self, quadruplos):
        self.quadruplos = quadruplos
        # Lista para armazenar as linhas de código assembly geradas
        self.assembly_code = [] 
        # Lista para armazenar as declarações de dados (variáveis, arrays)
        self.data_section = []
        # Lista para armazenar as linhas de código assembly geradas das funcoes
        self.assemblyfunction_code = []
        self.declared_functions = set() #vamos armazenar que funcoes já foram declaradas

        # Dicionário para mapear nomes de variáveis para labels P3
        self.var_labels = {}

        # Contador para gerar labels únicos (usado em saltos e condições)
        self.label_generator_count = 0
        self.string_literal_count = 0
        self.string_literal_map = {}  # Maps string content to a label
        self.declared_vars = set()  # To keep track of vars/temps for data section

        # Ponto de entrada do programa (label inicial)
        self.program_entry_point = "_start"
        # Pre-scan for all variables, temporaries, and array allocations
        self._pre_scan_quadruplos()

    def _new_internal_label(self, prefix="L_asm_"):
        self.label_generator_count += 1
        return f"{prefix}{self.label_generator_count}"

    def _add_string_literal(self, string_content):
        if string_content in self.string_literal_map:
            return self.string_literal_map[string_content]

        self.string_literal_count += 1
        label = f"STR_LIT_{self.string_literal_count}"
        self.string_literal_map[string_content] = label

        # Create P3 STR pseudo-instruction parts
        # STR '<texto>' | <const>[,'<texto>' |<const>] [cite: 125]
        # Each char is a word in P3 STR.
        # Example: STR_LIT_1: STR 'H','e','l','l','o',0
        char_parts = [f"'{char}'" for char in string_content]
        char_parts.append("0")  # Null terminator
        #elf.data_section.append(f"{label}: STR {','.join(char_parts)}")

        self.data_section.append(self._format_line(f"{label}", "STR", f"{','.join(char_parts)}",f"; '{string_content}'"))


        return label

    def _is_tac_temp(self, operand_str):
        return operand_str is not None and isinstance(operand_str, str) and operand_str.startswith('t')

    def _is_tac_label(self, operand_str):
        return operand_str is not None and isinstance(operand_str, str) and operand_str.startswith('L')

    def _is_immediate_val(self, operand_str):
        if operand_str is None or not isinstance(operand_str, str):
            return False
        # Matches integers, hex (0xFFFFh), binary (101b), octal (77o)
        if re.match(r"^-?[0-9]+$", operand_str): return True
        if re.match(r"^-?[0-9a-fA-F]+h$", operand_str): return True
        if re.match(r"^-?[01]+b$", operand_str): return True
        if re.match(r"^-?[0-7]+o$", operand_str): return True
        return False

    def _get_p3_operand_syntax(self, tac_operand, context="load"):
        """
        Converte uma string de operando TAC em sintaxe P3 para utilização numa instrução.
        context="load": para operandos de origem (ex.: MOV R1, <aqui>)
        context="store": para operandos de destino (ex.: MOV <aqui>, R1)
        context="address": quando o próprio operando é um rótulo de endereço para JMP/CALL
        """
        if tac_operand is None:
            return None

        s_tac_operand = str(tac_operand)

        if self._is_immediate_val(s_tac_operand):
            return s_tac_operand  # P3 immediates are just numbers/chars
        elif s_tac_operand.startswith("'") and s_tac_operand.endswith("'") and len(s_tac_operand) == 3:  # char literal
            return s_tac_operand  # e.g. 'A'
        elif self._is_tac_temp(s_tac_operand) or s_tac_operand in self.declared_vars:
            # These are variables/temporaries stored in memory
            if context == "store" or context == "load":
                label= self._get_var_label(s_tac_operand)
                return f"M[{label}]"  # Access memory location
            return s_tac_operand  # Return name for address context if needed (e.g. for LEA-like ops, not directly in P3)
        elif self._is_tac_label(s_tac_operand) or s_tac_operand in ["main", "end_main"] or s_tac_operand.startswith(
                "end_"):  # Labels for jumps/calls
            return s_tac_operand
        else:  # Default assumption for unknown symbols is a variable name / memory location
            if context == "store" or context == "load":
                return f"M[{s_tac_operand}]"
            return s_tac_operand

    def _pre_scan_quadruplos(self):
        """
        Scans quadruples to identify all variables, temporaries, and array allocations
        to declare them in the data section.
        """
        # Adicione endereços de E/S comuns como EQU para facilitar a leitura, caso sejam utilizados com frequência
        # self.data_section.append("TEXT_OUT_PORT EQU FFFEh") [pagina: 4 do manual]
        # self.data_section.append("TEXT_STAT_PORT EQU FFFDh")
        # self.data_section.append("TEXT_IN_PORT EQU FFFFh")


        for quad in self.quadruplos:
            operands = [quad['arg1'], quad['arg2'], quad['res']]

            if quad['op'] == 'alloc':  # alloc var, size_elements
                var_name = quad['arg1']
                num_elements_tac = int(quad['arg2'])
                # TAC element size is 4 bytes, P3 words are 2 bytes.
                num_p3_words = num_elements_tac * 2
                self.data_section.append(self._format_line(
                    f"{var_name}", f"TAB", f"{num_p3_words}", f" ; alloc {num_elements_tac} TAC elements ({num_p3_words} P3 words)"))
                self.declared_vars.add(var_name)


            if quad['op'] == 'writes':  # writes "string" esta intrução escreve uma string literal
                str_content = quad['arg1'].strip('"')
                self._add_string_literal(str_content)  # Declares in data_section


            if quad['op'] == 'label':
                # é uma label de uma funçáo
                # se já existir main não coloca
                for operand in operands:
                    if operand and isinstance(operand, str):
                        self.declared_functions.add(operand)


            for operand in operands:
                if operand and isinstance(operand, str):
                    if self._is_tac_temp(operand) or (not self._is_immediate_val(operand) and not self._is_tac_label(
                            operand) and not operand.startswith("'") and not operand.endswith(":")):
                        self.declared_vars.add(operand)

        # Adicionar declarações WORD para todas as variáveis/temporárias identificadas ainda não declaradas por alloc
        # Certifique-se de que isto é feito após declarações específicas, como STR ou TAB, de alloc.
        # Este será anexado posteriormente, após literais de string específicos.
        # Aqui, apenas preenchemos self.declared_vars por enquanto.

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

    def _get_var_label1(self, name):
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
            self.data_section.append(self._format_line(label, "WORD", name, f"; {name}"))
        return self.var_labels[name]

    def _get_var_label(self, name):
        """
        Devolve uma etiqueta P3 curta e única associada a uma variável.
        Se a etiqueta para esta variável ainda não existir, cria a sua
        declaração no segmento de dados.
        """
        # A sua função de sanitização continua aqui
        name = self._sanitize_var(name)
        if name is None:
            return None

        # Verifica se já foi criada uma etiqueta para este nome de variável

        if name not in self.var_labels:
            # Gera uma nova etiqueta curta e única usando o contador
            self.label_generator_count += 1
            label = f"VAR_{self.label_generator_count}"

            # Associa o nome original da variável à nova etiqueta gerada
            self.var_labels[name] = label

            # Adiciona a declaração à secção de dados.
            # Nota: Inicializamos com '0' e mantemos o nome original no comentário.
            #linha_declaracao = f"{label}: WORD 0 ; Variável original: {name}"
            #self.data_section.append(linha_declaracao)
            try:
                # Tenta converter 'name' para um inteiro.
                valor_inteiro = int(name)

                # Se funcionar, é um número. Pode formatá-lo como quiser.
                # Aqui, estamos a assumir que um inteiro de 32 bits ocupa 2 palavras.
                #self.data_section.append(
                #    self._format_line(label, "WORD", str(valor_inteiro & 0xFFFF), f"; literal inteiro '{name}' (low)"))
                #self.data_section.append(
                #    self._format_line("", "WORD", str((valor_inteiro >> 16) & 0xFFFF), f"; (high)"))
                self.data_section.append(self._format_line(label, "WORD", name, f"; {name}"))
            except (ValueError, TypeError):
                # Se a conversão falhar, não é um número. Trata-se de um nome de variável.
                # Vamos assumir que uma variável não inicializada começa em 0.
                self.data_section.append(self._format_line(label, "WORD", "0", f"; variável '{name}'"))
            #self.data_section.append(self._format_line(label, "WORD", name, f"; {name}"))

        # Devolve a etiqueta curta e única associada ao nome
        return self.var_labels[name]

    def _declare_array(self, name, size):
        """
        Declara um array no segmento de dados.
        Remove declarações anteriores do mesmo nome para evitar duplicação.
        """
        name = self._sanitize_var(name)
        label = f"VAR_{name.upper()}"
        decl = self._format_line(f"{label}", "TAB", size, f"; Array {name}")  # sem dois pontos!
        # Remove possíveis declarações anteriores da mesma variável
        self.data_section = [d for d in self.data_section if not d.startswith(f"{label} ")]
        self.data_section.append(decl)
        self.var_labels[name] = label
        return label

    def _gen_label(self, base="L"):
        """
        Gera um label único para saltos condicionais ou blocos de código.
        """
        self.label_generator_count += 1
        return f"{base}{self.label_generator_count}"

    def translate_tac_instruction(self, instr, quad_num):
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

        # Atribuição
        if op in ('ASSIGN_CONST', '(DOUBLE)', '='):
            # res = arg1
            # Load arg1 -> R1
            if arg1_label is None:
                p3_arg1_syntax = self._get_p3_operand_syntax(arg1, 'load')
                if not str(arg1).startswith("M[") and not self._is_immediate_val(str(arg1)) and not (
                        str(arg1).startswith("'") and str(arg1).endswith("'")):
                    # if arg1 is a variable name, needs M[]
                    p3_arg1_syntax = f"M[{arg1}]" if not self._is_immediate_val(str(arg1)) else str(arg1)
            else:
                p3_arg1_syntax = self._get_p3_operand_syntax(arg1_label, 'load')

            self.assembly_code.append(self._format_line("","MOV", f"R1, {p3_arg1_syntax}"))
            self.assembly_code.append(self._format_line("",f"MOV",f"{self._get_p3_operand_syntax(res, 'store')}, R1"))

        # Operações aritméticas e atribuição
        # res = arg1 op arg2. Um operando P3 deve ser um registo
        # Padrão geral: MOV R1, arg1; MOV R2, arg2; P3_OP R1, R2; MOV res, R1
        elif op in ['+', '-', '*', '/', '%']:
            # Load arg1 -> R1
            self.assembly_code.append(self._format_line("",f"MOV",f"R1, {self._get_p3_operand_syntax(arg1, 'load')}"))
            # Load arg2 ->  R2
            self.assembly_code.append(self._format_line("",f"MOV",f"R2, {self._get_p3_operand_syntax(arg2, 'load')}"))
            p3_res_syntax = self._get_p3_operand_syntax(res, 'store')
            if op in '+':
                # res = arg1 + arg2
                #self.assembly_code.append(self._format_line("","MOV", f"R1, {arg1_label}"))
                #self.assembly_code.append(self._format_line("","MOV", f"R2, {arg2_label}"))
                self.assembly_code.append(self._format_line("","ADD", "R1, R2","; ZCNO flags affected"))
                self.assembly_code.append(self._format_line("",f"MOV",f"{p3_res_syntax}, R1"))
            elif op in '-':
                # res = arg1 - arg2
                # self.assembly_code.append(self._format_line("","MOV", f"R1, {arg1_label}"))
                # self.assembly_code.append(self._format_line("","MOV", f"R2, {arg2_label}"))
                # self.assembly_code.append(self._format_line("","SUB", "R1, R2"))
                # self.assembly_code.append(self._format_line("","MOV", f"{res_label}, R1"))
                self.assembly_code.append(self._format_line("", "SUB", "R1, R2", "; ZCNO flags affected"))
                self.assembly_code.append(self._format_line("", f"MOV",f"{p3_res_syntax}, R1"))
            elif op in '*': # MUL op1, op2 -> op1 has MSW, op2 has LSW.
                # res = arg1 * arg2
                # self.assembly_code.append(self._format_line("","MOV", f"R1, {arg1_label}"))
                # self.assembly_code.append(self._format_line("","MOV", f"R2, {arg2_label}"))
                # self.assembly_code.append(self._format_line("","MUL", "R1, R2"))
                # self.assembly_code.append(self._format_line("","MOV", f"{res_label}, R1"))
                self.assembly_code.append(self._format_line("", "MUL", "R1, R2", "; R1=MSW, R2=LSW. Unsigned. Z based on 32bit, CNO=0"))
                self.assembly_code.append(self._format_line("", "MOV",f"{p3_res_syntax}, R1","; Store LSW into result"))
            elif op in '/':  # DIV op1, op2 -> op1 tem Quociente, op2 tem Resto.
                # res = arg1 / arg2
                # self.assembly_code.append(self._format_line("","MOV", f"R1, {arg1_label}"))
                # self.assembly_code.append(self._format_line("","MOV", f"R2, {arg2_label}"))
                # self.assembly_code.append(self._format_line("","DIV", "R1, R2"))
                # self.assembly_code.append(self._format_line("","MOV", f"{res_label}, R1"))
                self.assembly_code.append(self._format_line("", "DIV", "R1, R2", "; R1=Quociente, R2=Resto. Unsigned. O on div by zero, CN=0."))
                self.assembly_code.append(self._format_line("", "MOV",f"{p3_res_syntax}, R1","; Guarda Quociente no resultado"))
            elif op in '%':  # DIV op1, op2 -> op1 tem Quociente, op2 tem Resto.
                # res = arg1 / arg2
                # self.assembly_code.append(self._format_line("","MOV", f"R1, {arg1_label}"))
                # self.assembly_code.append(self._format_line("","MOV", f"R2, {arg2_label}"))
                # self.assembly_code.append(self._format_line("","DIV", "R1, R2"))
                # self.assembly_code.append(self._format_line("","MOV", f"{res_label}, R1"))
                self.assembly_code.append(
                    self._format_line("", "DIV", "R1, R2", "; R1=Quociente, R2=Resto. Unsigned. O on div by zero, CN=0."))
                self.assembly_code.append(
                    self._format_line("", "MOV",f"{p3_res_syntax}, R2", "; Guarda Resto no resultado"))
            # TESTAR REVER NO P3
            elif op == 'NEG':
                # res = -arg1
                # self.assembly_code.append(self._format_line("","MOV", f"R1, {arg1_label}"))
                self.assembly_code.append(self._format_line("","NEG", "R1"))
                self.assembly_code.append(self._format_line("","MOV",f"{p3_res_syntax},  R1"))

        # Operações lógicas
        elif op in ('AND',):
            # res = arg1 AND arg2
            self.assembly_code.append(self._format_line("","MOV", f"R1, {arg1_label}"))
            self.assembly_code.append(self._format_line("","MOV", f"R2, {arg2_label}"))
            self.assembly_code.append(self._format_line("","AND", "R1, R2"))
            self.assembly_code.append(self._format_line("","MOV", f"{res_label}, R1"))
        elif op in ('OR',):
            # res = arg1 OR arg2
            self.assembly_code.append(self._format_line("","MOV", f"R1, {arg1_label}"))
            self.assembly_code.append(self._format_line("","MOV", f"R2, {arg2_label}"))
            self.assembly_code.append(self._format_line("","OR",  "R1, R2"))
            self.assembly_code.append(self._format_line("","MOV", f"{res_label}, R1"))
        elif op in ('XOR',):
            # res = arg1 XOR arg2
            self.assembly_code.append(self._format_line("","MOV", f"R1, {arg1_label}"))
            self.assembly_code.append(self._format_line("","MOV", f"R2, {arg2_label}"))
            self.assembly_code.append(self._format_line("","XOR", "R1, R2"))
            self.assembly_code.append(self._format_line("","MOV", f"{res_label}, R1"))

        # Comparações (CMP + saltos)
        elif op in ('==', '!=', '<', '<=', '>', '>='):
            # res = (arg1 op arg2) ? 1 : 0
            #self.assembly_code.append(self._format_line("","MOV", f"R1, {arg1_label}"))
            #self.assembly_code.append(self._format_line("","MOV", f"R2, {arg2_label}"))
            #self.assembly_code.append(self._format_line("","CMP", "R1, R2"))

            self.assembly_code.append(self._format_line("","MOV",f"R1, {self._get_p3_operand_syntax(arg1, 'load')}"))
            self.assembly_code.append(self._format_line("","MOV",f"R2, {self._get_p3_operand_syntax(arg2, 'load')}"))
            self.assembly_code.append(self._format_line("","CMP","R1, R2","; ZCNO flags affected"))

            #true_label = self._gen_label("TRUE")
            #end_label = self._gen_label("END")

            p3_res_syntax = self._get_p3_operand_syntax(res, 'store')
            true_label = self._new_internal_label("REL_TRUE_")
            end_label = self._new_internal_label("REL_END_")

            # Mapeamento do operador TAC para o salto P3 correspondente
            jump = {
                '==': 'JMP.Z',   # igual
                '!=': 'JMP.NZ',  # diferente
                '<' : 'JMP.N',   # menor
                '<=': 'JMP.NP',  # menor ou igual
                '>' : 'JMP.P',   # maior
                '>=': 'JMP.NN'   # maior ou igual
            }[op]
            # TESTAR DEVE ESTAR OK PARA = E <>
            self.assembly_code.append(self._format_line("",jump, true_label))

            # Other relational ops would require more complex flag checking or specific P3 idioms
            # .... (f"; Relational op '{op}' requires more complex P3 flag logic or specific subroutines")

            self.assembly_code.append(self._format_line("","MOV",f"{p3_res_syntax}, R0")) # False path
            self.assembly_code.append(self._format_line("","JMP",f"{end_label}"))
            self.assembly_code.append(self._format_line(f"{true_label}:", "NOP"))
            self.assembly_code.append(self._format_line("","MOV",f"{p3_res_syntax}, 1"))  # True path
            self.assembly_code.append(self._format_line(f"{end_label}:", "NOP"))

        # Saltos e labels
        elif op == 'LABEL':
            # Marca um label no código
            self.assembly_code.append(self._format_line(res+":", "NOP"))
        elif op == 'GOTO':
            # Salto incondicional
            self.assembly_code.append(self._format_line("", "JMP", self._get_p3_operand_syntax(res, 'address')))
        elif op == 'IFGOTO': # if cond_var goto label
            # Salto se arg1 != 0
            # MOV R1, M[cond_var]
            # CMP R1, #0
            # JMP.NZ label ; Jump if Not Zero (condition is true)
            # self.assembly_code.append(self._format_line("", "MOV", f"R1, {arg1_label}"))
            self.assembly_code.append(self._format_line("", "MOV", f"R1, {self._get_p3_operand_syntax(arg1, 'load')}"))
            self.assembly_code.append(self._format_line("", "CMP", "R1", "0"))
            self.assembly_code.append(self._format_line("", f"JMP.NZ",f"{self._get_p3_operand_syntax(res, 'address')}"))

        # Arrays TESTAR
        elif op == 'ALLOC':
            # Declaração de array (já tratada na primeira passagem)
            self._declare_array(arg1, arg2)
        elif op == 'LOAD_ARRAY':
            # res = arg1[arg2]
            arr = self._get_var_label(arg1)
            idx = self._get_var_label(arg2)
            self.assembly_code.append(self._format_line("", "MOV", "R1", idx))
            self.assembly_code.append(self._format_line("", "MOV", "R2", arr+"[R1]"))
            self.assembly_code.append(self._format_line("", "MOV",res_label, "R2"))
        elif op == 'STORE_ARRAY':
            # arg1[arg2] = res
            arr = self._get_var_label(arg1)
            idx = self._get_var_label(arg2)
            val = self._get_var_label(res)
            self.assembly_code.append(self._format_line("", "MOV", "R1", idx))
            self.assembly_code.append(self._format_line("", "MOV", "R2", val))
            self.assembly_code.append(self._format_line("", "MOV", arr+"[R1]", "R2"))

            # --- Array Operations ---
            # TAC: t_offset = index * 4 (bytes)
            # P3: word_offset = byte_offset / 2
        elif op == '[]':  # res = array_name[byte_offset_var]
            # array_name (arg1), byte_offset_var (arg2), res (destination)
            # 1. Get byte_offset into R1
            self.assembly_code.append(self._format_line("",f"MOV",f"R1, {self._get_p3_operand_syntax(arg2, 'load')} ","; R1 = byte offset"))
            # 2. Convert to word offset: R1 = R1 / 2 (or SHR R1, 1)
            self.assembly_code.append(self._format_line("",f"SHR",f"R1, 1 ","; R1 = word offset (P3 words are 2 bytes) [cite: 199]"))
            # 3. Get base address of array into R2. P3 doesn't have MOV REG, LABEL_ADDRESS directly for all instructions.
            #    We need to use EQU for base address or load it if dynamic.
            #    Let's assume arg1 (array_name) is a label whose value is the base address.
            #    MOV R2, #array_name (Loads immediate address value into R2)
            self.assembly_code.append(self._format_line("",f"MOV",f"R2, {arg1} ","; R2 = base address of array '{arg1}'"))
            # 4. Add offset: R2 = R2 + R1
            self.assembly_code.append(self._format_line("",f"ADD",f"R2, R1 ","; R2 = address of element"))
            # 5. Load value: R3 = M[R2] (register indirect)
            self.assembly_code.append(self._format_line("",f"MOV",f"R3, M[R2] ","; Load value from array element"))
            # 6. Store in res: M[res] = R3
            self.assembly_code.append(self._format_line("",f"MOV",f"{self._get_p3_operand_syntax(res, 'store')}, R3"))
        elif op == '[]=':  # array_name[byte_offset_var] = value_var
            # array_name (arg1), byte_offset_var (arg2), value_var (res in TAC quad)
            # 1. Get byte_offset into R1
            self.assembly_code.append(self._format_line("",f"MOV",f"R1, {self._get_p3_operand_syntax(arg2, 'load')}","; R1 = byte offset"))
            # 2. Convert to word offset
            self.assembly_code.append(self._format_line("",f"SHR",f"R1, 1","; R1 = word offset [cite: 199]"))
            # 3. Get base address of array into R2
            self.assembly_code.append(self._format_line("",f"MOV",f"R2, {arg1} ","; R2 = base address of array '{arg1}'"))
            # 4. Add offset: R2 = R2 + R1
            self.assembly_code.append(self._format_line("",f"ADD",f"R2, R1 ","; R2 = address of element"))
            # 5. Get value_to_store into R3
            self.assembly_code.append(self._format_line("",f"MOV",f"R3, {self._get_p3_operand_syntax(res, 'load')} ","; R3 = value to store"))
            # 6. Store value: M[R2] = R3
            self.assembly_code.append(self._format_line("",f"MOV",f"M[R2], R3 ","; Store value into array element"))

        # Pilha (stack)
        elif op == 'PUSH':
            # Empilha valor de arg1
            self.assembly_code.append(self._format_line("", "PUSH", arg1_label))
        elif op == 'POP':
            # Retira valor do topo da pilha para res
            self.assembly_code.append(self._format_line("", "POP", res_label))

        # Funções
        # --- Function Call Mechanism ---
        elif op == 'PARAM':  # param arg1
            self.assembly_code.append(self._format_line("",f"MOV",f"R1, {self._get_p3_operand_syntax(arg1, 'load')}"))
            self.assembly_code.append(self._format_line("",f"PUSH",f"R1","; Push parameter"))

        elif op == 'CALL': # res = call func_name (arg1 is func_name, res is for return value)
            # Chamada de função (label)
            #self.assembly_code.append(self._format_line("", "CALL", res_label))
            self.assembly_code.append(self._format_line("",f"CALL",f"{self._get_p3_operand_syntax(arg1, 'address').upper()}","; PC pushed to stack"))
            if res:  # Function has a return value, assume it's in R1 by convention
                self.assembly_code.append(self._format_line("",
                    f"MOV",f"{self._get_p3_operand_syntax(res, 'store')}, R1","; Store return value (conventionally R1)"))
            if arg1 == "reads":
                self.add_function_reads()
            if arg1 == "readc":
                self.add_function_readc()
            if arg1 == "read":
                self.add_function_read()

        elif op == 'RETURN': # return (optional_value)
            # Retorno de função
            # self.assembly_code.append(self._format_line("", "RET"))
            if arg1:  # There is a return value
                self.assembly_code.append(self._format_line("",
                    f"MOV",f"R1, {self._get_p3_operand_syntax(arg1, 'load')}","; Load return value into R1 (convention)"))
            self.assembly_code.append(self._format_line("",f"RET","","; Return from subroutine, PC restored from stack [cite: 183]"))

        elif op == 'HALT':
            # Termina a execução do programa
            # O P3 não tem uma instrução HALT, definimos 'Fim' como ponto de paragem.
            self.assembly_code.append(self._format_line(f"; {op.lower()}", "-" * 25))
            self.assembly_code.append(self._format_line("", "BR", "Fim", "; Fim com loop infinito"))

        # --------------------------------------------------------------------------------------------------------------
        # Funções Entrada/Saída
        # --------------------------------------------------------------------------------------------------------------
        elif op == 'READ':
            # read(): Lê int ou double.
            self.assembly_code.append(self._format_line(f"; {op.lower()} {arg1_label}", "", "-"*25))
            #self.assembly_code.append(self._format_line("", "MOV", "R1", "M[FFFFh]"))
            #self.assembly_code.append(self._format_line("", "MOV", f"{res_label}, R1"))

        elif op == 'READC':
            # readc(): Lê caracter (retorna valor ASCII).
            self.assembly_code.append(self._format_line(f"; {op.lower()} {arg1_label}", "", "-"*25))
            self.assembly_code.append(self._format_line("", "CALL", f"{op.upper()}", "; Chama a rotina"))
            self.assembly_code.append(
                self._format_line("", "MOV", f"M[{arg1_label}], R1", "; Endereço do valor passado via pilha"))
            self.assembly_code.append("")
            self.add_function_readc()

        elif op == 'READS':
            # reads(): Lê string para vetor de int (termina em 0).
            self.assembly_code.append(self._format_line(f"; {op.lower()} {arg1_label}", "", "-"*25))
            self.assembly_code.append(self._format_line("", "CALL", f"{op.upper()}", "; Chama a rotina"))
            self.assembly_code.append("")
            self.add_function_reads()

        elif op == 'WRITE':
            # write(x): Imprime valor de variável.
            self.assembly_code.append(self._format_line(f"; {op.lower()} {arg1_label}", "", "-"*25))
            self.assembly_code.append(self._format_line("", "PUSH", "R1", "; Guarda R1"))
            self.assembly_code.append(self._format_line("", "PUSH", "R2", "; Guarda R2"))
            self.assembly_code.append(self._format_line("", "PUSH", f"{arg1_label}", "; Endereço do valor passado via pilha"))
            self.assembly_code.append(self._format_line("", "CALL", f"{op.upper()}", "; Chama a rotina"))
            self.assembly_code.append(self._format_line("", "POP", "R0"))
            self.assembly_code.append(self._format_line("", "POP", "R2"))
            self.assembly_code.append(self._format_line("", "POP", "R1"))
            self.assembly_code.append("")
            self.add_function_write()
            # em alternativa, imprime o carater
            #self.assembly_code.append(self._format_line("", "MOV", f"R1, M[{arg1_label}]", "; Lê o carater apontado por R1"))
            #self.assembly_code.append(self._format_line("", "MOV", "M[FFFEh], R1", "; Escreve o carater no endereço de saída"))

        elif op == 'WRITEC':
            # writec(x): Imprime caracter (ASCII).
            self.assembly_code.append(self._format_line(f"; {op.lower()} {arg1_label}", "", "-"*25))
            self.assembly_code.append(self._format_line("", "PUSH", "R1", "; Guarda R1"))
            self.assembly_code.append(self._format_line("", "PUSH", "R2", "; Guarda R2"))
            self.assembly_code.append(self._format_line("", "PUSH", f"{arg1_label}", "; Endereço do valor passado via pilha"))
            self.assembly_code.append(self._format_line("", "CALL", f"{op.upper()}", "; Chama a rotina"))
            self.assembly_code.append(self._format_line("", "POP", "R0"))
            self.assembly_code.append(self._format_line("", "POP", "R2"))
            self.assembly_code.append(self._format_line("", "POP", "R1"))
            self.assembly_code.append("")
            self.add_function_writec()

        elif op == 'WRITEV':
            # writev(vetor): Imprime vetor no formato {48, 49, 0}.
            self.assembly_code.append(self._format_line(f"; {op.lower()} {arg1_label}", "", "-"*25))
            self.assembly_code.append(self._format_line("", "PUSH", f"{arg1_label}", "; Endereço do valor passado via pilha"))
            self.assembly_code.append(self._format_line("", "CALL", f"{op.upper()}", "; Chama a rotina"))
            self.assembly_code.append(self._format_line("", "POP", "R0"))
            self.assembly_code.append("")
            self.add_function_writev()

        elif op in ('WRITES'):
            # writes "string_literal"
            str_label = self.string_literal_map.get(arg1.strip('"'))
            if str_label:
                self.assembly_code.append(self._format_line(f"; {op.lower()} {str_label}", "", "-"*25))
                self.assembly_code.append(self._format_line("", "PUSH", "R1", "; Guarda R1"))
                self.assembly_code.append(self._format_line("", "PUSH", "R2", "; Guarda R2"))
                self.assembly_code.append(self._format_line("", "PUSH", f"{str_label}", "; Endereço da string passado via pilha"))
                self.assembly_code.append(self._format_line("", "CALL", f"{op.upper()}", "; Chama a rotina"))
                self.assembly_code.append(self._format_line("", "POP", "R0"))
                self.assembly_code.append(self._format_line("", "POP", "R2"))
                self.assembly_code.append(self._format_line("", "POP", "R1"))
                self.assembly_code.append("")
                self.add_function_writes()
            else:
                self.assembly_code.append(
                    self._format_line("", f"; ERROR: String literal para writes não encontrado: {arg1}"))

        else:
            # Caso não exista tradução, insere comentário de aviso
            self.assembly_code.append(f";; AVISO: Operação TAC '{op}' não traduzida para P3.")


    #-------------------------------------------------------------------------------------------------------------------
    # Definição de funções Entrada/Saída
    #-------------------------------------------------------------------------------------------------------------------
    def add_function_read(self):
        if 'read' not in self.declared_functions:
            self.declared_functions.add('read')
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append("; ----- Função read(): Lê int ou double.")

    def add_function_reads(self):
        if 'reads' not in self.declared_functions:
            self.declared_functions.add('reads')
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append("; ----- Função reads(): Lê string para vetor de int (termina em 0)")
            self.assemblyfunction_code.append(self._format_line("", ";RM ------------------------------------------------------------------------"))
            self.assemblyfunction_code.append(self._format_line("", ";RM - codigo já a funcionar bem no simulador P3, mas ainda não funciona aqui"))
            self.assemblyfunction_code.append(self._format_line("", ";RM - tenho de rever os problemas com o guardar dos registos usados"))
            self.assemblyfunction_code.append(self._format_line("", ";RM - e passagem de parametros/retorno de acordo com o 'Function Call Mechanism'"))
            self.assemblyfunction_code.append(self._format_line("", ";RM ------------------------------------------------------------------------"))
            self.assemblyfunction_code.append(self._format_line("READS:", "NOP"))
            #self.assemblyfunction_code.append(self._format_line("", "PUSH", "R1", "; Guarda registos usados"))
            #self.assemblyfunction_code.append(self._format_line("", "PUSH", "R2"))
            #self.assemblyfunction_code.append(self._format_line("", "PUSH", "R3"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R1, BUFFER", "; Ponteiro do buffer"))
            self.assemblyfunction_code.append(self._format_line("READS_L1:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R2, M[CTRL_PORT]", "; Verifica se há tecla disponível"))
            self.assemblyfunction_code.append(self._format_line("", "CMP", "R2, R0"))
            self.assemblyfunction_code.append(self._format_line("", "BR.Z", "READS_L1", "; Espera enquanto não houver tecla"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R3, M[IN_PORT]", "; Lê o carater"))
            self.assemblyfunction_code.append(self._format_line("", "CMP", "R3, LINEFEED", "; Verifica se carregou em Enter"))
            self.assemblyfunction_code.append(self._format_line("", "BR.Z","READS_L2", "; Se sim, termina"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "M[R1], R3", "; Guarda carater no buffer"))
            self.assemblyfunction_code.append(self._format_line("", "INC", "R1", "; Avança ponteiro"))
            self.assemblyfunction_code.append(self._format_line("", "BR", "READS_L1", "; Repete"))
            self.assemblyfunction_code.append(self._format_line("READS_L2:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R2, 0", "; Terminador NULL"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "M[R1], R2", "; Escreve terminador"))
            #self.assemblyfunction_code.append(self._format_line("", "POP", "R3", "; Restaura registos pela ordem inversa"))
            #self.assemblyfunction_code.append(self._format_line("", "POP", "R2"))
            #self.assemblyfunction_code.append(self._format_line("", "POP", "R1"))
            self.assemblyfunction_code.append(self._format_line("READS_END:", "RET"))
    def add_function_readc(self):
        if 'readc' not in self.declared_functions:
            self.declared_functions.add('readc')
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append("; ----- Função readc(): Lê caracter (retorna valor ASCII).")
            self.assemblyfunction_code.append(self._format_line("READC:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("", "CMP", "M[CTRL_PORT], R0", "; Verifica se há tecla disponível"))
            self.assemblyfunction_code.append(self._format_line("", "BR.Z", "READC", "; Espera enquanto não houver tecla"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R1, M[IN_PORT]", "; Lê o carater"))
            self.assemblyfunction_code.append(self._format_line("READC_END:", "RET"))

    def add_function_write(self):
        if 'write' not in self.declared_functions:
            self.declared_functions.add('write')
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append("; ----- Função write(x): Imprime valor de variável.")
            self.assemblyfunction_code.append(self._format_line("", ";RM ------------------------------------------------------------------------"))
            self.assemblyfunction_code.append(self._format_line("", ";RM - codigo já a funcionar bem no simulador P3, mas ainda não funciona aqui"))
            self.assemblyfunction_code.append(self._format_line("", ";RM - e falta guardar os valores dos registos usados"))
            self.assemblyfunction_code.append(self._format_line("", ";RM ------------------------------------------------------------------------"))
            self.assemblyfunction_code.append(self._format_line("WRITE:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("", "MOV","R1, M[SP+2]","; R1 = valor a imprimir"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R1, M[R1]", "; R1 = valor a imprimir"))
            self.assemblyfunction_code.append(self._format_line("", "MOV","R7, 10000","; Divisor inicial (10^4)"))
            self.assemblyfunction_code.append(self._format_line("", "MOV","R6, R0","; Flag: dígito já impresso (0 = ainda não)"))
            self.assemblyfunction_code.append(self._format_line("WRITE_L1:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R2, R1", "; R2 = valor atual"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R3, R7", "; R3 = divisor"))
            self.assemblyfunction_code.append(self._format_line("", "DIV", "R2, R3", "; R2 = quociente (dígito), R3 = resto"))
            self.assemblyfunction_code.append(self._format_line("", "CMP", "R6, R0", "; Já imprimimos algum dígito?"))
            self.assemblyfunction_code.append(self._format_line("", "BR.NZ", "WRITE_L2", "; Se sim, imprime sempre"))
            self.assemblyfunction_code.append(self._format_line("", "CMP", "R2, R0"))
            self.assemblyfunction_code.append(self._format_line("", "BR.Z", "WRITE_L3", "; Se dígito é 0 e nada impresso, salta"))
            self.assemblyfunction_code.append(self._format_line("WRITE_L2:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("", "ADD", "R2, 48", "; Converte para ASCII"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "M[OUT_PORT], R2", "; Escreve dígito"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R6, 1", "; Marca que começámos a imprimir"))
            self.assemblyfunction_code.append(self._format_line("WRITE_L3:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R1, R3", "; Atualiza valor com o resto"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R4, 10"))
            self.assemblyfunction_code.append(self._format_line("", "DIV", "R7, R4", "; R7 = R7 / 10 (próximo divisor)"))
            self.assemblyfunction_code.append(self._format_line("", "CMP", "R7, R0"))
            self.assemblyfunction_code.append(self._format_line("", "BR.NZ", "WRITE_L1"))
            self.assemblyfunction_code.append(self._format_line("", "; Caso número seja 0 imprime '0'"))
            self.assemblyfunction_code.append(self._format_line("", "CMP", "R6, R0"))
            self.assemblyfunction_code.append(self._format_line("", "BR.NZ", "WRITE_LF"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R1, '0'"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "M[OUT_PORT], R1"))
            self.assemblyfunction_code.append(self._format_line("WRITE_LF:", "MOV", "R2, LINEFEED","; Muda de linha"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "M[OUT_PORT], R2"))
            self.assemblyfunction_code.append(self._format_line("WRITE_END:", "RET"))

    def add_function_writec(self):
        if 'writec' not in self.declared_functions:
            self.declared_functions.add('writec')
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append("; ----- Função writec(x): Imprime caracter (ASCII).")
            #self.assemblyfunction_code.append(self._format_line("", ";RM ------------------------------------------------------------------------"))
            #self.assemblyfunction_code.append(self._format_line("", ";RM - codigo já a funcionar bem no simulador P3, mas ainda não funciona aqui"))
            #self.assemblyfunction_code.append(self._format_line("", ";RM - e falta guardar os valores dos registos usados"))
            #self.assemblyfunction_code.append(self._format_line("", ";RM ------------------------------------------------------------------------"))
            #self.assemblyfunction_code.append(self._format_line("WRITEC:", "NOP"))
            #self.assemblyfunction_code.append(self._format_line("", "MOV", "R1, M[SP+2]", "; R1 = valor ASCII (ex: 49)"))
            #self.assemblyfunction_code.append(self._format_line("", "; Guarda valor original"))
            #self.assemblyfunction_code.append(self._format_line("", "MOV", "R4, R1"))
            #self.assemblyfunction_code.append(self._format_line("", "; Divide por 10"))
            #self.assemblyfunction_code.append(self._format_line("", "MOV", "R2, R1"))
            #self.assemblyfunction_code.append(self._format_line("", "MOV", "R3, 10"))
            #self.assemblyfunction_code.append(self._format_line("", "DIV", "R2, R3", "; R2 = dezenas, R3 = unidades"))
            #self.assemblyfunction_code.append(self._format_line("", "; Converte e escreve dígito das dezenas"))
            #self.assemblyfunction_code.append(self._format_line("", "ADD", "R2, 48"))
            #self.assemblyfunction_code.append(self._format_line("", "MOV", "M[OUT_PORT], R2"))
            #self.assemblyfunction_code.append(self._format_line("", "; Converte e escreve dígito das unidades"))
            #self.assemblyfunction_code.append(self._format_line("", "ADD", "R3, 48"))
            #self.assemblyfunction_code.append(self._format_line("", "MOV", "M[OUT_PORT], R3"))
            #self.assemblyfunction_code.append(self._format_line("WRITEC_LF:", "MOV", "R2, 10","; \\n"))
            #self.assemblyfunction_code.append(self._format_line("", "MOV", "M[OUT_PORT], R2"))
            #self.assemblyfunction_code.append(self._format_line("WRITEC_END:", "RET"))

            # interpretação alternativa da função, imprime o carater na variável
            self.assemblyfunction_code.append(self._format_line("WRITEC:", "NOP", "","; escreve um carater na consola"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R1, M[SP+2]","; Endereço da string passado via pilha"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R2, M[R1]","; Lê o carater apontado por R1"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "M[FFFEh], R2","; Escreve o carater no endereço de saída"))
            self.assemblyfunction_code.append(self._format_line("WRITEC_END:", "RET",  "",""))

    def add_function_writev(self):
        if 'writev' not in self.declared_functions:
            self.declared_functions.add('writev')
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append("; ----- Função writev(vetor): Imprime vetor no formato {48, 49, 0}.")
            self.assemblyfunction_code.append(self._format_line("", ";RM ------------------------------------------------------------------------"))
            self.assemblyfunction_code.append(self._format_line("", ";RM - agora está a terminar se apanhar um valor 0"))
            self.assemblyfunction_code.append(self._format_line("", ";RM - é preciso alterar para passar 2 valores no stack, o vetor e o tamanho..."))
            self.assemblyfunction_code.append(self._format_line("", ";RM ------------------------------------------------------------------------"))
            self.assemblyfunction_code.append(self._format_line("WRITEV:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R1, M[SP+2]","; Endereço da string passado via pilha"))
            self.assemblyfunction_code.append(self._format_line("WRITEV_LOOP:", "MOV", "R2, M[R1]", "; Lê o carater apontado por R1"))
            self.assemblyfunction_code.append(self._format_line("", "CMP", "R2, R0","; Compara com o terminador"))
            self.assemblyfunction_code.append(self._format_line("", "JMP.Z", "WRITEV_END","; Se for zero, salta para o fim"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R3, R1"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R1", "; Guarda R1"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R2", "; Guarda R2"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R3", "; Endereço do valor passado via pilha"))
            self.assemblyfunction_code.append(self._format_line("", "CALL", "WRITE","; Chama a rotina"))
            self.assemblyfunction_code.append(self._format_line("", "POP", "R0"))
            self.assemblyfunction_code.append(self._format_line("", "POP", "R2"))
            self.assemblyfunction_code.append(self._format_line("", "POP", "R1"))
            self.assemblyfunction_code.append(self._format_line("", "INC", "R1","; Avança para a próxima posição"))
            self.assemblyfunction_code.append(self._format_line("", "JMP", "WRITEV_LOOP","; Repete o ciclo"))
            self.assemblyfunction_code.append(self._format_line("WRITEV_LF:", "MOV", "R2, LINEFEED","; Muda de linha"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "M[OUT_PORT], R2"))
            self.assemblyfunction_code.append(self._format_line("WRITEV_END:", "RET"))

    def add_function_writes(self):
        if 'writes' not in self.declared_functions:
            self.declared_functions.add('writes')
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append("; ----- Função writes(\"texto\"): Imprime string")
            self.assemblyfunction_code.append(self._format_line("", "; Altera R1, R2"))
            self.assemblyfunction_code.append(self._format_line("WRITES:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R1, M[SP+2]","; Endereço da string passado via pilha"))
            self.assemblyfunction_code.append(self._format_line("WRITES_L1:", "MOV", "R2, M[R1]","; Lê o carater apontado por R1"))
            self.assemblyfunction_code.append(self._format_line("", "CMP", "R2, R0","; Compara com o terminador"))
            self.assemblyfunction_code.append(self._format_line("", "JMP.Z", "WRITES_LF","; Se for zero, salta para o fim"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "M[OUT_PORT], R2","; Escreve o carater no endereço de saída"))
            self.assemblyfunction_code.append(self._format_line("", "INC", "R1","; Avança para o próximo carater"))
            self.assemblyfunction_code.append(self._format_line("", "JMP", "WRITES_L1","; Repete o ciclo"))
            self.assemblyfunction_code.append(self._format_line("WRITES_LF:", "MOV", "R2, LINEFEED","; Muda de linha"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "M[OUT_PORT], R2"))
            self.assemblyfunction_code.append(self._format_line("WRITES_END:", "RET"))


    # -------------------------------------------------------------------------------------------------------------------


    def generate_from_tac_list(self, tac_list):
        """
        Gera o código Assembly P3 completo a partir de uma lista de instruções TAC.
        Retorna o código como uma string pronta a ser escrita num ficheiro .as.
        """
        #self.data_section = []
        self.assembly_code = []
        self.assemblyfunction_code = []
        #self.var_labels = {}
        #self.label_generator_count = 0

        # Primeira passagem: declara arrays variáveis e constantes
        # for instr in tac_list:
        #     if instr.get('op', '').upper() == 'ALLOC':
        #         self._declare_array(instr.get('arg1'), instr.get('arg2'))
        #     else:
        #         self._get_var_label(instr.get('res'))
        #         self._get_var_label(instr.get('arg1'))
        #         self._get_var_label(instr.get('arg2'))
        '''
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
'''
        # Segunda passagem: traduz instruções TAC para assembly
        for indice, instr in enumerate(tac_list):
            quad_num = indice + 1
            self.translate_tac_instruction(instr, quad_num)

        # Monta o código final
        output = []
        if self.data_section:
            output.append(self._format_line(";" + "=" * 14, "Região de Dados (inicia no endereço 8000h)"))
            output.append(self._format_line("", "ORIG", "8000h"))
            output.append("")
            output.extend(sorted(self.data_section))
            output.append("")

        output.append(self._format_line(";" + "-" * 14, "Definições de Constantes de sistema"))
        output.append(self._format_line("SP_ADDRESS", "EQU", "FDFFh"))
        output.append(self._format_line("CTRL_PORT","EQU","FFFDh", "; Porto de controlo do teclado"))
        output.append(self._format_line("IN_PORT","EQU","FFFFh", "; Porto de entrada de texto (teclado)"))
        output.append(self._format_line("OUT_PORT","EQU","FFFEh", "; Porto de saída (consola)"))
        output.append(self._format_line("LINEFEED","EQU","10", "; Código ASCII da tecla enter na consola (LF)"))
        output.append("")

        output.append(self._format_line(";"+"="*14, "Região de Código (inicia no endereço 0000h)"))
        output.append(self._format_line("", "ORIG", "0000h"))

        output.append(self._format_line("", "JMP", "_start","; jump to main"))
        output.append("")
        output.append(self._format_line(";"+"-"*14, "Rotinas"))

        output.extend(self.assemblyfunction_code)

        output.append("")
        output.append(self._format_line(";"+"-"*14, "Programa Principal "))

        output.append(self._format_line(f"{self.program_entry_point}:", "NOP"))

        output.append(self._format_line("", "MOV", "R7, SP_ADDRESS"))
        output.append(self._format_line("", "MOV", "SP, R7", "; Define o Stack Pointer"))
        output.append("")
        output.extend(self.assembly_code)
        output.append("")
        output.append(self._format_line("Fim:", "BR", "Fim"))
        output.append("")
        return "\n".join(output)
