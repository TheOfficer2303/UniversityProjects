	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 12, 0	sdk_version 12, 3
	.globl	_birdMoves                      ; -- Begin function birdMoves
	.p2align	2
_birdMoves:                             ; @birdMoves
	.cfi_startproc
; %bb.0:
	adrp	x0, l_.str@PAGE
	add	x0, x0, l_.str@PAGEOFF
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_birdGreet                      ; -- Begin function birdGreet
	.p2align	2
_birdGreet:                             ; @birdGreet
	.cfi_startproc
; %bb.0:
	adrp	x0, l_.str.1@PAGE
	add	x0, x0, l_.str.1@PAGEOFF
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_birdMenu                       ; -- Begin function birdMenu
	.p2align	2
_birdMenu:                              ; @birdMenu
	.cfi_startproc
; %bb.0:
	adrp	x0, l_.str.2@PAGE
	add	x0, x0, l_.str.2@PAGEOFF
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_dogGreet                       ; -- Begin function dogGreet
	.p2align	2
_dogGreet:                              ; @dogGreet
	.cfi_startproc
; %bb.0:
	adrp	x0, l_.str.3@PAGE
	add	x0, x0, l_.str.3@PAGEOFF
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_dogMenu                        ; -- Begin function dogMenu
	.p2align	2
_dogMenu:                               ; @dogMenu
	.cfi_startproc
; %bb.0:
	adrp	x0, l_.str.4@PAGE
	add	x0, x0, l_.str.4@PAGEOFF
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_catGreet                       ; -- Begin function catGreet
	.p2align	2
_catGreet:                              ; @catGreet
	.cfi_startproc
; %bb.0:
	adrp	x0, l_.str.5@PAGE
	add	x0, x0, l_.str.5@PAGEOFF
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_catMenu                        ; -- Begin function catMenu
	.p2align	2
_catMenu:                               ; @catMenu
	.cfi_startproc
; %bb.0:
	adrp	x0, l_.str.6@PAGE
	add	x0, x0, l_.str.6@PAGEOFF
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_animalPrintGreeting            ; -- Begin function animalPrintGreeting
	.p2align	2
_animalPrintGreeting:                   ; @animalPrintGreeting
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #48
	stp	x29, x30, [sp, #32]             ; 16-byte Folded Spill
	add	x29, sp, #32
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	stur	x0, [x29, #-8]
	ldur	x8, [x29, #-8]
	ldr	x8, [x8, #8]
	str	x8, [sp, #16]                   ; 8-byte Folded Spill
	ldur	x8, [x29, #-8]
	ldr	x8, [x8]
	ldr	x8, [x8, #8]
	blr	x8
	ldr	x10, [sp, #16]                  ; 8-byte Folded Reload
	mov	x8, x0
	adrp	x0, l_.str.7@PAGE
	add	x0, x0, l_.str.7@PAGEOFF
	mov	x9, sp
	str	x10, [x9]
	str	x8, [x9, #8]
	bl	_printf
	ldp	x29, x30, [sp, #32]             ; 16-byte Folded Reload
	add	sp, sp, #48
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_animalPrintMenu                ; -- Begin function animalPrintMenu
	.p2align	2
_animalPrintMenu:                       ; @animalPrintMenu
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #48
	stp	x29, x30, [sp, #32]             ; 16-byte Folded Spill
	add	x29, sp, #32
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	stur	x0, [x29, #-8]
	ldur	x8, [x29, #-8]
	ldr	x8, [x8, #8]
	str	x8, [sp, #16]                   ; 8-byte Folded Spill
	ldur	x8, [x29, #-8]
	ldr	x8, [x8]
	ldr	x8, [x8]
	blr	x8
	ldr	x10, [sp, #16]                  ; 8-byte Folded Reload
	mov	x8, x0
	adrp	x0, l_.str.8@PAGE
	add	x0, x0, l_.str.8@PAGEOFF
	mov	x9, sp
	str	x10, [x9]
	str	x8, [x9, #8]
	bl	_printf
	ldp	x29, x30, [sp, #32]             ; 16-byte Folded Reload
	add	sp, sp, #48
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_constructDog                   ; -- Begin function constructDog
	.p2align	2
_constructDog:                          ; @constructDog
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #16
	.cfi_def_cfa_offset 16
	str	x0, [sp, #8]
	str	x1, [sp]
	ldr	x9, [sp, #8]
	adrp	x8, _dogFunctions@PAGE
	add	x8, x8, _dogFunctions@PAGEOFF
	str	x8, [x9]
	ldr	x8, [sp]
	ldr	x9, [sp, #8]
	str	x8, [x9, #8]
	add	sp, sp, #16
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_constructBird                  ; -- Begin function constructBird
	.p2align	2
_constructBird:                         ; @constructBird
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #16
	.cfi_def_cfa_offset 16
	str	x0, [sp, #8]
	str	x1, [sp]
	ldr	x9, [sp, #8]
	adrp	x8, _birdFunctions@PAGE
	add	x8, x8, _birdFunctions@PAGEOFF
	str	x8, [x9]
	ldr	x8, [sp]
	ldr	x9, [sp, #8]
	str	x8, [x9, #8]
	add	sp, sp, #16
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_constructCat                   ; -- Begin function constructCat
	.p2align	2
_constructCat:                          ; @constructCat
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #16
	.cfi_def_cfa_offset 16
	str	x0, [sp, #8]
	str	x1, [sp]
	ldr	x9, [sp, #8]
	adrp	x8, _catFunctions@PAGE
	add	x8, x8, _catFunctions@PAGEOFF
	str	x8, [x9]
	ldr	x8, [sp]
	ldr	x9, [sp, #8]
	str	x8, [x9, #8]
	add	sp, sp, #16
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_createDog                      ; -- Begin function createDog
	.p2align	2
_createDog:                             ; @createDog
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #32
	stp	x29, x30, [sp, #16]             ; 16-byte Folded Spill
	add	x29, sp, #16
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	str	x0, [sp, #8]
	mov	x0, #16
	bl	_malloc
	str	x0, [sp]
	ldr	x0, [sp]
	ldr	x1, [sp, #8]
	bl	_constructDog
	ldr	x0, [sp]
	ldp	x29, x30, [sp, #16]             ; 16-byte Folded Reload
	add	sp, sp, #32
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_createBird                     ; -- Begin function createBird
	.p2align	2
_createBird:                            ; @createBird
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #32
	stp	x29, x30, [sp, #16]             ; 16-byte Folded Spill
	add	x29, sp, #16
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	str	x0, [sp, #8]
	mov	x0, #16
	bl	_malloc
	str	x0, [sp]
	ldr	x0, [sp]
	ldr	x1, [sp, #8]
	bl	_constructBird
	ldr	x0, [sp]
	ldp	x29, x30, [sp, #16]             ; 16-byte Folded Reload
	add	sp, sp, #32
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_createCat                      ; -- Begin function createCat
	.p2align	2
_createCat:                             ; @createCat
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #32
	stp	x29, x30, [sp, #16]             ; 16-byte Folded Spill
	add	x29, sp, #16
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	str	x0, [sp, #8]
	mov	x0, #16
	bl	_malloc
	str	x0, [sp]
	ldr	x0, [sp]
	ldr	x1, [sp, #8]
	bl	_constructCat
	ldr	x0, [sp]
	ldp	x29, x30, [sp, #16]             ; 16-byte Folded Reload
	add	sp, sp, #32
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_testAnimals                    ; -- Begin function testAnimals
	.p2align	2
_testAnimals:                           ; @testAnimals
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #48
	stp	x29, x30, [sp, #32]             ; 16-byte Folded Spill
	add	x29, sp, #32
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	adrp	x0, l_.str.9@PAGE
	add	x0, x0, l_.str.9@PAGEOFF
	bl	_createDog
	stur	x0, [x29, #-8]
	adrp	x0, l_.str.10@PAGE
	add	x0, x0, l_.str.10@PAGEOFF
	bl	_createCat
	str	x0, [sp, #16]
	adrp	x0, l_.str.11@PAGE
	add	x0, x0, l_.str.11@PAGEOFF
	bl	_createDog
	str	x0, [sp, #8]
	adrp	x0, l_.str.12@PAGE
	add	x0, x0, l_.str.12@PAGEOFF
	bl	_createBird
	str	x0, [sp]
	ldur	x0, [x29, #-8]
	bl	_animalPrintGreeting
	ldr	x0, [sp, #16]
	bl	_animalPrintGreeting
	ldr	x0, [sp, #8]
	bl	_animalPrintGreeting
	ldr	x0, [sp]
	bl	_animalPrintGreeting
	ldur	x0, [x29, #-8]
	bl	_animalPrintMenu
	ldr	x0, [sp, #16]
	bl	_animalPrintMenu
	ldr	x0, [sp, #8]
	bl	_animalPrintMenu
	ldr	x0, [sp]
	bl	_animalPrintMenu
	ldur	x0, [x29, #-8]
	bl	_free
	ldr	x0, [sp, #8]
	bl	_free
	ldp	x29, x30, [sp, #32]             ; 16-byte Folded Reload
	add	sp, sp, #48
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_createNDogs                    ; -- Begin function createNDogs
	.p2align	2
_createNDogs:                           ; @createNDogs
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #48
	stp	x29, x30, [sp, #32]             ; 16-byte Folded Spill
	add	x29, sp, #32
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	stur	w0, [x29, #-4]
	ldursw	x8, [x29, #-4]
	lsl	x0, x8, #4
	bl	_malloc
	str	x0, [sp, #16]
	ldr	x0, [sp, #8]
	adrp	x1, l_.str.13@PAGE
	add	x1, x1, l_.str.13@PAGEOFF
	mov	x2, #-1
	bl	___strcpy_chk
	str	wzr, [sp, #4]
	b	LBB16_1
LBB16_1:                                ; =>This Inner Loop Header: Depth=1
	ldr	w8, [sp, #4]
	ldur	w9, [x29, #-4]
	subs	w8, w8, w9
	b.ge	LBB16_4
	b	LBB16_2
LBB16_2:                                ;   in Loop: Header=BB16_1 Depth=1
	ldr	x8, [sp, #16]
	ldrsw	x9, [sp, #4]
	add	x0, x8, x9, lsl #4
	ldr	x1, [sp, #8]
	bl	_constructDog
	b	LBB16_3
LBB16_3:                                ;   in Loop: Header=BB16_1 Depth=1
	ldr	w8, [sp, #4]
	add	w8, w8, #1
	str	w8, [sp, #4]
	b	LBB16_1
LBB16_4:
	ldr	x0, [sp, #16]
	ldp	x29, x30, [sp, #32]             ; 16-byte Folded Reload
	add	sp, sp, #48
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_testHeapAndStack               ; -- Begin function testHeapAndStack
	.p2align	2
_testHeapAndStack:                      ; @testHeapAndStack
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #16
	.cfi_def_cfa_offset 16
	adrp	x8, l_.str.14@PAGE
	add	x8, x8, l_.str.14@PAGEOFF
	str	x8, [sp, #8]
	adrp	x8, _dogFunctions@PAGE
	add	x8, x8, _dogFunctions@PAGEOFF
	str	x8, [sp]
	ldr	x0, [sp]
	ldr	x1, [sp, #8]
	add	sp, sp, #16
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_main                           ; -- Begin function main
	.p2align	2
_main:                                  ; @main
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #112
	stp	x29, x30, [sp, #96]             ; 16-byte Folded Spill
	add	x29, sp, #96
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	stur	wzr, [x29, #-4]
	stur	w0, [x29, #-8]
	stur	x1, [x29, #-16]
	bl	_testAnimals
	mov	w8, #4
	stur	w8, [x29, #-20]
	ldur	w0, [x29, #-20]
	bl	_createNDogs
	stur	x0, [x29, #-32]
	stur	wzr, [x29, #-36]
	b	LBB18_1
LBB18_1:                                ; =>This Inner Loop Header: Depth=1
	ldur	w8, [x29, #-36]
	ldur	w9, [x29, #-20]
	subs	w8, w8, w9
	b.ge	LBB18_4
	b	LBB18_2
LBB18_2:                                ;   in Loop: Header=BB18_1 Depth=1
	ldur	x8, [x29, #-32]
	ldursw	x9, [x29, #-36]
	add	x0, x8, x9, lsl #4
	bl	_animalPrintGreeting
	ldur	x8, [x29, #-32]
	ldursw	x9, [x29, #-36]
	add	x0, x8, x9, lsl #4
	bl	_animalPrintMenu
	b	LBB18_3
LBB18_3:                                ;   in Loop: Header=BB18_1 Depth=1
	ldur	w8, [x29, #-36]
	add	w8, w8, #1
	stur	w8, [x29, #-36]
	b	LBB18_1
LBB18_4:
	ldur	x0, [x29, #-32]
	bl	_free
	adrp	x0, l_.str.15@PAGE
	add	x0, x0, l_.str.15@PAGEOFF
	bl	_printf
	bl	_testHeapAndStack
	add	x8, sp, #40
	str	x8, [sp, #8]                    ; 8-byte Folded Spill
	str	x0, [sp, #40]
	str	x1, [sp, #48]
	add	x0, sp, #24
	str	x0, [sp, #16]                   ; 8-byte Folded Spill
	adrp	x1, l_.str.16@PAGE
	add	x1, x1, l_.str.16@PAGEOFF
	bl	_constructCat
	ldr	x0, [sp, #8]                    ; 8-byte Folded Reload
	bl	_animalPrintGreeting
	ldr	x0, [sp, #16]                   ; 8-byte Folded Reload
	bl	_animalPrintGreeting
	ldr	x0, [sp, #8]                    ; 8-byte Folded Reload
	bl	_animalPrintMenu
	ldr	x0, [sp, #16]                   ; 8-byte Folded Reload
	bl	_animalPrintMenu
	mov	w0, #0
	ldp	x29, x30, [sp, #96]             ; 16-byte Folded Reload
	add	sp, sp, #112
	ret
	.cfi_endproc
                                        ; -- End function
	.section	__TEXT,__cstring,cstring_literals
l_.str:                                 ; @.str
	.asciz	"im moving!"

l_.str.1:                               ; @.str.1
	.asciz	"kre!"

l_.str.2:                               ; @.str.2
	.asciz	"kukce"

l_.str.3:                               ; @.str.3
	.asciz	"vau!"

l_.str.4:                               ; @.str.4
	.asciz	"kuhanu govedinu"

l_.str.5:                               ; @.str.5
	.asciz	"mijau!"

l_.str.6:                               ; @.str.6
	.asciz	"konzerviranu tunjevinu"

	.section	__DATA,__data
	.globl	_dogFunctions                   ; @dogFunctions
	.p2align	3
_dogFunctions:
	.quad	_dogMenu
	.quad	_dogGreet

	.globl	_catFunctions                   ; @catFunctions
	.p2align	3
_catFunctions:
	.quad	_catMenu
	.quad	_catGreet

	.globl	_birdFunctions                  ; @birdFunctions
	.p2align	3
_birdFunctions:
	.quad	_birdMenu
	.quad	_birdGreet
	.quad	_birdMoves

	.section	__TEXT,__cstring,cstring_literals
l_.str.7:                               ; @.str.7
	.asciz	"%s pozdravlja: %s\n"

l_.str.8:                               ; @.str.8
	.asciz	"%s voli: %s\n"

l_.str.9:                               ; @.str.9
	.asciz	"Hamlet"

l_.str.10:                              ; @.str.10
	.asciz	"Ofelija"

l_.str.11:                              ; @.str.11
	.asciz	"Polonije"

l_.str.12:                              ; @.str.12
	.asciz	"Ptica"

l_.str.13:                              ; @.str.13
	.asciz	"Jedan od N pasa"

l_.str.14:                              ; @.str.14
	.asciz	"Pas 1"

l_.str.15:                              ; @.str.15
	.asciz	"\n"

l_.str.16:                              ; @.str.16
	.asciz	"Macak 1"

.subsections_via_symbols
