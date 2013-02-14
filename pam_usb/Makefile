SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
SRCDWL := $(shell rpmspec -P $(NAME).spec | grep -i '^source' | head -1 | awk -F ':' '{print $$2":"$$3}' | tr -d ' ')
SRCNAME := $(shell basename $(SRCDWL))
include ../common/Makefile
sources:
	[ -f $(SRCNAME) ] || wget -O $(SRCNAME) $(SRCDWL)
