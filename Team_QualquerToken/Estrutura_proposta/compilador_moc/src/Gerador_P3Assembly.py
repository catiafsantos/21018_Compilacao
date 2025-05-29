import copy


class Gerador_P3Assembly:
    def __init__(self):
        self.assembly_lines = []
        self.data_declarations = []
        self.variable_locations = {}
        self.label_counter = 0
        self.program_entry_point = "_start"  # Pode ser 'main' se o seu TAC sempre começar com label 'main'
        self.temp_registers = ["R1", "R2", "R3"]
        self.current_temp_reg_idx = 0

    def _get_temp_register(self):
        reg = self.temp_registers[self.current_temp_reg_idx]
        self.current_temp_reg_idx = (self.current_temp_reg_idx + 1) % len(self.temp_registers)
        return reg

    def _get_variable_p3_label(self, tac_var_name_or_const):
        if tac_var_name_or_const is None:
            return None
        # Se for um número (constante imediata), retorna como string
        if isinstance(tac_var_name_or_const, (int, float)):
            return str(tac_var_name_or_const)

        # Se não for uma string (nome de variável/label), não faz nada
        if not isinstance(tac_var_name_or_const, str):
            return None  # Ou levantar um erro se esperado ser sempre string ou None

        # Limpeza do nome para ser uma etiqueta P3 válida
        clean_var_name = tac_var_name_or_const.replace('$', 't_')

        if clean_var_name not in self.variable_locations:
            p3_label = f"Var_{clean_var_name}"
            self.variable_locations[clean_var_name] = p3_label
            self.data_declarations.append(f"{p3_label}: WORD 0    ; Variável/Temporária {tac_var_name_or_const}")
        return self.variable_locations[clean_var_name]

    def _generate_p3_label(self, tac_label_name):
        # Labels TAC já vêm como strings, e.g., 'L0', 'main'
        # Apenas retornamos, a sintaxe P3 para label é 'NomeLabel:'
        return str(tac_label_name)

    def translate_tac_instruction(self, tac_instr_dict):
        # Acessar campos usando chaves de dicionário e .get() para segurança
        op = tac_instr_dict.get('op')
        arg1_val = tac_instr_dict.get('arg1')  # Valor original do TAC (pode ser int, str, None)
        arg2_val = tac_instr_dict.get('arg2')
        res_val = tac_instr_dict.get('res')  # Chave 'res' para o resultado/destino

        # Obter representações P3 (etiquetas de memória ou strings de constantes)
        # _get_variable_p3_label lida com constantes e alocação de variáveis
        arg1_p3 = self._get_variable_p3_label(arg1_val)
        arg2_p3 = self._get_variable_p3_label(arg2_val)
        res_p3 = self._get_variable_p3_label(res_val)

        reg1 = "R1"
        reg2 = "R2"
        # R0 é sempre 0 em P3

        # Construir uma representação textual do TAC para comentários
        tac_comment_arg1 = f"{arg1_val}" if arg1_val is not None else ""
        tac_comment_arg2 = f", {arg2_val}" if arg2_val is not None else ""
        tac_comment_res = f"{res_val}" if res_val is not None else ""
        if op in ['ASSIGN', 'ASSIGN_CONST', 'ASSIGN_VAR', 'NEG', 'POP']:  # Operações com 'res = arg1' ou 'res = OP arg1'
            self.assembly_lines.append(f"; TAC: {op} {tac_comment_res}, {tac_comment_arg1}")
        elif op in ['LABEL', 'GOTO', 'PUSH', 'RETURN', 'PARAM']:  # Operações com 'res' ou 'arg1' principal
            self.assembly_lines.append(f"; TAC: {op} {tac_comment_res or tac_comment_arg1}")
        else:  # Operações com 'res = arg1 op arg2' ou 'IF cond GOTO label'
            self.assembly_lines.append(f"; TAC: {op} {tac_comment_res}, {tac_comment_arg1}{tac_comment_arg2}")

        if op == 'ASSIGN_CONST' or op == '(double)' or op == '=' and isinstance(arg1_val, (int, float)):
            # No seu TAC: {'op': '(double)', 'arg1': 10, 'res': 't4'}
            # ou {'op': '=', 'arg1': 0, 'res': 'total'} (arg1 é int)
            # P3: MOV R1, const_val; MOV M[addr_result], R1
            const_val_for_mov = arg1_val  # Já é o número
            self.assembly_lines.append(
                f"    MOV {reg1}, {const_val_for_mov}     ; {reg1} = {const_val_for_mov} (constante)")
            self.assembly_lines.append(f"    MOV {res_p3}, {reg1}   ; {res_val} = {reg1}")

        elif op == '=':  # Atribuição de variável, e.g. {'op': '=', 'arg1': 't11', 'res': 'total'}
            # P3: MOV R1, M[addr_arg1]; MOV M[addr_result], R1
            self.assembly_lines.append(f"    MOV {reg1}, {arg1_p3}     ; {reg1} = {arg1_val}")
            self.assembly_lines.append(f"    MOV {res_p3}, {reg1}   ; {res_val} = {reg1}")

        elif op in ['ADD', 'SUB', 'AND', 'OR', 'XOR', '+',
                    '-']:  # {'op': '+', 'arg1': 'total', 'arg2': 't10', 'res': 't11'}
            # P3_OP pode ser o próprio 'op' se os nomes coincidirem, ajuste se necessário.
            p3_op_str = op
            if op == '+': p3_op_str = 'ADD'
            if op == '-': p3_op_str = 'SUB'
            # ... outros mapeamentos se o nome do 'op' do TAC não for o mnemónico P3

            self.assembly_lines.append(f"    MOV {reg1}, {arg1_p3}     ; {reg1} = {arg1_val}")
            self.assembly_lines.append(f"    MOV {reg2}, {arg2_p3}     ; {reg2} = {arg2_val}")
            self.assembly_lines.append(
                f"    {p3_op_str.upper()} {reg1}, {reg2}        ; {reg1} = {reg1} {p3_op_str} {reg2}")
            self.assembly_lines.append(f"    MOV {res_p3}, {reg1}   ; {res_val} = {reg1}")

        elif op == 'MUL' or op == 'DIV':
            self.assembly_lines.append(f"    MOV {reg1}, {arg1_p3}     ; {reg1} (op1) = {arg1_val}")
            self.assembly_lines.append(f"    MOV {reg2}, {arg2_p3}     ; {reg2} (op2) = {arg2_val}")
            self.assembly_lines.append(f"    {op.upper()} {reg1}, {reg2}        ; {op.upper()} {reg1}, {reg2}")
            if op == 'MUL':
                self.assembly_lines.append(f"    MOV {res_p3}, {reg2}   ; {res_val} = LSB do resultado (de {reg2})")
            elif op == 'DIV':
                self.assembly_lines.append(f"    MOV {res_p3}, {reg1}   ; {res_val} = Quociente (de {reg1})")

        elif op == 'label':  # {'op': 'label', 'res': 'main'}
            # O 'res' do TAC é o nome do label
            self.assembly_lines.append(f"{self._generate_p3_label(res_val)}:")

        elif op == 'goto':  # {'op': 'goto', 'res': 'L1'}
            # O 'res' do TAC é o label de destino
            self.assembly_lines.append(f"    JMP {self._generate_p3_label(res_val)}")

        elif op == 'IF_FALSE_GOTO':  # (Exemplo: IF_FALSE cond_var GOTO L_target)
            # No seu TAC: {'op': 'IF_FALSE_GOTO', 'arg1': 'cond_var', 'res': 'L_target'}
            # CMP reg_cond, R0 (R0 é sempre 0)
            # JMP.Z L_target
            self.assembly_lines.append(f"    MOV {reg1}, {arg1_p3}     ; {reg1} = {arg1_val} (condição)")
            self.assembly_lines.append(f"    CMP {reg1}, R0            ; Compara {reg1} com 0 (R0)")
            self.assembly_lines.append(f"    JMP.Z {self._generate_p3_label(res_val)}  ; Salta se Zero (condição == 0)")

        # Seu TAC tem 'alloc' e '[]=', '[]'. Estes são para arrays/vetores.
        # P3 não tem suporte direto a arrays complexos, você os simularia com memória.
        # 'alloc v, 3' -> Reservar 3 palavras para 'v'.
        # 'v[0] = 1' -> Calcular endereço de v + (0 * tamanho_elemento) e mover 1 para lá.
        # 't10 = v[t9]' -> Calcular endereço de v + (t9 * tamanho_elemento) e carregar.
        # Precisamos de um tamanho de elemento (assumindo 1 palavra P3 = 16 bits = 2 bytes se endereçamento por byte,
        # mas P3 endereça por palavra, então offset é direto).

        elif op == 'alloc':  # {'op': 'alloc', 'arg1': 'v', 'arg2': '3', 'res': None}
            # arg1 é o nome do array, arg2 é o número de elementos (palavras P3)
            array_label = self._get_variable_p3_label(arg1_val)  # Registra a etiqueta base do array
            num_elements = int(arg2_val)
            # A declaração efetiva com TAB será feita na montagem final da string
            # Aqui, apenas garantimos que a etiqueta base existe.
            # Se você já tiver adicionado com WORD 0, TAB sobrescreveria ou precisaria de lógica
            # para usar TAB em vez de WORD para arrays.
            # Vamos ajustar _get_variable_p3_label para não adicionar declaração se for alloc
            # ou modificar a declaração existente para TAB.
            # Por agora, a declaração de dados para 'array_label' já foi feita como 'WORD 0'.
            # Precisamos de uma maneira de dizer que é um array e qual o seu tamanho.
            # Uma forma simples é usar TAB na seção de dados:
            # Remover a declaração WORD anterior e adicionar TAB
            if f"{array_label}: WORD 0    ; Variável/Temporária {arg1_val}" in self.data_declarations:
                self.data_declarations.remove(f"{array_label}: WORD 0    ; Variável/Temporária {arg1_val}")

            # Adicionar nova declaração com TAB se não existir uma similar
            tab_decl = f"{array_label}: TAB {num_elements}    ; Array {arg1_val} com {num_elements} palavras"
            if tab_decl not in self.data_declarations:
                self.data_declarations.append(tab_decl)
            self.assembly_lines.append(f"    ; alloc {arg1_val}, {num_elements} (espaço reservado com TAB)")

        elif op == '[]=':  # {'op': '[]=', 'arg1': 'v', 'arg2': '0', 'res': '1'}
            # array_name[index] = value_to_store
            # array_name -> arg1_val
            # index -> arg2_val (pode ser constante ou variável TAC)
            # value_to_store -> res_val (pode ser constante ou variável TAC)

            array_base_label = self._get_variable_p3_label(arg1_val)  # e.g., Var_v

            # Carregar valor a ser armazenado para um registrador (reg2)
            if isinstance(res_val, (int, float)):  # Se o valor a ser armazenado é uma constante
                self.assembly_lines.append(
                    f"    MOV {reg2}, {res_val}        ; {reg2} = {res_val} (valor para armazenar)")
            else:  # Se o valor a ser armazenado é uma variável TAC
                val_to_store_p3_loc = self._get_variable_p3_label(res_val)
                self.assembly_lines.append(
                    f"    MOV {reg2}, {val_to_store_p3_loc} ; {reg2} = {res_val} (valor para armazenar)")

            # Calcular endereço: base_addr + index. Usar modo indexado M[Rx + W]
            # Rx terá o índice, W será a etiqueta base.
            # Mas P3 é M[Rx+W], onde W é constante.
            # Se o índice (arg2_val) for uma constante, podemos fazer M[array_base_label + index_constante] se o assembler P3 suportar.
            # O manual P3 especifica M[Rx+W] e M[W]. Para M[Label+offset_constante], o Label é W.
            # Se o índice for variável (t9 no seu exemplo), precisamos carregar o índice para um Rx.
            # MOV R_idx, index_val
            # E depois usar M[R_idx + Label_base] se o assembler suportar Label como W.
            # O modo indexado é M[Rx+W]. Se W é a etiqueta base, Rx é o índice.

            # Carregar índice (arg2_val) para um registrador (reg1)
            if isinstance(arg2_val, (int, float)):  # Índice é constante
                self.assembly_lines.append(f"    MOV {reg1}, {arg2_val}        ; {reg1} = {arg2_val} (índice)")
            else:  # Índice é variável TAC
                index_p3_loc = self._get_variable_p3_label(arg2_val)
                self.assembly_lines.append(f"    MOV {reg1}, {index_p3_loc}    ; {reg1} = {arg2_val} (índice)")

            # Armazenar o valor (em reg2) no endereço indexado
            # P3: MOV M[Rx+W], Ry (onde Rx tem o índice, W é a base, Ry tem o valor)
            # W aqui é a etiqueta base do array.
            # Rx é reg1 (índice). Ry é reg2 (valor).
            self.assembly_lines.append(
                f"    MOV M[{reg1}+{array_base_label}], {reg2} ; {arg1_val}[{arg2_val}] = {res_val}")

        elif op == '[]':  # {'op': '[]', 'arg1': 'v', 'arg2': 't9', 'res': 't10'}
            # result_var = array_name[index]
            # result_var -> res_val
            # array_name -> arg1_val
            # index -> arg2_val
            array_base_label = self._get_variable_p3_label(arg1_val)
            result_p3_loc = self._get_variable_p3_label(res_val)

            # Carregar índice (arg2_val) para um registrador (reg1)
            if isinstance(arg2_val, (int, float)):  # Índice é constante
                self.assembly_lines.append(f"    MOV {reg1}, {arg2_val}        ; {reg1} = {arg2_val} (índice)")
            else:  # Índice é variável TAC
                index_p3_loc = self._get_variable_p3_label(arg2_val)
                self.assembly_lines.append(f"    MOV {reg1}, {index_p3_loc}    ; {reg1} = {arg2_val} (índice)")

            # Carregar valor do endereço indexado (M[Rx+W]) para um registrador (reg2)
            # Rx é reg1 (índice). W é array_base_label.
            self.assembly_lines.append(
                f"    MOV {reg2}, M[{reg1}+{array_base_label}] ; {reg2} = {arg1_val}[{arg2_val}]")
            # Armazenar o valor carregado (em reg2) na variável de resultado
            self.assembly_lines.append(f"    MOV {result_p3_loc}, {reg2} ; {res_val} = {reg2}")
        elif op == 'write':  # Supondo TAC: {'op': 'IO_WRITE_TEXT', 'arg1': <char_var_ou_constante>}
            char_val_tac = tac_instr_dict.get('arg1')

            # _get_variable_p3_label pode retornar a constante diretamente se for numérica
            # ou a etiqueta de memória se for uma variável.
            # Se char_val_tac for um caractere literal como 'A', _get_variable_p3_label precisa ser ajustado
            # ou você trata aqui para obter o valor ASCII ou a representação P3 para char.
            # P3 aceita 'A' como constante (página 7, fonte 82, 87).

            operand_str_p3 = self._get_variable_p3_label(char_val_tac)
            reg_temp = "R1"  # Usar um registrador temporário

            self.assembly_lines.append(f"; TAC: WRITE {char_val_tac}")
            if operand_str_p3.startswith("Var_") or operand_str_p3.startswith("M["):  # Se for uma variável/memória
                self.assembly_lines.append(f"    MOV {reg_temp}, {operand_str_p3}  ; Carrega char para {reg_temp}")
                self.assembly_lines.append(f"    MOV M[FFFEh], {reg_temp}      ; Escreve {reg_temp} em FFFEh")
            else:  # Se for uma constante (incluindo 'A')
                self.assembly_lines.append(
                    f"    MOV {reg_temp}, {operand_str_p3}  ; Carrega char '{operand_str_p3}' para {reg_temp}")
                self.assembly_lines.append(f"    MOV M[FFFEh], {reg_temp}      ; Escreve {reg_temp} em FFFEh")
        else:
            self.assembly_lines.append(f";; AVISO: Operação TAC '{op}' não traduzida para P3.")
        self.assembly_lines.append("")

    def generate_from_tac_list(self, tac_list_of_dicts):
        self.assembly_lines = []
        self.data_declarations = []
        self.variable_locations = {}
        self.label_counter = 0
        self.current_temp_reg_idx = 0

        # Primeira passagem para identificar todas as variáveis e prepará-las para declaração
        for instr_dict in tac_list_of_dicts:
            # Usar .get() para evitar KeyError se a chave não existir (embora 'op' e 'res' devam existir)
            # Para 'alloc', arg1 é o nome do array a ser declarado com TAB.
            # Outras vars/temps serão declaradas com WORD 0 por _get_variable_p3_label
            # se não forem constantes.
            if instr_dict.get('op') == 'alloc':
                array_name = instr_dict.get('arg1')
                num_elements = int(instr_dict.get('arg2', 0))
                if array_name:
                    p3_label = f"Var_{array_name.replace('$', 't_')}"
                    self.variable_locations[
                        array_name.replace('$', 't_')] = p3_label  # Mapeia nome original para etiqueta limpa
                    # Verifica se já existe uma declaração WORD para este array e remove-a
                    word_decl_to_remove = f"{p3_label}: WORD 0    ; Variável/Temporária {array_name}"
                    if word_decl_to_remove in self.data_declarations:
                        self.data_declarations.remove(word_decl_to_remove)
                    # Adiciona declaração TAB
                    tab_decl = f"{p3_label}: TAB {num_elements}    ; Array {array_name} com {num_elements} palavras"
                    if tab_decl not in self.data_declarations:  # Evitar duplicados se 'alloc' for chamado várias vezes
                        self.data_declarations.append(tab_decl)
            else:
                self._get_variable_p3_label(instr_dict.get('res'))
                self._get_variable_p3_label(instr_dict.get('arg1'))
                self._get_variable_p3_label(instr_dict.get('arg2'))

        # Traduzir cada instrução TAC
        for instr_dict in tac_list_of_dicts:
            # Se o 'op' for 'label' e o 'res' for 'main', este pode ser o ponto de entrada.
            if instr_dict.get('op') == 'label' and instr_dict.get('res') == 'main':
                self.program_entry_point = 'main'  # Usa 'main' como _start
            self.translate_tac_instruction(instr_dict)

        # Montar a string final do código assembly
        output_string_list = []
        output_string_list.append(f"ORIG 0                 ; Define origem do programa")
        output_string_list.append("")

        if self.data_declarations:
            output_string_list.append("; === Declarações de Variáveis e Arrays ===")
            # Ordenar para consistência, opcional
            self.data_declarations.sort()
            output_string_list.extend(self.data_declarations)
            output_string_list.append("; =========================================")
            output_string_list.append("")

        # Prólogo com inicialização do SP e ponto de entrada
        output_string_list.append(f"{self.program_entry_point}:")
        output_string_list.append(
            f"    MOV R7, 0xFFFE          ; Carrega endereço inicial da pilha em R7 (ajustar para o topo da memória P3)")
        output_string_list.append(f"    MOV SP, R7              ; Inicializa SP com valor de R7")
        output_string_list.append("")

        output_string_list.extend(self.assembly_lines)  # Corpo principal do programa

        output_string_list.append("")
        output_string_list.append("END_PROGRAM:                ; Rótulo para fim do programa")
        output_string_list.append("    JMP END_PROGRAM         ; Loop infinito para terminar a execução")

        return "\n".join(output_string_list)