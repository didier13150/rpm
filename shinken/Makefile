SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
SRC := shinken-1.2.4.tar.gz
include ../common/Makefile
sources:
	[ -f $(SRC) ] || wget http://shinken-monitoring.org/pub/shinken-1.2.4.tar.gz