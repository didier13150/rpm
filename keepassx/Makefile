SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
SRCVER := $(shell rpmspec -P $(NAME).spec | grep -i '^version' | awk -F ':' '{print $$2}' | tr -d ' ')
SRCNAME := $(shell rpmspec -P $(NAME).spec | grep -i '^source' | head -1 | awk -F ':' '{print $$3}' | tr -d ' ' | xargs basename)

include ../common/Makefile
prepare:
	@echo -e "\033[1;32mDownloading from Git\033[0m"
	@if [ ! -d $(NAME) ] ; then \
		git clone https://github.com/didier13150/keepassx.git $(NAME) ; \
	else \
		pushd $(NAME) ; \
		git co master ; \
		git pull ; \
		popd ; \
	fi
	@rm -f $(SRCNAME)
	@tar -czf $(SRCNAME) $(NAME)

