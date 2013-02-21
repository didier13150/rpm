SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
SRCDWL1 := $(shell rpmspec -P $(NAME).spec | grep -i '^source0' | awk -F ':' '{print $$2":"$$3}' | tr -d ' ')
SRCNAME1 := $(shell basename $(SRCDWL1))
SRCDWL2 := $(shell rpmspec -P $(NAME).spec | grep -i '^source1' | awk -F ':' '{print $$2":"$$3}' | tr -d ' ')
SRCNAME2 := $(shell basename $(SRCDWL2))
SRCDWL3 := $(shell rpmspec -P $(NAME).spec | grep -i '^source2' | awk -F ':' '{print $$2":"$$3}' | tr -d ' ')
SRCNAME3 := $(shell basename $(SRCDWL3))
SRCDWL4 := $(shell rpmspec -P $(NAME).spec | grep -i '^source3' | awk -F ':' '{print $$2":"$$3}' | tr -d ' ')
SRCNAME4 := $(shell basename $(SRCDWL4))
include ../common/Makefile
sources:
	@echo -e "\033[1;32mDownloading sources\033[0m"
	@[ -f $(SRCNAME1) ] || wget -O $(SRCNAME1) $(SRCDWL1)
	@[ -f $(SRCNAME2) ] || wget -O $(SRCNAME2) $(SRCDWL2) ; chmod 0644 $(SRCNAME2)
	@[ -f $(SRCNAME3) ] || wget -O $(SRCNAME3) $(SRCDWL3) ; chmod 0644 $(SRCNAME3)
	@[ -f $(SRCNAME4) ] || wget -O $(SRCNAME4) $(SRCDWL4)
