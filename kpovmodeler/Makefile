SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
SRC := kpovmodeler-1.1.3.tar.gz
include ../common/Makefile
sources:
	[ -f $(SRC) ] && exit 0 || svn export -r 1305095 svn://anonsvn.kde.org/home/kde/trunk/extragear/graphics/kpovmodeler kpovmodeler-1.1.3
	tar -czf $(SRC) kpovmodeler-1.1.3
	rm -rf kpovmodeler-1.1.3