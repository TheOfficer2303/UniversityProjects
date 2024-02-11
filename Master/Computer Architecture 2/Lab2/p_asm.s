// oznaka sintakse:
.intel_syntax noprefix

// neka simbol potprogram_asm
// bude vidljiv izvana:
.global potprogram_asm


potprogram_asm:
    push ebp # pohranimo staru vrijednost na stog
    mov ebp, esp

    sub esp, 8
    mov eax, [ebp + 8] # parametar n
    mov edx, eax # edx = n
    mov ecx, 0 # ecx = brojac = 0
    mov eax, 0 # eax = zbroj = 0

    petlja:
    cmp ecx, edx 
    jl zbroji # je li brojac < n
    mov esp, ebp
    pop ebp
    ret

    zbroji:
    add eax, ecx
    add ecx, 1
    jmp petlja
    