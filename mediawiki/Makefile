SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
include ../common/Makefile
GERRITSRCS := Mpdf CategoryTree Math Auth_remoteuser
WIKIMEDIASRCS := Git2Pages RandomImage MultimediaViewer CommonsMetadata BetaFeatures ConfirmAccount PdfHandler
SPECIALSRCS := Widgets

prepare:
	@echo -e "\033[1;32mDownloading extensions from GIT\033[0m"
	
	@for extension in $(GERRITSRCS) ; do \
		echo -e "\033[1;32m$$extension\033[0m" ; \
		if [ ! -f $$extension.tgz ] ; then \
			echo -n "$$extension: " ; \
			git clone https://gerrit.wikimedia.org/r/p/mediawiki/extensions/$$extension.git ; \
			tar -czf $$extension.tgz $$extension ; \
			rm -rf $$extension ; \
		fi ; \
	done
	@for extension in $(SPECIALSRCS) ; do \
		echo -e "\033[1;32m$$extension\033[0m" ; \
		if [ ! -f $$extension.tgz ] ; then \
			echo -n "$$extension: " ; \
			git clone https://gerrit.wikimedia.org/r/p/mediawiki/extensions/$$extension.git ; \
			pushd $$extension ; git submodule init ; git submodule update ; popd ; \
			tar -czf $$extension.tgz $$extension ; \
			rm -rf $$extension ; \
		fi ; \
	done
	@for extension in $(WIKIMEDIASRCS) ; do \
		echo -e "\033[1;32m$$extension\033[0m" ; \
		if [ ! -f $$extension.tgz ] ; then \
			echo "$$extension: git clone https://git.wikimedia.org/git/mediawiki/extensions/$$extension.git" ; \
			git clone https://git.wikimedia.org/git/mediawiki/extensions/$$extension.git ; \
			tar -czf $$extension.tgz $$extension ; \
			rm -rf $$extension ; \
		fi ; \
	done

clean-extension:
	@for extension in $(GERRITSRCS) ; do \
		rm -f  $$extension.tgz ; \
	done
	@for extension in $(WIKIMEDIASRCS) ; do \
		rm -f  $$extension.tgz ; \
	done
