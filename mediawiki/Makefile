SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
include ../common/Makefile
ALLSRCS := Cite SyntaxHighlight_GeSHi PdfExport Mpdf CategoryTree Math
prepare:
	@echo -e "\033[1;32mDownloading extensions from GIT\033[0m"
	@for extension in $(ALLSRCS) ; do \
		rm -f  $$extension.tgz ; \
		echo -n "$$extension: " ; \
		[ -d $$extension ] || git clone https://gerrit.wikimedia.org/r/p/mediawiki/extensions/$$extension ; \
		tar -czf $$extension.tgz $$extension ; \
		rm -rf $$extension ; \
	done
