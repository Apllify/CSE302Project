	.globl main
	.text
main:
	pushq %rsp
	movq %rsp, %rbp


	subq $96, %rsp


	/* %0 = const 20 */
	movq $20, -8(%rbp)

	/* %1 = const 0 */
	movq $0, -16(%rbp)

	/* %2 = const 1 */
	movq $1, -24(%rbp)

	/* %3 = const 0 */
	movq $0, -32(%rbp)

	/* label %.L4 */

	/* %7 = copy %0 */
	movq -8(%rbp), %r11
	movq %r11, -40(%rbp)

	/* %8 = const 0 */
	movq $0, -48(%rbp)

	/* %9 = sub %7 %8 */
	movq -40(%rbp), %r11
	subq -48(%rbp), %r11
	movq %r11, -56(%rbp)

	/* jnle %9 %.L5 */

	/* jmp %.L6 */

	/* label %.L5 */

	/* %10 = copy %0 */
	movq -8(%rbp), %r11
	movq %r11, -64(%rbp)

	/* %11 = const 1 */
	movq $1, -72(%rbp)

	/* %0 = sub %10 %11 */
	movq -64(%rbp), %r11
	subq -72(%rbp), %r11
	movq %r11, -8(%rbp)

	/* %12 = copy %1 */
	movq -16(%rbp), %r11
	movq %r11, -80(%rbp)

	/* print %12 */

	/* %13 = copy %1 */
	movq -16(%rbp), %r11
	movq %r11, -88(%rbp)

	/* %14 = copy %2 */
	movq -24(%rbp), %r11
	movq %r11, -96(%rbp)

	/* %3 = add %13 %14 */
	movq -88(%rbp), %r11
	addq -96(%rbp), %r11
	movq %r11, -32(%rbp)

	/* %1 = copy %2 */
	movq -24(%rbp), %r11
	movq %r11, -16(%rbp)

	/* %2 = copy %3 */
	movq -32(%rbp), %r11
	movq %r11, -24(%rbp)

	/* jmp %.L4 */

	/* label %.L6 */



	movq %rbp, %rsp
	popq %rbp
	movq $0, %rax
	retq