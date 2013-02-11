SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
SRC := aluzzardi-pam_usb-0.5.0-25-g6a30dff.tar.gz
include ../common/Makefile
sources:
	[ -f $(SRC) ] || wget -O $(SRC) https://github.com/aluzzardi/pam_usb/tarball/master