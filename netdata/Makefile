SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
SRCVER := $(shell rpmspec -P $(NAME).spec | grep -i '^version' | awk -F ':' '{print $$2}' | tr -d ' ')
SRCNAME := $(shell rpmspec -P $(NAME).spec | grep -i '^source' | head -1 | awk -F ':' '{print $$3}' | tr -d ' ' | xargs basename)

include ../common/Makefile
prepare:
