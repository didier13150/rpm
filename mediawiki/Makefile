SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
SRCDWL := $(shell rpmspec -P $(NAME).spec | grep -i '^source' | head -1 | awk -F ':' '{print $$2":"$$3}' | tr -d ' ')
SRCNAME := $(shell basename $(SRCDWL))
include ../common/Makefile
sources:
	@echo -e "\033[1;32mDownloading sources\033[0m"
	@[ -f $(SRCNAME) ] || wget -O $(SRCNAME) $(SRCDWL)
	@for extension in Cite SyntaxHighlight_GeSHi PdfExport Mpdf CategoryTree Math; do \
		rm -f  $$extension.tgz ; \
		echo -n "$$extension: " ; \
		[ -d $$extension ] && git pull || git clone https://gerrit.wikimedia.org/r/p/mediawiki/extensions/$$extension ; \
		tar -czf $$extension.tgz $$extension ; \
	done
	@for extension in CustomTag CalcBitrate ; do \
		rm -f  $$extension.tgz ; \
		tar -czf $$extension.tgz $$extension ; \
	done
