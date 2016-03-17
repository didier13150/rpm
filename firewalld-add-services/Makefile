SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
include ../common/Makefile
prepare:
	tar -czf $(NAME).tar.gz *.xml README.md
