;============== Região de Dados (inicia no endereço 8000h)                
                ORIG    8000h           

STR_LIT_1       STR     'I','n','t','r','o','d','u','z','a',' ','i','n','t','e','i','r','o',':',' ',0; 'Introduza inteiro: '
VAR_1           WORD    fact            ; fact
VAR_10          WORD    t4              ; t4
VAR_11          WORD    main            ; main
VAR_12          WORD    Introduza inteiro: ; Introduza inteiro: 
VAR_13          WORD    read            ; read
VAR_14          WORD    t5              ; t5
VAR_15          WORD    t6              ; t6
VAR_16          WORD    t7              ; t7
VAR_17          WORD    end_main        ; end_main
VAR_2           WORD    param1          ; param1
VAR_3           WORD    1               ; 1
VAR_4           WORD    t1              ; t1
VAR_7           WORD    L2              ; L2
VAR_8           WORD    t2              ; t2
VAR_9           WORD    t3              ; t3

SP_ADDRESS      EQU     FDFFh           

;============== Região de Código (inicia no endereço 0000h)                
                ORIG    0000h           
                JMP     _start          ; jump to main

;-------------- Rotinas                 

WRITES:         NOP                     ; escreve uma string na consola
MostraChar:     MOV     R2, M[R1]       ; Lê o carater apontado por R1
                CMP     R2, 0           ; Compara com o terminador
                JMP.Z   FimChar         ; Se for zero, salta para o fim
                MOV     M[FFFEh], R2    ; Escreve o carater no endereço de saída
                INC     R1              ; Avança para o próximo carater
                BR      MostraChar      ; Repete o ciclo
FimChar:        RET                     

;-------------- Programa Principal                 
_start:         NOP                     
                MOV     R7, SP_ADDRESS  
                MOV     SP, R7          ; Define o Stack Pointer

fact:           NOP                     
                MOV     R1, M[param1]   
                MOV     R2, 1           
                CMP     R1, R2          ; ZCNO flags affected
                JMP.NP  REL_TRUE_5      
                MOV     M[t1], 0        
                JMP     REL_END_6       
REL_TRUE_5:     NOP                     
                MOV     M[t1], 1        
REL_END_6:      NOP                     
;; AVISO: Operação TAC 'IFFALSE' não traduzida para P3.
L2:             NOP                     
                MOV     R1, M[param1]   
                MOV     R2, 1           
                SUB     R1, R2          ; ZCNO flags affected
                MOV     M[t2], R1       
                MOV     R1, M[t2]       
                PUSH    R1              ; Push parameter
                CALL    fact            ; PC pushed to stack
                MOV     M[t3], R1       ; Store return value (conventionally R1)
                MOV     R1, M[param1]   
                MOV     R2, M[t3]       
                MUL     R1, R2          ; R1=MSW, R2=LSW. Unsigned. Z based on 32bit, CNO=0
                MOV     M[t4], R1       ; Store LSW into result
                MOV     R1, M[t4]       ; Load return value into R1 (convention)
                RET                     ; Return from subroutine, PC restored from stack [cite: 183]
main:           NOP                     
                MOV     R1, STR_LIT_1   ; R1 aponta para o endereço da string "Introduza inteiro: "
                CALL    WRITES          ; Chama a rotina
                CALL    read            ; PC pushed to stack
                MOV     M[t5], R1       ; Store return value (conventionally R1)
                MOV     R1, M[t5]       
                PUSH    R1              ; Push parameter
                CALL    fact            ; PC pushed to stack
                MOV     M[t6], R1       ; Store return value (conventionally R1)
; write         -------------------------                
                MOV     R1, M[VAR_15]   ; Lê o carater apontado por R1
                MOV     M[FFFEh], R1    ; Escreve o carater no endereço de saída
                BR      Fim             ; Fim com loop infinito
end_main:       NOP                     

Fim:            BR      Fim             
