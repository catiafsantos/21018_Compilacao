;============== Região de Dados (inicia no endereço 8000h)                
                ORIG    8000h           

STR_LIT_1       STR     'I','n','t','r','o','d','u','z','a',' ','i','n','t','e','i','r','o',':',' ',0; 'Introduza inteiro: '
VAR_1           WORD    0               ; variável 'fact'
VAR_10          WORD    0               ; variável 't2'
VAR_11          WORD    0               ; variável 't3'
VAR_12          WORD    0               ; variável 't4'
VAR_13          WORD    0               ; variável 'main'
VAR_14          WORD    0               ; variável 'Introduza inteiro: '
VAR_15          WORD    0               ; variável 'read'
VAR_16          WORD    0               ; variável 't5'
VAR_17          WORD    0               ; variável 'n'
VAR_18          WORD    0               ; variável 't6'
VAR_19          WORD    0               ; variável 't7'
VAR_2           WORD    0               ; variável 'param1'
VAR_3           WORD    0               ; variável 'k'
VAR_4           WORD    0               ; variável 'param2'
VAR_5           WORD    0               ; variável 'i'
VAR_6           WORD    1               ; 1
VAR_7           WORD    0               ; variável 't1'
VAR_8           WORD    0               ; variável 'L2'
VAR_9           WORD    0               ; variável 'L1'

;-------------- Definições de Constantes de sistema                
SP_ADDRESS      EQU     FDFFh           
CTRL_PORT       EQU     FFFDh           ; Porto de controlo do teclado
IN_PORT         EQU     FFFFh           ; Porto de entrada de texto (teclado)
OUT_PORT        EQU     FFFEh           ; Porto de saída (consola)
LINEFEED        EQU     10              ; Código ASCII da tecla enter na consola (LF)

;============== Região de Código (inicia no endereço 0000h)                
                ORIG    0000h           
                JMP     _start          ; jump to main

;-------------- Rotinas                 

; ----- Função writes("texto"): Imprime string
WRITES:         NOP                     
                ; Guarda os registos usados na função                
                PUSH    R1              
                PUSH    R2              

                MOV     R1, M[SP+4]     ; Endereço da string passado via pilha
WRITES_L1:      MOV     R2, M[R1]       ; Lê o carater apontado por R1
                CMP     R2, R0          ; Compara com o terminador
                JMP.Z   WRITES_LF       ; Se for zero, salta para o fim
                MOV     M[OUT_PORT], R2 ; Escreve o carater no endereço de saída
                INC     R1              ; Avança para o próximo carater
                JMP     WRITES_L1       ; Repete o ciclo
WRITES_LF:      MOV     R2, LINEFEED    ; Muda de linha
                MOV     M[OUT_PORT], R2 
                ; Restaura os registos usados na função                
                POP     R2              
                POP     R1              

WRITES_END:     RET                     

; READ: Le inteiro da consola.
; Return o inteiro em R1.
READ:           NOP                     
                PUSH    R1              ; Guarda os registos usados na função
                PUSH    R2              ; Guarda os registos usados na função
;               PUSH    R3              ; Guarda os registos usados na função
;               PUSH    R4              ; Guarda os registos usados na função
;               PUSH    R5              ; Guarda os registos usados na função
;               PUSH    R6              ; Guarda os registos usados na função
;               PUSH    R7              ; Guarda os registos usados na função
                MOV     R4, 0           ; armazena numero
                MOV     R7, 1           ; armazena sinal (1 positivo, -1 negativo)
READ_WAIT:      NOP                     
                MOV     R2, M[CTRL_PORT]; Verifica se há tecla disponível
                CMP     R2, R0          
                BR.Z    READ_WAIT       ; Espera enquanto não houver tecla
                MOV     R1, M[IN_PORT]  ; Lê o carácter para R1 
                CMP     R1, '-'         ; verifica se é sinal
                JMP.NZ  READ_CONT       ; Nao e '-', continua
                MOV     R7, -1          ; armazena sinal (-1 negativo) 
READ_CONT:      NOP                     
                ;CMP    R1, LINEFEED    ; verifica se foi o enter 
                ;BR.Z   READ_RET        ; label muito longe!!! 
                ; verificar se é um número entre 0 e 9                
                MOV     R2, 30h         ; Load ASCII '0'- 30 dec - 1Eh
                CMP     R1, R2          ; Compara R2 ('0') with R1 (char)
                BR.N    READ_WAIT       ; se menor '0', le novamente 
                MOV     R2, 39h         ; Load ASCII '9' - 39 dec - 27h
                CMP     R2, R1          ; Compara R1 (char) with R2 ('9')
                BR.N    READ_WAIT       ; se maior '9', le novamente 
                MOV     R2, 30h         ; Load ASCII '0'
                ; R4 contém o número a ser multiplicado por 10                
                SUB     R1, R2          ; R1 tem o valor inteiro digitado
                MOV     R5, R4          ; Copia o valor original para R5 (será X * 2)
                SHL     R5, 1           ; R5 = R5 * 2 (desloca R5 1 bit para a esquerda)
                MOV     R6, R4          ; Copia o valor original para R6 (será X * 8)
                SHL     R6, 3           ; R6 = R6 * 8 (desloca R6 3 bits para a esquerda)
                ADD     R5, R6          ; R5 = (X * 2) + (X * 8) = X * 10
                ; O resultado da multiplicação por 10 está agora em R5                
                MOV     R4, R1          ; Armazena em R4 numero digitado
                ADD     R4, R5          ; Adiciona R4 com R5 (numero anterior *10)
                MOV     R5, 0           ; Reset R5
                MOV     R6, 0           ; Reset R6
READ_NEXT:      MOV     R2, M[CTRL_PORT]; Verifica se há tecla disponível
                CMP     R2, R0          
                BR.Z    READ_NEXT       ; Espera enquanto não houver tecla
                MOV     R1, M[IN_PORT]  ; Lê o carácter para R1 
                CMP     R1, LINEFEED    ; verifica se foi o enter 
                BR.Z    READ_RET        ; termina 
                JMP     READ_CONT       ; le outro numero 
READ_RET:       NOP                     
                CMP     R7, 0           ; Se negativo o numero e negativo
                JMP.NN  READ1_END       ; Jump positivo
                NEG     R4              ; Negamos o numero
READ1_END:      MOV     R1, R4          ; Colocamos em R1 o numero
                MOV     M[SP+4], R1     ; Escreve o valor de retorno no espaço do stack
                ; Restaura os registos usados na função                
;               POP     R7              
;               POP     R6              
;               POP     R5              
;               POP     R4              
;               POP     R3              
                POP     R2              
                POP     R1              
READ_END:       RET                     

; ----- Função write(x): Imprime valor de variável.
WRITE:          NOP                     
                ; Guarda os registos usados na função                
                PUSH    R1              
                PUSH    R2              
                PUSH    R3              
                PUSH    R4              
                PUSH    R6              
                PUSH    R7              

                MOV     R1, M[SP+8]     ; R1 = valor a imprimir
                MOV     R1, M[R1]       ; R1 = valor a imprimir
                MOV     R0, 0           ; Tratamento de números negativos
                CMP     R1, R0          ; Compara o número com zero
                BR.NN   WRITE_POSITIVE  ; Se R1 for Não Negativo (>= 0), salta para imprimir.
                MOV     R2, '-'         ; Sinal negativo para imprimir.
                MOV     M[OUT_PORT], R2 ; Se R1 for negativo, imprime o sinal de menos
                NEG     R1              ; Converte R1 para seu valor absoluto (positivo)
WRITE_POSITIVE: NOP                     
                MOV     R7, 10000       ; Divisor inicial (10^4)
                MOV     R6, R0          ; Flag: dígito já impresso (0 = ainda não)

WRITE_L1:       MOV     R2, R1          ; R2 = valor atual
                MOV     R3, R7          ; R3 = divisor
                DIV     R2, R3          ; R2 = quociente (dígito), R3 = resto
                CMP     R6, R0          ; Já imprimimos algum dígito?
                BR.NZ   WRITE_L2        ; Se sim, imprime sempre
                CMP     R2, R0          
                BR.Z    WRITE_L3        ; Se dígito é 0 e nada impresso, salta

WRITE_L2:       ADD     R2, 48          ; Converte para ASCII
                MOV     M[OUT_PORT], R2 ; Escreve dígito
                MOV     R6, 1           ; Marca que começámos a imprimir

WRITE_L3:       MOV     R1, R3          ; Atualiza valor com o resto
                MOV     R4, 10          
                DIV     R7, R4          ; R7 = R7 / 10 (próximo divisor)
                CMP     R7, R0          
                BR.NZ   WRITE_L1        
                ; Caso número seja 0 imprime '0'                
                CMP     R6, R0          
                BR.NZ   WRITE_LF        
                MOV     R1, '0'         
                MOV     M[OUT_PORT], R1 
WRITE_LF:       MOV     R2, LINEFEED    ; Muda de linha
                MOV     M[OUT_PORT], R2 
                ; Restaura os registos usados na função                
                POP     R7              
                POP     R6              
                POP     R4              
                POP     R3              
                POP     R2              
                POP     R1              

WRITE_END:      RET                     

;-------------- Programa Principal                 
_start:         NOP                     
                MOV     R7, SP_ADDRESS  
                MOV     SP, R7          ; Define o Stack Pointer

fact:           NOP                     
                MOV     R1, M[VAR_2]    
                MOV     M[VAR_3], R1    
                MOV     R1, M[VAR_4]    
                MOV     M[VAR_5], R1    
                MOV     R1, M[VAR_2]    
                MOV     R2, 1           
                CMP     R1, R2          ; ZCNO flags affected
                JMP.P   L2              
L1:             NOP                     
                MOV     R1, 1           ; Load return value into R1 (convention)
                RET                     ; Return from subroutine, PC restored from stack [cite: 183]
L2:             NOP                     
                MOV     R1, M[VAR_2]    
                MOV     R2, 1           
                SUB     R1, R2          ; ZCNO flags affected
                MOV     M[VAR_10], R1   
                MOV     R1, M[VAR_10]   
                PUSH    R1              ; Push parameter
; call fact             -------------------------
                PUSH    R0              ; Reserva espaço para retorno
                CALL    FACT            ; Chama a rotina
                POP     M[VAR_11]       ; Atribui o valor à variável

                MOV     R1, M[VAR_2]    
                MOV     R2, M[VAR_11]   
                MUL     R1, R2          ; R1=MSW, R2=LSW. Unsigned. Z based on 32bit, CNO=0
                MOV     M[VAR_12], R2   ; Store LSW into result
                MOV     R1, M[VAR_12]   ; Load return value into R1 (convention)
                RET                     ; Return from subroutine, PC restored from stack [cite: 183]
main:           NOP                     
; writes STR_LIT_1        -------------------------
                PUSH    STR_LIT_1       ; Endereço da string passado via pilha
                CALL    WRITES          ; Chama a rotina
                POP     R0              

; call read             -------------------------
                PUSH    R0              ; Reserva espaço para retorno
                CALL    READ            ; Chama a rotina
                POP     M[VAR_16]       ; Atribui o valor à variável

                MOV     R1, M[VAR_16]   
                MOV     M[VAR_17], R1   
                MOV     R1, M[VAR_16]   
                PUSH    R1              ; Push parameter
; call fact             -------------------------
                PUSH    R0              ; Reserva espaço para retorno
                CALL    FACT            ; Chama a rotina
                POP     M[VAR_18]       ; Atribui o valor à variável

; write VAR_18          -------------------------
                PUSH    VAR_18          ; Endereço do valor passado via pilha
                CALL    WRITE           ; Chama a rotina
                POP     R0              ; Limpa a pilha

; halt          -------------------------                
                BR      Fim             ; Fim com loop infinito

Fim:            BR      Fim             
