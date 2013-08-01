SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
SRCVER := $(shell rpmspec -P $(NAME).spec | grep -i '^version' | awk -F ':' '{print $$2}' | tr -d ' ')
SRCNAME := $(shell rpmspec -P $(NAME).spec | grep -i '^source' | head -1 | awk -F ': ' '{print $$2}' | tr -d ' ' | xargs basename)
SRCPATH := $(shell rpmspec -P $(NAME).spec | grep -i '^source' | head -1 | awk -F ': ' '{print $$2}' | tr -d ' ' | xargs dirname)
include ../common/Makefile
prepare:
	@echo -e "\033[1;32mDownloading from Git\033[0m"
	@if [ ! -f $(SRCNAME) ] ; then \
		wget $(SRCPATH)/v$(SRCVER).tar.gz ; \
		mv v$(SRCVER).tar.gz $(SRCNAME) ; \
	fi

