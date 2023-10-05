CC_PATH ?= ../llvm-project-memswasm/build
WASI_LIBC_PATH ?= ../ms-wasi-libc/sysroot
SUFFIX ?= .wasm

CC = $(CC_PATH)/bin/clang
CFLAGS =-O2 --target=wasm32-unknown-wasi -ffreestanding --sysroot $(WASI_LIBC_PATH) -x c -L$(WASI_LIBC_PATH)/lib/wasm32-wasi -lc -Wl,--no-entry -Wl,--export-all -DPOLYBENCH_TIME -D_WASI_EMULATED_PROCESS_CLOCKS -lwasi-emulated-process-clocks

LINEAR_ALGEBRA_KERNELS_FILES = $(wildcard linear-algebra/kernels/*/*.c)
LINEAR_ALGEBRA_SOLVERS_FILES = $(wildcard linear-algebra/solvers/*/*.c)

DATAMINING_FILES = $(wildcard datamining/*/*.c)
MEDLEY_FILES = $(wildcard medley/*/*.c)
STENCILS_FILES = $(wildcard stencils/*/*.c)

INCLUDES = -Iutilities -I$(WASI_LIBC_PATH)/include

ALL_C_FILES = $(LINEAR_ALGEBRA_KERNELS_FILES) $(LINEAR_ALGEBRA_SOLVERS_FILES) $(DATAMINING_FILES) $(MEDLEY_FILES) $(STENCILS_FILES)

ALL_TARGET = $(patsubst %.c,%$(SUFFIX),$(ALL_C_FILES))

.PHONY: all clean

all: $(ALL_TARGET)

%$(SUFFIX): %.c
	$(CC) $(INCLUDES) -o $@ $< utilities/polybench.c $(CFLAGS)

clean:
	rm -f $(ALL_TARGET)

