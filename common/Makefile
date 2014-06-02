RPMDEFINES := --define "_sourcedir $(SRCDIR)" \
              --define "_specdir $(SRCDIR)" \
              --define "_srcrpmdir $(SRCDIR)/result" \
              --define "_rpmdir $(SRCDIR)"

SRCDEFINES := --define "_source_filedigest_algorithm 1" \
              --define "_binary_filedigest_algorithm 1"

ARCH := $(shell uname -i)
DISTNAME := $(shell source /etc/os-release && echo $${ID})
DISTRELEASE := $(shell source /etc/os-release && echo $${VERSION_ID})
DISTRIB := $(DISTNAME)-$(DISTRELEASE)
TARGET := $(DISTRIB)-$(ARCH)
SRCURIS := $(shell rpmspec -P $(NAME).spec | grep -i '^source' | awk -F ':' '{print $$2":"$$3}' | tr -d ' ')
MOCKOPTS := "--disable-plugin=package_state"
SRCDIR := $(shell pwd)


LIVECD_PKGS :=    livecd-build bash coreutils dbus-python dmraid \
                  livecd-tools selinux-policy-targeted yum bzip2 cpio diffutils \
                  findutils gawk gcc gcc-c++ grep gzip info make patch \
                  redhat-release redhat-rpm-config rpm-build sed shadow-utils \
                  tar unzip util-linux-ng which squashfs-tools centos-release \
                  selinux-policy policycoreutils grub parted
APPLIANCE_PKGS := livecd-build bash coreutils dbus-python dmraid \
                  appliance-tools selinux-policy-targeted yum bzip2 cpio diffutils \
                  findutils gawk gcc gcc-c++ grep gzip info make patch \
                  redhat-release redhat-rpm-config rpm-build sed shadow-utils \
                  tar unzip util-linux-ng which squashfs-tools centos-release \
                  selinux-policy policycoreutils grub parted
	  
all: fedora
fedora: clean sources srpm rpmlint build rpmlint
centos: clean sources srpm rpmlint el6-build rpmlint

showvars:
	@echo "ARCH:        $(ARCH)"
	@echo "DISTNAME:    $(DISTNAME)"
	@echo "DISTRELEASE: $(DISTRELEASE)"
	@echo "DISTRIB:     $(DISTRIB)"
	@echo "TARGET:      $(TARGET)"

clean:
	@echo -e "\033[1;32mCleaning" $(shell basename $(SRCDIR) ) "directory \033[0m"
	@rm -rfv \
		*~ \
		$(SRCDIR)/{build,root,state,available_pkgs,installed_pkgs}.log \
		$(SRCDIR)/*.rpm \
		$(SRCDIR)/result/$(NAME)*.src.rpm \
		$(SRCDIR)/result/*log

rpmlint:
	@echo -e "\033[1;32mChecking "$(NAME)".spec file\033[0m"
	-rpmlint $(NAME).spec result/$(NAME)*.rpm

srpm:
	@echo -e "\033[1;32mBuilding SRPM file\033[0m"
	@rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME).spec

build: srpm
	@echo -e "\033[1;32mBuilding RPMs files\033[0m"
	@mock $(MOCKOPTS) -r '$(TARGET)' --resultdir=$(SRCDIR)/result rebuild $(SRCDIR)/result/$(NAME)*.src.rpm

el6-build: srpm
	@echo -e "\033[1;32mBuild RPMs files for CentOS 6\033[0m"
	@rm -rf $(SRCDIR)/result-el6
	@mkdir -p $(SRCDIR)/result-el6
	@mock $(MOCKOPTS) -r 'centos-6-$(ARCH)' --resultdir=$(SRCDIR)/result-el6 rebuild $(SRCDIR)/result/$(NAME)*.src.rpm

help:
	@echo -e "\033[1;32mAvailable targets:\033[0m"
	@echo " - fedora:    Building SRPM and RPMs for current Fedora release"
	@echo " - centos:    Building SRPM and RPMs for CentOS 6"
	@echo " - rpmlint:   Test spec and SRPM files"
	@echo " - srpm:      Make SRPM"
	@echo " - build:     Make RPMs from SRPM"
	@echo " - clean:     Delete mock log files and all (S)RPMs"

appliance:
	@echo -e "\033[1;32mBuilding appliance\033[0m"
	@mock $(MOCKOPTS) -r '$(TARGET)' --init --resultdir=$(SRCDIR)
	@mock $(MOCKOPTS) -r '$(TARGET)' --install $(APPLIANCE_PKGS) --resultdir=$(SRCDIR)
	@mock $(MOCKOPTS) -r '$(TARGET)' --copyin kickstart/graphical.ks /tmp --resultdir=$(SRCDIR)
	@mock $(MOCKOPTS) -r '$(TARGET)' --shell 'appliance-creator -n Fedora -c /tmp/graphical.ks' --resultdir=$(SRCDIR)
	#@mock $(MOCKOPTS) --clean

iso:
	@echo -e "\033[1;32mBuilding iso\033[0m"

sources: prepare
	@echo -e "\033[1;32mDownloading sources\033[0m"
	@for url in $(shell echo $(SRCURIS) | tr ' ' '\n') ; do \
		mustBeDownloaded=`echo "$$url" | grep '://'` ; \
		if [ ! -z $$mustBeDownloaded ] ; then \
			pkgsrc=`basename "$${url}" | awk -F '?' '{print $$1}'` ; \
			[ -f $$pkgsrc ] || wget -O $$pkgsrc $$url ; \
			[ $$? -eq 0 ] && chmod 0644 $$pkgsrc || rm -f $$pkgsrc ; \
		fi ; \
	done
