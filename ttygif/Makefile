SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
SRCVER := $(shell rpmspec -P $(NAME).spec | grep -i '^version' | awk -F ':' '{print $$2}' | tr -d ' ')
SRCNAME := $(shell rpmspec -P $(NAME).spec | grep -i '^source' | head -1 | awk -F ':' '{print $$2}' | tr -d ' ' | xargs basename)
include ../common/Makefile
prepare:
	@echo -e "\033[1;32mDownloading extra from Git\033[0m"
	@if [ ! -d "$(SRCNAME)-$(SRCVER)" ] ; then \
		git clone https://github.com/icholy/$(NAME).git $(NAME)-$(SRCVER) ; \
	fi
	@if [ ! -f "$(SRCNAME)" ] ; then \
		tar -czf $(NAME)-$(SRCVER).tar.gz $(NAME)-$(SRCVER) ; \
	fi
	@rm -rf $(NAME)-$(SRCVER)

