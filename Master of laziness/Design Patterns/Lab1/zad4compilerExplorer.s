CoolClass::set(int):
  push rbp
  mov rbp, rsp
  mov QWORD PTR [rbp-8], rdi
  mov DWORD PTR [rbp-12], esi
  mov rax, QWORD PTR [rbp-8]
  mov edx, DWORD PTR [rbp-12]
  mov DWORD PTR [rax+8], edx
  nop
  pop rbp
  ret
CoolClass::get():
  push rbp
  mov rbp, rsp
  mov QWORD PTR [rbp-8], rdi
  mov rax, QWORD PTR [rbp-8]
  mov eax, DWORD PTR [rax+8]
  pop rbp
  ret
PlainOldClass::set(int):
  push rbp
  mov rbp, rsp
  mov QWORD PTR [rbp-8], rdi
  mov DWORD PTR [rbp-12], esi
  mov rax, QWORD PTR [rbp-8]
  mov edx, DWORD PTR [rbp-12]
  mov DWORD PTR [rax], edx
  nop
  pop rbp
  ret
Base::Base() [base object constructor]:
  push rbp
  mov rbp, rsp
  mov QWORD PTR [rbp-8], rdi
  mov edx, OFFSET FLAT:vtable for Base+16
  mov rax, QWORD PTR [rbp-8]
  mov QWORD PTR [rax], rdx
  nop
  pop rbp
  ret
CoolClass::CoolClass() [base object constructor]:
  push rbp
  mov rbp, rsp
  sub rsp, 16
  mov QWORD PTR [rbp-8], rdi
  mov rax, QWORD PTR [rbp-8]
  mov rdi, rax
  call Base::Base() [base object constructor]
  mov edx, OFFSET FLAT:vtable for CoolClass+16
  mov rax, QWORD PTR [rbp-8]
  mov QWORD PTR [rax], rdx
  nop
  leave
  ret
main:
  push rbp
  mov rbp, rsp
  push rbx
  sub rsp, 24
  mov edi, 16
  call operator new(unsigned long)
  mov rbx, rax
  mov rdi, rbx
  call CoolClass::CoolClass() [complete object constructor]
  mov QWORD PTR [rbp-24], rbx
  lea rax, [rbp-28]
  mov esi, 42
  mov rdi, rax
  call PlainOldClass::set(int)
  mov rax, QWORD PTR [rbp-24]
  mov rax, QWORD PTR [rax]
  mov rdx, QWORD PTR [rax]
  mov rax, QWORD PTR [rbp-24]
  mov esi, 42
  mov rdi, rax
  call rdx
  mov eax, 0
  mov rbx, QWORD PTR [rbp-8]
  leave
  ret
vtable for CoolClass:
  .quad 0
  .quad typeinfo for CoolClass
  .quad CoolClass::set(int)
  .quad CoolClass::get()
vtable for Base:
  .quad 0
  .quad typeinfo for Base
  .quad __cxa_pure_virtual
  .quad __cxa_pure_virtual
typeinfo for CoolClass:
  .quad vtable for __cxxabiv1::__si_class_type_info+16
  .quad typeinfo name for CoolClass
  .quad typeinfo for Base
typeinfo name for CoolClass:
  .string "9CoolClass"
typeinfo for Base:
  .quad vtable for __cxxabiv1::__class_type_info+16
  .quad typeinfo name for Base
typeinfo name for Base:
  .string "4Base"
