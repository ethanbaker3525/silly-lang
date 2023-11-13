
    default rel
    section .text
    global _entry
_entry:


    mov rax, 2
    push rax


    mov rax, 5
    push rax

    mov rax, 15
cqo
    pop r8
    div r8
    pop r8
    add rax, r8
    push rax

    mov rax, 15
cqo
    pop r8
    div r8

    ret
