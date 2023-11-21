global _entry
global _type
default rel

section .data
_type: db 0 ; eval type is num

section .text
_entry:
    mov rax, 100
    push rax
    mov rax, [rsp+0]
    push rax
    mov rax, [rsp+8]
    push rax
    mov rax, [rsp+16]
    push rax
    mov rax, 1
    pop r8
    sub rax, r8
    pop r8
    sub rax, r8
    pop r8
    add rax, r8
    add rsp, 8
    ret