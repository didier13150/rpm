RPMDEFINES := --define "_sourcedir $(SRCDIR)" \
              --define "_specdir $(SRCDIR)" \
              --define "_srcrpmdir $(SRCDIR)" \
              --define "_rpmdir $(SRCDIR)"

SRCDEFINES := --define "_source_filedigest_algorithm 1" \
              --define "_binary_filedigest_algorithm 1"

ARCH := $(shell uname -i)
DISTRIB := $(shell source /etc/os-release && echo $${ID}-$${VERSION_ID})
TARGET := $(DISTRIB)-$(ARCH)
URIS := $(shell rpmspec -P $(NAME).spec | grep -i '^source' | awk -F ':' '{print $$2":"$$3}' | tr -d ' ')

all: fedora

fedora: clean sources srpm rpmlint build log

clean:
	@echo -e "\033[1;32mCleaning" $(shell basename $(SRCDIR) ) "directory \033[0m"
	@rm -rfv *~ {build,root,state}.log *.rpm

rpmlint:
	@echo -e "\033[1;32mChecking "$(NAME)".spec file\033[0m"
	-rpmlint $(NAME).spec $(NAME)*.rpm

srpm:
	@echo -e "\033[1;32mBuilding SRPM file\033[0m"
	@rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME).spec

build: srpm
	@echo -e "\033[1;32mBuilding RPMs files\033[0m"
	-mock -r '$(TARGET)' rebuild $(NAME)*.src.rpm
	-mv /var/lib/mock/$(TARGET)/result/*.rpm $(SRCDIR)

log:
	@echo -e "\033[1;32mCopying mock log files\033[0m"
	@mv /var/lib/mock/$(TARGET)/result/{build,root,state}.log $(SRCDIR)

help:
	@echo -e "\033[1;32mAvailable targets:\033[0m"
	@echo " - all:       Building SRPM and RPMs (default target: ie when make is called without arg)"
	@echo " - rpmlint:   Test spec file"
	@echo " - srpm:      Make SRPM"
	@echo " - build:     Make RPMs from SRPM"
	@echo " - log:       Copy mock log file to current dir"
	@echo " - clean:     Delete mock log files and all (S)RPMs"

sources: prepare
	@echo -e "\033[1;32mDownloading sources\033[0m"
	@for url in $(shell echo $(URIS) | tr ' ' '\n') ; do \
		valid=`echo "$$url" | grep '://'` ; \
		if [ ! -z $$valid ] ; then \
			pkgsrc=`basename "$${url}" | awk -F '?' '{print $$1}'` ; \
			[ -f $$pkgsrc ] || wget -O $$pkgsrc $$url ; \
			[ $$? -eq 0 ] && chmod 0644 $$pkgsrc || rm -f $$pkgsrc ; \
		fi ; \
	done
