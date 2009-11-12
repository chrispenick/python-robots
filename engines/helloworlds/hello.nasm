	;; Hello World for the nasm Assembler (Linux)
	
	SECTION .data

	msg	db	"Hello, world!",0xa ; 
	len	equ     $ - msg

	SECTION .text
	global main

main:
        mov     eax,4		; write system call
        mov     ebx,1           ; file (stdou)
        mov     ecx,msg         ; string
        mov     edx,len         ; strlen
	int     0x80		; call kernel

	mov	eax,1		; exit system call
        mov     ebx,0      
        int     0x80		; call kernel

