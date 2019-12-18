SHELL := bash

all:
	@echo -n "1 " && python3 prog.py input1.txt
	@echo -n "2 " && python3 prog.py input2.txt

test: test*
	@for file in $^ ; do \
		echo $$file ; \
		python3 prog.py -v $$file ; \
		echo ; \
	done
