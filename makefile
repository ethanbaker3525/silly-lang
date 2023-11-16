PY_COMP := silly_compiler.py
RM := rm -f

BUILD := ./build

PY := python
AC := nasm
A_FLAGS := -f elf64
CC := gcc
C_FLAGS := -elf -c -o

main.o:
	@mkdir -p $(BUILD)
	@$(CC) $(C_FLAGS) $(BUILD)/main.o main.c

%.asm:
	@mkdir -p $(BUILD)
	@touch $(BUILD)/$@
	@$(PY) $(PY_COMP) $(BUILD)/$@

%.o : %.asm
	@$(AC) $(A_FLAGS) $(BUILD)/$^

%.run : %.o 
	@make -s main.o
	@$(CC) $(BUILD)/$^ $(BUILD)/main.o  -o $(BUILD)/$@

# use after another command to run all .run files in ./build
.PHONY: run
run:
	$(wildcard $(BUILD)/*.run)

.PHONY: clean
clean:
	@$(RM) -r $(BUILD)




