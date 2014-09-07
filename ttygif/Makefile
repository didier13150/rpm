SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
EXTRASRC := ttygif
EXTRASRCNAME := ttygif.tar.gz
include ../common/Makefile
prepare:
	@echo -e "\033[1;32mDownloading extra from Git\033[0m"
	@if [ ! -f $(EXTRASRC) ] ; then \
		git clone https://github.com/icholy/$(EXTRASRC).git $(EXTRASRC) ; \
		tar -czf $(EXTRASRCNAME) $(EXTRASRC) ; \
	fi
