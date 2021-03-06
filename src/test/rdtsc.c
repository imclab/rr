/* -*- Mode: C; tab-width: 8; c-basic-offset: 8; indent-tabs-mode: t; -*- */

#include "rrutil.h"


static uint64_t rdtsc(void) {
	uint32_t hi, lo;
	__asm__ __volatile__ ("rdtsc" : "=a"(lo), "=d"(hi));
	return (uint64_t)hi << 32 | (uint64_t)lo;
}

static void breakpoint(void) {
	int break_here = 1;
	(void)break_here;
}

int main(int argc, char *argv[]) {
	int i;
	uint64_t last_tsc = 0;

	for (i = 0; i < 100; ++i) {
		uint64_t tsc;

		breakpoint();
		/* NO SYSCALLS BETWEEN HERE AND RDTSC: next event for
		 * replay must be rdtsc */
		tsc = rdtsc();
		test_assert(last_tsc < tsc);
		atomic_printf("%" PRIu64 ",", tsc);
		last_tsc = tsc;
	}

	atomic_puts("EXIT-SUCCESS");
	return 0;
}
