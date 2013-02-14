SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
SRCDWL := $(shell rpmspec -P $(NAME).spec | grep -i '^source' | head -1 | awk -F ':' '{print $$2":"$$3}' | tr -d ' ')
SRCVER := $(shell rpmspec -P $(NAME).spec | grep -i '^version' | awk -F ':' '{print $$2}' | tr -d ' ')
SRCNAME := $(shell basename $(SRCDWL))
include ../common/Makefile
sources:
	[ -f $(SRCNAME) ] && exit 0 || svn export svn://anonsvn.kde.org/home/kde/trunk/extragear/graphics/kpovmodeler kpovmodeler-$(SRCVER)
	tar -czf $(SRCNAME) kpovmodeler-$(SRCVER)
	rm -rf kpovmodeler-$(SRCVER)