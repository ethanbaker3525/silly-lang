global _entry
global _type
default rel

section .data
_type: db 0 ; eval type is num

section .text
_entry:
    ; int sub
    ; num literal
    mov rax, 1
    push rax
    ; int sub
    ; num literal
    mov rax, 2
    push rax
    ; num literal
    mov rax, 3
    pop r8
    sub rax, r8
    pop r8
    sub rax, r8
    ret