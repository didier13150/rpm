RPMDEFINES := --define "_sourcedir $(SRCDIR)" \
              --define "_specdir $(SRCDIR)" \
              --define "_srcrpmdir $(SRCDIR)" \
              --define "_rpmdir $(SRCDIR)"

SRCDEFINES := --define "_source_filedigest_algorithm 1" \
              --define "_binary_filedigest_algorithm 1"

ARCH := $(shell uname -i)
DISTRIB := $(shell source /etc/os-release && echo $${ID}-$${VERSION_ID})
TARGET := $(DISTRIB)-$(ARCH)

all: fedora

fedora: clean sources build log

clean:
	@echo -e "\033[1;32mCleaning" $(shell basename $(SRCDIR) ) "directory \033[0m"
	@rm -rfv *~ build.log root.log state.log *.rpm

rpmlint:
	@echo -e "\033[1;32mChecking "$(NAME)".spec file\033[0m"
	rpmlint *.spec

srpm:
	@echo -e "\033[1;32mBuilding SRPM file\033[0m"
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME).spec

build: srpm
	@echo -e "\033[1;32mBuilding RPMs files\033[0m"
	-mock -r '$(TARGET)' rebuild *.src.rpm
	-mv /var/lib/mock/$(TARGET)/result/*.rpm $(SRCDIR)

log:
	@echo -e "\033[1;32mCopying mock log files\033[0m"
	@mv /var/lib/mock/$(TARGET)/result/*.log $(SRCDIR)

help:
	@echo -e "\033[1;32mAvailable targets:\033[0m"
	@echo " - all:       Building SRPM and RPMs (default target: ie when make is called without arg)"
	@echo " - rpmlint:   Test spec file"
	@echo " - srpm:      Make SRPM"
	@echo " - build:     Make RPMs from SRPM"
	@echo " - log:       Copy mock log file to current dir"
	@echo " - clean:     Delete mock log files and all (S)RPMs"
