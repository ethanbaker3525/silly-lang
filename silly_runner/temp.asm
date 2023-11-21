global _entry
global _type
default rel

section .data
_type: db 0 ; eval type is num

section .text
_entry:
    mov rax, 1
    push rax
    mov rax, 1
    pop r8
    add rax, r8
    ret