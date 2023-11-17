global _entry
global _type
default rel

section .data
_type: db 0 ; eval type is num

section .text
_entry:
    mov rax, 1
    cmp rax, 1
    je .if0
    mov rax, 2
    jmp .if1
.if0:
    mov rax, 1
.if1:
    ret