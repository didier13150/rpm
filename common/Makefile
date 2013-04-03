RPMDEFINES := --define "_sourcedir $(SRCDIR)" \
              --define "_specdir $(SRCDIR)" \
              --define "_srcrpmdir $(SRCDIR)/result" \
              --define "_rpmdir $(SRCDIR)"

SRCDEFINES := --define "_source_filedigest_algorithm 1" \
              --define "_binary_filedigest_algorithm 1"

ARCH := $(shell uname -i)
DISTRIB := $(shell source /etc/os-release && echo $${ID}-$${VERSION_ID})
TARGET := $(DISTRIB)-$(ARCH)
SRCURIS := $(shell rpmspec -P $(NAME).spec | grep -i '^source' | awk -F ':' '{print $$2":"$$3}' | tr -d ' ')

all: fedora
fedora: clean sources srpm rpmlint build

clean:
	@echo -e "\033[1;32mCleaning" $(shell basename $(SRCDIR) ) "directory \033[0m"
	@rm -rfv \
		*~ \
		$(SRCDIR)/{build,root,state,available_pkgs,installed_pkgs}.log \
		$(SRCDIR)/*.rpm \
	@rm -rf $(SRCDIR)/result

rpmlint:
	@echo -e "\033[1;32mChecking "$(NAME)".spec file\033[0m"
	-rpmlint $(NAME).spec result/$(NAME)*.src.rpm

srpm:
	@echo -e "\033[1;32mBuilding SRPM file\033[0m"
	@rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME).spec

build: srpm
	@echo -e "\033[1;32mBuilding RPMs files\033[0m"
	@mkdir -p $(SRCDIR)/result
	@mock -r '$(TARGET)' --resultdir=$(SRCDIR)/result rebuild $(SRCDIR)/result/$(NAME)*.src.rpm

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
	@for url in $(shell echo $(SRCURIS) | tr ' ' '\n') ; do \
		remote=`echo "$$url" | grep '://'` ; \
		if [ ! -z $$remote ] ; then \
			pkgsrc=`basename "$${url}" | awk -F '?' '{print $$1}'` ; \
			[ -f $$pkgsrc ] || wget -O $$pkgsrc $$url ; \
			[ $$? -eq 0 ] && chmod 0644 $$pkgsrc || rm -f $$pkgsrc ; \
		fi ; \
	done
