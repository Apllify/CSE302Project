	.globl main
	.text
main:
	pushq %rsp
	movq %rsp, %rbp


	subq $96, %rsp




	movq %rbp, %rsp
	popq %rbp
	movq $0, %rax
	retq