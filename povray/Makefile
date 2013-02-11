SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
SRC := povray-3.7.0.RC6.tar.gz
include ../common/Makefile
sources:
	[ -f $(SRC) ] || wget http://www.povray.org/redirect/www.povray.org/beta/source/$(SRC)