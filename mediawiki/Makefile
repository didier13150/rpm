SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
include ../common/Makefile
ALLSRCS := Mpdf CategoryTree Math Auth_remoteuser
prepare:
	@echo -e "\033[1;32mDownloading extensions from GIT\033[0m"
	
	@for extension in $(ALLSRCS) ; do \
		if [ ! -f $$extension.tgz ] ; then \
			echo -n "$$extension: " ; \
			git clone https://gerrit.wikimedia.org/r/p/mediawiki/extensions/$$extension ; \
			tar -czf $$extension.tgz $$extension ; \
			rm -rf $$extension ; \
		fi ; \
	done

clean-extension:
	@for extension in $(ALLSRCS) ; do \
		rm -f  $$extension.tgz ; \
	done