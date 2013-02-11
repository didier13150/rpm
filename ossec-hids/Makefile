SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
SRC := ossec-hids-2.7.tar.gz
include ../common/Makefile
sources:
	[ -f $(SRC) ] || wget http://www.ossec.net/files/$(SRC)
