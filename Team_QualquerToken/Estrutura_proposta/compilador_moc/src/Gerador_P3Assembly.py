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
        # Lista para armazenar temporariamente as linhas de código assembly geradas das funcoes
        self.assemblyfunction_codetemp = []
        # vamos armazenar que funcoes já foram declaradas
        self.declared_functions = set()
        # Dicionário para mapear nomes de variáveis para labels P3
        self.var_labels = {}

        # Contador para gerar labels únicos (usado em saltos e condições)
        self.label_generator_count = 0
        self.string_literal_count = 0
        self.string_literal_map = {}  # Mapeia as strings constant para uma label
        self.declared_vars = set()  # Para termos o track das vars/temps para a seccao de dados
        self.last_op=""
        # Ponto de entrada do programa (label inicial)
        self.program_entry_point = "_start"
        # Pre-scan de todas as variaveis, temporarios, e alocacoes de arrays
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
        char_parts = [f"'{char}'" for char in string_content]
        char_parts.append("0")  # Null terminator
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
            return s_tac_operand  # P3  numeros/caracteres
        elif s_tac_operand.startswith("'") and s_tac_operand.endswith("'") and len(s_tac_operand) == 3:  # char literal
            return s_tac_operand  # exemplo 'A'
        elif self._is_tac_temp(s_tac_operand) or s_tac_operand in self.declared_vars:
            # Estas sáo variaveis/temporarias armazenadas em memoria
            if context == "store" or context == "load":
                label= self._get_var_label(s_tac_operand)
                return f"M[{label}]"  # Accesso à localização da memória
            return s_tac_operand  # Retorna nome para o contexto do endereço se necessário
        elif self._is_tac_label(s_tac_operand) or s_tac_operand in ["main", "end_main"] or s_tac_operand.startswith(
                "end_"):  # Labels para jumps/calls
            return s_tac_operand
        else:  # Default para simbolos desconhecidos, é o nome de uma variavel / localização de memoria
            if context == "store" or context == "load":
                return f"M[{s_tac_operand}]"
            return s_tac_operand

    def _pre_scan_quadruplos(self):
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
                self._add_string_literal(str_content)  # Declara na data_section

            if quad['op'] == 'label':
                # é uma label de uma funçáo se já existir main não coloca
                for operand in operands:
                    if operand and isinstance(operand, str):
                        self.declared_functions.add(operand)

            for operand in operands:
                if operand and isinstance(operand, str):
                    if self._is_tac_temp(operand) or (not self._is_immediate_val(operand) and not self._is_tac_label(
                            operand) and not operand.startswith("'") and not operand.endswith(":")):
                        self.declared_vars.add(operand)
    @staticmethod
    def _format_line(col1: str, col2: str = "", col3: str = "", col4: str = "") -> str:
        # Formata quatro strings em uma linha única com colunas em posições fixas:
        return f"{col1:<16}{col2:<8}{col3:<16}{col4}"

    @staticmethod
    def _sanitize_var(name):
        # Limpa e adapta o nome da variável para ser usado como label no Assembly P3.
        # Substitui caracteres especiais e garante unicidade.
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
        # Devolve o label P3 associado a uma variável.
        # Se ainda não existir, cria a declaração no segmento de dados.
        name = self._sanitize_var(name)
        if name is None:
            return None
        if name not in self.var_labels:
            label = f"VAR_{name.upper()}"
            self.var_labels[name] = label
            self.data_section.append(self._format_line(label, "WORD", name, f"; {name}"))
        return self.var_labels[name]

    def _get_var_label(self, name):
        # Devolve uma etiqueta P3 curta e única associada a uma variável.
        # Se a etiqueta para esta variável ainda não existir, cria a sua
        # declaração no segmento de dados.
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
            try:
                # Tenta converter 'name' para um inteiro.
                valor_inteiro = int(name)
                # Se funcionar, é um número.
                self.data_section.append(self._format_line(label, "WORD", name, f"; {name}"))
            except (ValueError, TypeError):
                # Se a conversão falhar, não é um número. Trata-se de um nome de variável.
                self.data_section.append(self._format_line(label, "WORD", "0", f"; variável '{name}'"))
        # Devolve a etiqueta curta e única associada ao nome
        return self.var_labels[name]

    def _declare_array(self, name, size):
        # Declara um array no segmento de dados.
        # Remove declarações anteriores do mesmo nome para evitar duplicação.
        name = self._sanitize_var(name)
        label = f"VAR_{name.upper()}"
        decl = self._format_line(f"{label}", "TAB", size, f"; Array {name}")  # sem dois pontos!
        # Remove possíveis declarações anteriores da mesma variável
        self.data_section = [d for d in self.data_section if not d.startswith(f"{label} ")]
        self.data_section.append(decl)
        self.var_labels[name] = label
        return label

    def _gen_label(self, base="L"):
        # Gera um label único para saltos condicionais ou blocos de código.
        self.label_generator_count += 1
        return f"{base}{self.label_generator_count}"

    def adicionar_codigo(self, codigo_str: str, tipo_codigo: str):
        """
        Adiciona uma string de código ao local apropriado (assemblycode ou assemblyfunction_code).
        Args:
            codigo_str (str): A string de código assembly a ser adicionada.
            tipo_codigo (str): Indica onde o código deve ser adicionado.
                               Pode ser 'geral' para assemblycode ou 'funcao' para assemblyfunction_code.        """
        if tipo_codigo == 'geral':
            self.assembly_code.append(codigo_str)
        elif tipo_codigo == 'funcao':
            self.assemblyfunction_codetemp.append(codigo_str)
        else:
            print(f"Tipo de código '{tipo_codigo}' inválido. Usar 'geral' ou 'funcao'.")

    def translate_tac_instruction(self, instr, quad_num, tipo_codigo: str):
        # Traduz uma instrução TAC (dicionário) para Assembly P3 e adiciona as linhas geradas.
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
                    # se arg1 é o nome de uma variavel, necessitamos de M[]
                    p3_arg1_syntax = f"M[{arg1}]" if not self._is_immediate_val(str(arg1)) else str(arg1)
            else:
                p3_arg1_syntax = self._get_p3_operand_syntax(arg1_label, 'load')
            self.adicionar_codigo(self._format_line("", "MOV", f"R1, {p3_arg1_syntax}"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", f"MOV", f"{self._get_p3_operand_syntax(res, 'store')}, R1"),
                                  tipo_codigo)

        # Operações aritméticas e atribuição
        # res = arg1 op arg2. Um operando P3 deve ser um registo
        # Padrão geral: MOV R1, arg1; MOV R2, arg2; P3_OP R1, R2; MOV res, R1
        elif op in ['+', '-', '*', '/', '%']:
            # Load arg1 -> R1
            self.adicionar_codigo(self._format_line("", f"MOV", f"R1, {self._get_p3_operand_syntax(arg1, 'load')}"),
                                  tipo_codigo)
            # Load arg2 ->  R2
            self.adicionar_codigo(self._format_line("", f"MOV", f"R2, {self._get_p3_operand_syntax(arg2, 'load')}"),
                                  tipo_codigo)
            p3_res_syntax = self._get_p3_operand_syntax(res, 'store')
            if op in '+':
                # res = arg1 + arg2
                self.adicionar_codigo(self._format_line("", "ADD", "R1, R2", "; ZCNO flags affected"), tipo_codigo)
                self.adicionar_codigo(self._format_line("", f"MOV", f"{p3_res_syntax}, R1"), tipo_codigo)
            elif op in '-':
                # res = arg1 - arg2
                self.adicionar_codigo(self._format_line("", "SUB", "R1, R2", "; ZCNO flags affected"), tipo_codigo)
                self.adicionar_codigo(self._format_line("", f"MOV", f"{p3_res_syntax}, R1"), tipo_codigo)
            elif op in '*':  # MUL op1, op2 -> op1 has MSW, op2 has LSW.
                # res = arg1 * arg2
                self.adicionar_codigo(
                    self._format_line("", "MUL", "R1, R2", "; R1=MSW, R2=LSW. Unsigned. Z based on 32bit, CNO=0"),
                    tipo_codigo)
                self.adicionar_codigo(self._format_line("", "MOV", f"{p3_res_syntax}, R2", "; Store LSW into result"),
                                      tipo_codigo)
            elif op in '/':  # DIV op1, op2 -> op1 tem Quociente, op2 tem Resto.
                # res = arg1 / arg2
                self.adicionar_codigo(self._format_line("", "DIV", "R1, R2",
                                                        "; R1=Quociente, R2=Resto. Unsigned. O on div by zero, CN=0."),
                                      tipo_codigo)
                self.adicionar_codigo(
                    self._format_line("", "MOV", f"{p3_res_syntax}, R1", "; Guarda Quociente no resultado"),
                    tipo_codigo)
            elif op in '%':  # DIV op1, op2 -> op1 tem Quociente, op2 tem Resto.
                # res = arg1 / arg2
                self.adicionar_codigo(
                    self._format_line("", "DIV", "R1, R2",
                                      "; R1=Quociente, R2=Resto. Unsigned. O on div by zero, CN=0."), tipo_codigo)
                self.adicionar_codigo(
                    self._format_line("", "MOV", f"{p3_res_syntax}, R2", "; Guarda Resto no resultado"), tipo_codigo)
        elif op == '!':
            self.adicionar_codigo(self._format_line("", "CMP", "R2, R1"), tipo_codigo)
        # Operações lógicas
        elif op in ('AND',):
            # res = arg1 AND arg2
            self.adicionar_codigo(self._format_line("", "MOV", f"R1, {arg1_label}"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "MOV", f"R2, {arg2_label}"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "AND", "R1, R2"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "MOV", f"{res_label}, R1"), tipo_codigo)
        elif op in ('OR',):
            # res = arg1 OR arg2
            self.adicionar_codigo(self._format_line("", "MOV", f"R1, {arg1_label}"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "MOV", f"R2, {arg2_label}"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "OR", "R1, R2"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "MOV", f"{res_label}, R1"), tipo_codigo)
        elif op in ('XOR',):
            # res = arg1 XOR arg2
            self.adicionar_codigo(self._format_line("", "MOV", f"R1, {arg1_label}"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "MOV", f"R2, {arg2_label}"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "XOR", "R1, R2"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "MOV", f"{res_label}, R1"), tipo_codigo)

        # Comparações (CMP + saltos)
        elif op in ('==', '!=', '<', '<=', '>', '>='):
            # res = (arg1 op arg2) ? 1 : 0

            self.adicionar_codigo(self._format_line("", "MOV", f"R1, {self._get_p3_operand_syntax(arg1, 'load')}"),
                                  tipo_codigo)
            self.adicionar_codigo(self._format_line("", "MOV", f"R2, {self._get_p3_operand_syntax(arg2, 'load')}"),
                                  tipo_codigo)
            self.adicionar_codigo(self._format_line("", "CMP", "R1, R2", "; ZCNO flags affected"), tipo_codigo)
            self.last_op = op

        elif op == 'IFFALSE':
            # Mapeamento do operador TAC para o salto P3 correspondente
            # Verificamos a last_op que contem a condição
            salto = {
                '==': 'JMP.NZ',  # igual
                '!=': 'JMP.Z',  # diferente
                '<': 'JMP.P',  # menor
                '<=': 'JMP.P',  # menor ou igual
                '>': 'JMP.N',  # maior
                '>=': 'JMP.N'  # maior ou igual
            }[self.last_op]
            salto2 = {
                '==': '',  # igual
                '!=': '',  # diferente
                '<': 'JMP.Z',  # menor
                '<=': '',  # menor ou igual
                '>': 'JMP.Z',  # maior
                '>=': ''  # maior ou igual
            }[self.last_op]

            self.adicionar_codigo(self._format_line("", salto, f"{res}"), tipo_codigo)
            if (salto2 != ''):
                self.adicionar_codigo(self._format_line("", salto2, f"{res}"), tipo_codigo)

        elif op == 'IFGOTO':
            # Mapeamento do operador TAC para o salto P3 correspondente
            # Verificamos a last_op que contem a condição
            salto = {
                '==': 'JMP.Z',  # igual
                '!=': 'JMP.NZ',  # diferente
                '<': 'JMP.N',  # menor
                '<=': 'JMP.N',  # menor ou igual
                '>': 'JMP.P',  # maior
                '>=': 'JMP.P'  # maior ou igual
            }[self.last_op]
            salto2 = {
                '==': '',  # igual
                '!=': '',  # diferente
                '<': 'JMP.Z',  # menor
                '<=': '',  # menor ou igual
                '>': 'JMP.Z',  # maior
                '>=': ''  # maior ou igual
            }[self.last_op]

            self.adicionar_codigo(self._format_line("", salto, f"{res}"), tipo_codigo)
            if (salto2 != ''):
                self.adicionar_codigo(self._format_line("", salto2, f"{res}"), tipo_codigo)

        # Saltos e labels
        elif op == 'LABEL':
            # Marca um label no código
            self.adicionar_codigo(self._format_line(res.upper() + ":", "NOP"), tipo_codigo)
        elif op == 'GOTO':
            # Salto incondicional
            self.adicionar_codigo(self._format_line("", "JMP", self._get_p3_operand_syntax(res, 'address')),
                                  tipo_codigo)
        elif op == 'IFGOTO2':  # if cond_var goto label
            self.adicionar_codigo(self._format_line("", "MOV", f"R1, {self._get_p3_operand_syntax(arg1, 'load')}"),
                                  tipo_codigo)
            self.adicionar_codigo(self._format_line("", "CMP", "R1, 0", ), tipo_codigo)
            self.adicionar_codigo(self._format_line("", f"JMP.NZ", f"{self._get_p3_operand_syntax(res, 'address')}"),
                                  tipo_codigo)

        # Arrays TESTAR
        elif op == 'ALLOC':
            # Declaração de array (já tratada na primeira passagem)
            self._declare_array(arg1, arg2)
        elif op == 'LOAD_ARRAY':
            # res = arg1[arg2]
            arr = self._get_var_label(arg1)
            idx = self._get_var_label(arg2)
            self.adicionar_codigo(self._format_line("", "MOV", "R1", idx), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "MOV", "R2", arr + "[R1]"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "MOV", res_label, "R2"), tipo_codigo)
        elif op == 'STORE_ARRAY':
            # arg1[arg2] = res
            arr = self._get_var_label(arg1)
            idx = self._get_var_label(arg2)
            val = self._get_var_label(res)
            self.adicionar_codigo(self._format_line("", "MOV", "R1", idx), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "MOV", "R2", val), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "MOV", arr + "[R1]", "R2"), tipo_codigo)

            # --- Array Operations ---
            # TAC: t_offset = index * 4 (bytes)
            # P3: word_offset = byte_offset / 2
        elif op == '[]':  # res = array_name[byte_offset_var]
            # array_name (arg1), byte_offset_var (arg2), res (destination)
            self.adicionar_codigo(self._format_line("", f"MOV", f"R1, {self._get_p3_operand_syntax(arg2, 'load')} ",
                                                    "; R1 = byte offset"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", f"SHR", f"R1, 1 ", "; R1 = word offset"), tipo_codigo)
            # 3. base address do array em R2
            # MOV R2, #array_name (Loads  address no R2)
            self.adicionar_codigo(
                self._format_line("", f"MOV", f"R2, {arg1} ", "; R2 = endereco base do array '{arg1}'"), tipo_codigo)
            # 4. offset: R2 = R2 + R1
            self.adicionar_codigo(self._format_line("", f"ADD", f"R2, R1 ", "; R2 = endereco do elemento"), tipo_codigo)
            # 5. Load value: R3 = M[R2] (register indirect)
            self.adicionar_codigo(self._format_line("", f"MOV", f"R3, M[R2] ", "; Load value no array element"),
                                  tipo_codigo)
            # 6. Store in res: M[res] = R3
            self.adicionar_codigo(self._format_line("", f"MOV", f"{self._get_p3_operand_syntax(res, 'store')}, R3"),
                                  tipo_codigo)
        elif op == '[]=':  # array_name[byte_offset_var] = value_var
            # array_name (arg1), byte_offset_var (arg2), value_var (res in TAC quad)
            # byte_offset -> R1
            self.adicionar_codigo(
                self._format_line("", f"MOV", f"R1, {self._get_p3_operand_syntax(arg2, 'load')}", "; R1 = byte offset"),
                tipo_codigo)
            # Converter para word offset
            self.adicionar_codigo(self._format_line("", f"SHR", f"R1, 1", "; R1 = word offset"), tipo_codigo)
            # Obter endrreco base do array -> R2
            self.adicionar_codigo(
                self._format_line("", f"MOV", f"R2, {arg1} ", "; R2 = endereco base do array '{arg1}'"), tipo_codigo)
            # Adicionar offset: R2 = R2 + R1
            self.adicionar_codigo(self._format_line("", f"ADD", f"R2, R1 ", "; R2 = endereco do elemento"), tipo_codigo)
            # Obter value_to_store -> R3
            self.adicionar_codigo(self._format_line("", f"MOV", f"R3, {self._get_p3_operand_syntax(res, 'load')} ",
                                                    "; R3 = valor a guardar"), tipo_codigo)
            # Store value: M[R2] = R3
            self.adicionar_codigo(self._format_line("", f"MOV", f"M[R2], R3 ", "; Guarda valor no array element"),
                                  tipo_codigo)

        # Pilha (stack)
        elif op == 'PUSH':
            # Empilha valor de arg1
            self.adicionar_codigo(self._format_line("", "PUSH", arg1_label), tipo_codigo)
        elif op == 'POP':
            # Retira valor do topo da pilha para res
            self.adicionar_codigo(self._format_line("", "POP", res_label), tipo_codigo)

        # Funções
        elif op == 'PARAM':  # param arg1
            self.adicionar_codigo(self._format_line("", f"MOV", f"R1, {self._get_p3_operand_syntax(arg1, 'load')}"),
                                  tipo_codigo)
            self.adicionar_codigo(self._format_line("", f"PUSH", f"R1", "; Push parameter"), tipo_codigo)

        elif op == 'CALL':
            # Chamada de função (label)
            self.adicionar_codigo(self._format_line(f"; {op.lower()} {arg1}", "", "-" * 25), tipo_codigo)
            # se a função tem valor de retorno, reserva espaço no stack
            if res:
                if arg1 == "reads":
                    self.adicionar_codigo(self._format_line("", "PUSH", f"{res_label}", "; Endereço da variável"), tipo_codigo)
                else:
                    self.adicionar_codigo(self._format_line("", "PUSH", "R0", "; Reserva espaço para retorno"), tipo_codigo)

            # chama a função
            self.adicionar_codigo(self._format_line("", f"CALL", f"{self._get_p3_operand_syntax(arg1, 'address').upper()}","; Chama a rotina"), tipo_codigo)

            # se a função tem valor de retorno, está no stack
            if res:
                if arg1 == "reads":
                    self.adicionar_codigo(self._format_line("", "POP", "R0", "; Limpa a pilha, a leitura já está na variável certa"), tipo_codigo)
                else:
                    self.adicionar_codigo(self._format_line("", "POP", f"{self._get_p3_operand_syntax(res, 'store')}", "; Atribui o valor à variável"), tipo_codigo)

            self.adicionar_codigo("", tipo_codigo)

            # adicionar funções
            if arg1 == "reads":
                self.add_function_reads()
            if arg1 == "readc":
                self.add_function_readc()
            if arg1 == "read":
                self.add_function_read_int()


        elif op == 'RETURN':  # return (optional_value)
            # Retorno de função
            if arg1:  # There is a return value
                self.adicionar_codigo(self._format_line("",
                                                        f"MOV", f"R1, {self._get_p3_operand_syntax(arg1, 'load')}",
                                                        "; Load valor de retorno R1 "), tipo_codigo)
            self.adicionar_codigo(self._format_line("", f"RET", "", "; Returna da subroutina"), tipo_codigo)

        elif op == 'HALT':
            # Termina a execução do programa
            # O P3 não tem uma instrução HALT, definimos 'Fim' como ponto de paragem.
            self.adicionar_codigo(self._format_line(f"; {op.lower()}", "-" * 25), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "BR", "Fim", "; Fim com loop infinito"), tipo_codigo)

        # --------------------------------------------------------------------------------------------------------------
        # Funções Entrada/Saída
        # --------------------------------------------------------------------------------------------------------------
        elif op == 'READ':
            # read(): Lê int ou double.
            self.adicionar_codigo(self._format_line(f"; {op.lower()} {arg1_label}", "", "-" * 25), tipo_codigo)

        elif op == 'READC':
            # readc(): Lê caracter (retorna valor ASCII).
            self.adicionar_codigo(self._format_line(f"; {op.lower()} {arg1_label}", "", "-" * 25), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "PUSH", "R0", "; Reserva espaço para retorno"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "CALL", f"{op.upper()}", "; Chama a rotina"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "POP", f"M[{arg1_label}]", "; Atribui o valor à variável"), tipo_codigo)
            self.adicionar_codigo("", tipo_codigo)
            self.add_function_readc()

        elif op == 'READS':
            # reads(): Lê string para vetor de int (termina em 0).
            self.adicionar_codigo(self._format_line(f"; {op.lower()} {arg1_label}", "", "-" * 25), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "PUSH", "R0", "; Endereço da variável"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "CALL", f"{op.upper()}", "; Chama a rotina"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "POP", "R0", "; Limpa a pilha"), tipo_codigo)
            self.adicionar_codigo("", tipo_codigo)
            self.add_function_reads()

        elif op in ('WRITE', 'WRITEC'):
            self.adicionar_codigo(self._format_line(f"; {op.lower()} {arg1_label}", "", "-" * 25), tipo_codigo)
            self.adicionar_codigo(
                self._format_line("", "PUSH", f"{arg1_label}", "; Endereço do valor passado via pilha"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "CALL", f"{op.upper()}", "; Chama a rotina"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "POP", "R0", "; Limpa a pilha"), tipo_codigo)
            self.adicionar_codigo("", tipo_codigo)
            if op == 'WRITE':
                # write(x): Imprime valor de variável.
                self.add_function_write()
            else:
                # writec(x): Imprime caracter (ASCII).
                self.add_function_writec()

        elif op == 'WRITEV':
            # writev(vetor): Imprime vetor no formato {48, 49, 0}.
            self.adicionar_codigo(self._format_line(f"; {op.lower()} {arg1_label}", "", "-" * 25), tipo_codigo)
            self.adicionar_codigo(
                self._format_line("", "PUSH", f"{arg1_label}", "; Endereço do valor passado via pilha"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "CALL", f"{op.upper()}", "; Chama a rotina"), tipo_codigo)
            self.adicionar_codigo(self._format_line("", "POP", "R0"), tipo_codigo)
            self.adicionar_codigo("", tipo_codigo)
            self.add_function_writev()

        elif op in ('WRITES',):
            # writes "string_literal"
            str_label = self.string_literal_map.get(arg1.strip('"'))
            if str_label:
                self.adicionar_codigo(self._format_line(f"; {op.lower()} {str_label}", "", "-" * 25), tipo_codigo)
                self.adicionar_codigo(
                    self._format_line("", "PUSH", f"{str_label}", "; Endereço da string passado via pilha"),
                    tipo_codigo)
                self.adicionar_codigo(self._format_line("", "CALL", f"{op.upper()}", "; Chama a rotina"), tipo_codigo)
                self.adicionar_codigo(self._format_line("", "POP", "R0"), tipo_codigo)
                self.adicionar_codigo("", tipo_codigo)
                self.add_function_writes()
            else:
                self.adicionar_codigo(
                    self._format_line("", f"; ERROR: String literal para writes não encontrado: {arg1}"), tipo_codigo)

        else:
            # Caso não exista tradução, insere comentário de aviso
            self.adicionar_codigo(f";; AVISO: Operação TAC '{op}' não traduzida para P3.", tipo_codigo)

    #-------------------------------------------------------------------------------------------------------------------
    # Definição de funções Entrada/Saída
    #-------------------------------------------------------------------------------------------------------------------
    def add_function_read(self):
        if 'read' not in self.declared_functions:
            self.declared_functions.add('read')
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append("; ----- Função read(): Lê int ou double.")
            self.assemblyfunction_code.append(self._format_line("READ:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("READ_END:", "RET"))

    def add_function_readc(self):
        if 'readc' not in self.declared_functions:
            self.declared_functions.add('readc')
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append("; ----- Função readc(): Lê caracter (retorna valor ASCII).")
            self.assemblyfunction_code.append(self._format_line("READC:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("", "; Guarda os registos usados na função"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH","R1"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH","R2"))
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append(self._format_line("READC_WAIT:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("", "MOV","R2, M[CTRL_PORT]","; Verifica se há tecla disponível"))
            self.assemblyfunction_code.append(self._format_line("", "CMP","R2, R0"))
            self.assemblyfunction_code.append(self._format_line("", "BR.Z","READC_WAIT","; Espera enquanto não houver tecla"))
            self.assemblyfunction_code.append(self._format_line("", "MOV","R1, M[IN_PORT]","; Lê o carácter"))
            self.assemblyfunction_code.append(self._format_line("", "MOV","M[SP+4], R1","; Escreve o valor de retorno no espaço do stack"))
            self.assemblyfunction_code.append(self._format_line("", "; Restaura os registos usados na função"))
            self.assemblyfunction_code.append(self._format_line("", "POP","R2"))
            self.assemblyfunction_code.append(self._format_line("", "POP","R1"))
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append(self._format_line("READC_END:", "RET"))

    def add_function_read_int(self):
        if 'read_int' not in self.declared_functions:
            self.declared_functions.add('read_int')
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append("; READ: Le inteiro da consola.")
            self.assemblyfunction_code.append("; Return o inteiro em R1.")
            self.assemblyfunction_code.append(self._format_line("READ:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R1","; Guarda os registos usados na função"))
            self.assemblyfunction_code.append(
                self._format_line("", "PUSH", "R2", "; Guarda os registos usados na função"))
            self.assemblyfunction_code.append(
                self._format_line(";", "PUSH", "R3", "; Guarda os registos usados na função"))
            self.assemblyfunction_code.append(
                self._format_line(";", "PUSH", "R4", "; Guarda os registos usados na função"))
            self.assemblyfunction_code.append(
                self._format_line(";", "PUSH", "R5", "; Guarda os registos usados na função"))
            self.assemblyfunction_code.append(
                self._format_line(";", "PUSH", "R6", "; Guarda os registos usados na função"))
            self.assemblyfunction_code.append(
                self._format_line(";", "PUSH", "R7", "; Guarda os registos usados na função"))
            self.assemblyfunction_code.append(
                self._format_line("", "MOV", "R4, 0", "; armazena numero"))
            self.assemblyfunction_code.append(
                self._format_line("", "MOV", "R7, 1", "; armazena sinal (1 positivo, -1 negativo)"))
            self.assemblyfunction_code.append(self._format_line("READ_WAIT:", "NOP"))
            self.assemblyfunction_code.append(
                self._format_line("", "MOV", "R2, M[CTRL_PORT]", "; Verifica se há tecla disponível"))
            self.assemblyfunction_code.append(
                self._format_line("", "CMP", "R2, R0", ""))
            self.assemblyfunction_code.append(
                self._format_line("", "BR.Z", "READ_WAIT", "; Espera enquanto não houver tecla"))
            self.assemblyfunction_code.append(
                self._format_line("", "MOV", "R1, M[IN_PORT]", "; Lê o carácter para R1 "))
            self.assemblyfunction_code.append(
                self._format_line("", "CMP", "R1, '-'", "; verifica se é sinal"))
            self.assemblyfunction_code.append(
                self._format_line("", "JMP.NZ", "READ_CONT", "; Nao e '-', continua"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R7, -1","; armazena sinal (-1 negativo) "))
            self.assemblyfunction_code.append(self._format_line("READ_CONT:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("", ";CMP", "R1, LINEFEED", "; verifica se foi o enter "))
            self.assemblyfunction_code.append(self._format_line("", ";BR.Z", "READ_RET", "; label muito longe!!! "))
            self.assemblyfunction_code.append(self._format_line("", "; verificar se é um número entre 0 e 9", "", ""))
            self.assemblyfunction_code.append(
                self._format_line("", "MOV", "R2, 30h", "; Load ASCII '0'- 30 dec - 1Eh"))
            self.assemblyfunction_code.append(
                self._format_line("", "CMP", "R1, R2", "; Compara R2 ('0') with R1 (char)"))
            self.assemblyfunction_code.append(
                self._format_line("", "BR.N", "READ_WAIT", "; se menor '0', le novamente "))
            self.assemblyfunction_code.append(
                self._format_line("", "MOV", "R2, 39h", "; Load ASCII '9' - 39 dec - 27h"))
            self.assemblyfunction_code.append(
                self._format_line("", "CMP", "R2, R1", "; Compara R1 (char) with R2 ('9')"))
            self.assemblyfunction_code.append(
                self._format_line("", "BR.N", "READ_WAIT", "; se maior '9', le novamente "))
            self.assemblyfunction_code.append(
                self._format_line("", "MOV", "R2, 30h", "; Load ASCII '0'"))
            self.assemblyfunction_code.append(self._format_line("", "; R4 contém o número a ser multiplicado por 10", "", ""))

            self.assemblyfunction_code.append(
                self._format_line("", "SUB", "R1, R2", "; R1 tem o valor inteiro digitado"))
            self.assemblyfunction_code.append(
                self._format_line("", "MOV", "R5, R4", "; Copia o valor original para R5 (será X * 2)"))

            self.assemblyfunction_code.append(
                self._format_line("", "SHL", "R5, 1", "; R5 = R5 * 2 (desloca R5 1 bit para a esquerda)"))
            self.assemblyfunction_code.append(
                self._format_line("", "MOV", "R6, R4", "; Copia o valor original para R6 (será X * 8)"))
            self.assemblyfunction_code.append(
                self._format_line("", "SHL", "R6, 3", "; R6 = R6 * 8 (desloca R6 3 bits para a esquerda)"))
            self.assemblyfunction_code.append(
                self._format_line("", "ADD", "R5, R6", "; R5 = (X * 2) + (X * 8) = X * 10"))
            self.assemblyfunction_code.append(
                self._format_line("", "; O resultado da multiplicação por 10 está agora em R5", "", ""))
            self.assemblyfunction_code.append(
                self._format_line("", "MOV", "R4, R1", "; Armazena em R4 numero digitado"))
            self.assemblyfunction_code.append(
                self._format_line("", "ADD", "R4, R5", "; Adiciona R4 com R5 (numero anterior *10)"))
            self.assemblyfunction_code.append(
                self._format_line("", "MOV", "R5, 0", "; Reset R5"))
            self.assemblyfunction_code.append(
                self._format_line("", "MOV", "R6, 0", "; Reset R6"))
            self.assemblyfunction_code.append(
                self._format_line("READ_NEXT:", "MOV", "R2, M[CTRL_PORT]", "; Verifica se há tecla disponível"))
            self.assemblyfunction_code.append(
                self._format_line("", "CMP", "R2, R0", ""))
            self.assemblyfunction_code.append(
                self._format_line("", "BR.Z", "READ_NEXT", "; Espera enquanto não houver tecla"))
            self.assemblyfunction_code.append(
                self._format_line("", "MOV", "R1, M[IN_PORT]", "; Lê o carácter para R1 "))
            self.assemblyfunction_code.append(
                self._format_line("", "CMP", "R1, LINEFEED", "; verifica se foi o enter "))
            self.assemblyfunction_code.append(self._format_line("", "BR.Z", "READ_RET", "; termina "))
            self.assemblyfunction_code.append(self._format_line("", "JMP", "READ_CONT", "; le outro numero "))
            self.assemblyfunction_code.append(
                self._format_line("READ_RET:", "NOP", "", ""))
            self.assemblyfunction_code.append(
                self._format_line("", "CMP", "R7, 0", "; Se negativo o numero e negativo"))
            self.assemblyfunction_code.append(
                self._format_line("", "JMP.NN", "READ1_END", "; Jump positivo"))
            self.assemblyfunction_code.append(
                self._format_line("", "NEG", "R4", "; Negamos o numero"))
            self.assemblyfunction_code.append(
                self._format_line("READ1_END:", "MOV", "R1, R4", "; Colocamos em R1 o numero"))
            self.assemblyfunction_code.append(
                self._format_line("", "MOV", "M[SP+4], R1", "; Escreve o valor de retorno no espaço do stack"))
            self.assemblyfunction_code.append(
                self._format_line("", "; Restaura os registos usados na função", "", ""))
            self.assemblyfunction_code.append(self._format_line(";", "POP", "R7",""))
            self.assemblyfunction_code.append(
                self._format_line(";", "POP", "R6", ""))
            self.assemblyfunction_code.append(
                self._format_line(";", "POP", "R5", ""))
            self.assemblyfunction_code.append(
                self._format_line(";", "POP", "R4", ""))
            self.assemblyfunction_code.append(
                self._format_line(";", "POP", "R3", ""))
            self.assemblyfunction_code.append(
                self._format_line("", "POP", "R2", ""))
            self.assemblyfunction_code.append(
                self._format_line("", "POP", "R1", ""))
            self.assemblyfunction_code.append(
                self._format_line("READ_END:", "RET", "", ""))

    def add_function_reads(self):
        if 'reads' not in self.declared_functions:
            self.declared_functions.add('reads')
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append("; ----- Função reads(): Lê string para vetor (termina em 0)")
            self.assemblyfunction_code.append(self._format_line("READS:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("", "; Guarda os registos usados na função"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R1"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R2"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R3"))
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R1, M[SP+5]", "; Ponteiro da variável de retorno"))
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
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append(self._format_line("", "; Restaura registos pela ordem inversa"))
            self.assemblyfunction_code.append(self._format_line("", "POP", "R3"))
            self.assemblyfunction_code.append(self._format_line("", "POP", "R2"))
            self.assemblyfunction_code.append(self._format_line("", "POP", "R1"))
            self.assemblyfunction_code.append(self._format_line("READS_END:", "RET"))

    def add_function_write(self):
        if 'write' not in self.declared_functions:
            self.declared_functions.add('write')
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append("; ----- Função write(x): Imprime valor de variável.")
            self.assemblyfunction_code.append(self._format_line("WRITE:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("", "; Guarda os registos usados na função"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R1"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R2"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R3"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R4"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R6"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R7"))
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R1, M[SP+8]","; R1 = valor a imprimir"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R1, M[R1]", "; R1 = valor a imprimir"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R0, 0", "; Tratamento de números negativos"))
            self.assemblyfunction_code.append(self._format_line("", "CMP", "R1, R0", "; Compara o número com zero"))
            self.assemblyfunction_code.append(self._format_line("", "BR.NN", "WRITE_POSITIVE", "; Se R1 for Não Negativo (>= 0), salta para imprimir."))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R2, '-'", "; Sinal negativo para imprimir."))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "M[OUT_PORT], R2", "; Se R1 for negativo, imprime o sinal de menos"))
            self.assemblyfunction_code.append(self._format_line("", "NEG", "R1", "; Converte R1 para seu valor absoluto (positivo)"))
            self.assemblyfunction_code.append(self._format_line("WRITE_POSITIVE:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R7, 10000","; Divisor inicial (10^4)"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R6, R0","; Flag: dígito já impresso (0 = ainda não)"))
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append(self._format_line("WRITE_L1:", "MOV", "R2, R1", "; R2 = valor atual"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R3, R7", "; R3 = divisor"))
            self.assemblyfunction_code.append(self._format_line("", "DIV", "R2, R3", "; R2 = quociente (dígito), R3 = resto"))
            self.assemblyfunction_code.append(self._format_line("", "CMP", "R6, R0", "; Já imprimimos algum dígito?"))
            self.assemblyfunction_code.append(self._format_line("", "BR.NZ", "WRITE_L2", "; Se sim, imprime sempre"))
            self.assemblyfunction_code.append(self._format_line("", "CMP", "R2, R0"))
            self.assemblyfunction_code.append(self._format_line("", "BR.Z", "WRITE_L3", "; Se dígito é 0 e nada impresso, salta"))
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append(self._format_line("WRITE_L2:", "ADD", "R2, 48", "; Converte para ASCII"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "M[OUT_PORT], R2", "; Escreve dígito"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R6, 1", "; Marca que começámos a imprimir"))
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append(self._format_line("WRITE_L3:", "MOV", "R1, R3", "; Atualiza valor com o resto"))
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
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append(self._format_line("", "; Restaura registos pela ordem inversa"))
            self.assemblyfunction_code.append(self._format_line("", "POP", "R7"))
            self.assemblyfunction_code.append(self._format_line("", "POP", "R6"))
            self.assemblyfunction_code.append(self._format_line("", "POP", "R4"))
            self.assemblyfunction_code.append(self._format_line("", "POP", "R3"))
            self.assemblyfunction_code.append(self._format_line("", "POP", "R2"))
            self.assemblyfunction_code.append(self._format_line("", "POP", "R1"))
            self.assemblyfunction_code.append(self._format_line("WRITE_END:", "RET"))

    def add_function_write_(self):
        if 'write' not in self.declared_functions:
            self.declared_functions.add('write')
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append("; ----- Função write(x): Imprime valor de variável.")
            self.assemblyfunction_code.append(self._format_line("WRITE:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("", "; Guarda os registos usados na função"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R1"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R2"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R3"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R4"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R6"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH", "R7"))
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R1, M[SP+8]", "; R1 = valor a imprimir"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R1, M[R1]", "; R1 = valor a imprimir"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R7, 10000", "; Divisor inicial (10^4)"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R6, R0", "; Flag: dígito já impresso (0 = ainda não)"))
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append(self._format_line("WRITE_L1:", "MOV", "R2, R1", "; R2 = valor atual"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R3, R7", "; R3 = divisor"))
            self.assemblyfunction_code.append(self._format_line("", "DIV", "R2, R3", "; R2 = quociente (dígito), R3 = resto"))
            self.assemblyfunction_code.append(self._format_line("", "CMP", "R6, R0", "; Já imprimimos algum dígito?"))
            self.assemblyfunction_code.append(self._format_line("", "BR.NZ", "WRITE_L2", "; Se sim, imprime sempre"))
            self.assemblyfunction_code.append(self._format_line("", "CMP", "R2, R0"))
            self.assemblyfunction_code.append(self._format_line("", "BR.Z", "WRITE_L3", "; Se dígito é 0 e nada impresso, salta"))
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append(self._format_line("WRITE_L2:", "ADD", "R2, 48", "; Converte para ASCII"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "M[OUT_PORT], R2", "; Escreve dígito"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R6, 1", "; Marca que começámos a imprimir"))
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append(self._format_line("WRITE_L3:", "MOV", "R1, R3", "; Atualiza valor com o resto"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R4, 10"))
            self.assemblyfunction_code.append(self._format_line("", "DIV", "R7, R4", "; R7 = R7 / 10 (próximo divisor)"))
            self.assemblyfunction_code.append(self._format_line("", "CMP", "R7, R0"))
            self.assemblyfunction_code.append(self._format_line("", "BR.NZ", "WRITE_L1"))
            self.assemblyfunction_code.append(self._format_line("", "; Caso número seja 0 imprime '0'"))
            self.assemblyfunction_code.append(self._format_line("", "CMP", "R6, R0"))
            self.assemblyfunction_code.append(self._format_line("", "BR.NZ", "WRITE_LF"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R1, '0'"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "M[OUT_PORT], R1"))
            self.assemblyfunction_code.append(self._format_line("WRITE_LF:", "MOV", "R2, LINEFEED", "; Muda de linha"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "M[OUT_PORT], R2"))
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append(self._format_line("", "; Restaura registos pela ordem inversa"))
            self.assemblyfunction_code.append(self._format_line("", "POP", "R7"))
            self.assemblyfunction_code.append(self._format_line("", "POP", "R6"))
            self.assemblyfunction_code.append(self._format_line("", "POP", "R4"))
            self.assemblyfunction_code.append(self._format_line("", "POP", "R3"))
            self.assemblyfunction_code.append(self._format_line("", "POP", "R2"))
            self.assemblyfunction_code.append(self._format_line("", "POP", "R1"))
            self.assemblyfunction_code.append(self._format_line("WRITE_END:", "RET"))

    def add_function_writec(self):
        if 'writec' not in self.declared_functions:
            self.declared_functions.add('writec')
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append("; ----- Função writec(x): Imprime caracter (ASCII).")
            self.assemblyfunction_code.append(self._format_line("WRITEC:", "NOP", "","; escreve um carater na consola"))
            self.assemblyfunction_code.append(self._format_line("", "; Guarda os registos usados na função"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH","R1"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH","R2"))
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R1, M[SP+4]","; Endereço da string passado via pilha"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R2, M[R1]","; Lê o carater apontado por R1"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "M[FFFEh], R2","; Escreve o carater no endereço de saída"))
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append(self._format_line("", "; Restaura registos pela ordem inversa"))
            self.assemblyfunction_code.append(self._format_line("", "POP","R2"))
            self.assemblyfunction_code.append(self._format_line("", "POP","R1"))
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
            self.assemblyfunction_code.append(self._format_line("WRITES:", "NOP"))
            self.assemblyfunction_code.append(self._format_line("", "; Guarda os registos usados na função"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH","R1"))
            self.assemblyfunction_code.append(self._format_line("", "PUSH","R2"))
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append(self._format_line("", "MOV", "R1, M[SP+4]","; Endereço da string passado via pilha"))
            self.assemblyfunction_code.append(self._format_line("WRITES_L1:", "MOV", "R2, M[R1]","; Lê o carater apontado por R1"))
            self.assemblyfunction_code.append(self._format_line("", "CMP", "R2, R0","; Compara com o terminador"))
            self.assemblyfunction_code.append(self._format_line("", "JMP.Z", "WRITES_LF","; Se for zero, salta para o fim"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "M[OUT_PORT], R2","; Escreve o carater no endereço de saída"))
            self.assemblyfunction_code.append(self._format_line("", "INC", "R1","; Avança para o próximo carater"))
            self.assemblyfunction_code.append(self._format_line("", "JMP", "WRITES_L1","; Repete o ciclo"))
            self.assemblyfunction_code.append(self._format_line("WRITES_LF:", "MOV", "R2, LINEFEED","; Muda de linha"))
            self.assemblyfunction_code.append(self._format_line("", "MOV", "M[OUT_PORT], R2"))
            self.assemblyfunction_code.append("")
            self.assemblyfunction_code.append(self._format_line("", "; Restaura registos pela ordem inversa"))
            self.assemblyfunction_code.append(self._format_line("", "POP","R2"))
            self.assemblyfunction_code.append(self._format_line("", "POP","R1"))
            self.assemblyfunction_code.append(self._format_line("WRITES_END:", "RET"))

    # -------------------------------------------------------------------------------------------------------------------

    def generate_from_tac_list(self, tac_list):
        """
        Gera o código Assembly P3 completo a partir de uma lista de instruções TAC.
        Retorna o código como uma string pronta a ser escrita num ficheiro .as.
        """
        self.assembly_code = []
        self.assemblyfunction_code = []
        self.assemblyfunction_codetemp  = []
        tipo_codigo='funcao'# 'geral'ou 'funcao' - é geral quando encontra o main, antes é funcao
        # traduz instruções TAC para assembly
        for indice, instr in enumerate(tac_list):
            quad_num = indice + 1
            if ((instr['op'] == 'label') and (instr['res'] == 'main')):
                tipo_codigo = 'geral'
            self.translate_tac_instruction(instr, quad_num, tipo_codigo)

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
        output.extend(self.assemblyfunction_codetemp)
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
