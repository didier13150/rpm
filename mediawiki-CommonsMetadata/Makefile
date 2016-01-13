SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
EXTENSION := $(shell echo $(NAME) | awk -F '-' '{print $$2}')
include ../common/Makefile

prepare:
	@echo -e "\033[1;32mDownloading extensions from GIT: $(EXTENSION)\033[0m"
	@if [ ! -f $(EXTENSION).tgz ] ; then \
		git clone https://git.wikimedia.org/git/mediawiki/extensions/$(EXTENSION).git ; \
	else \
		pushd $(EXTENSION) ; \
		git pull ; \
		popd ; \
	fi
	@rm -f $(EXTENSION).tgz
	@tar -czf $(EXTENSION).tgz $(EXTENSION)
