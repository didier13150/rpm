SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
SRCVER := $(shell rpmspec -P $(NAME).spec | grep -i '^version' | awk -F ':' '{print $$2}' | tr -d ' ')
SRCNAME := $(shell rpmspec -P $(NAME).spec | grep -i '^source' | head -1 | awk -F ':' '{print $$3}' | tr -d ' ' | xargs basename)
include ../common/Makefile
prepare:
	@echo -e "\033[1;32mDownloading from Git\033[0m"
	@if [ ! -d Nagstamon ] ; then \
		git clone git://github.com/HenriWahl/Nagstamon.git ; \
	else \
		pushd Nagstamon ; \
		git pull ; \
		popd ; \
	fi
	@rm -f $(SRCNAME)
	@pushd Nagstamon ; tar -czf ../$(SRCNAME) Nagstamon ; popd

