RPMDEFINES     := --define "_sourcedir $(SRCDIR)" \
                  --define "_specdir $(SRCDIR)" \
                  --define "_srcrpmdir $(SRCDIR)/$(RESULT)" \
                  --define "_rpmdir $(SRCDIR)"

SRCDEFINES     := --define "_source_filedigest_algorithm 1" \
                  --define "_binary_filedigest_algorithm 1"

ARCH           := $(shell uname -i)
DISTNAME       := $(shell source /etc/os-release && echo $${ID})
DISTSHORT      := $(shell if [ $(DISTNAME) == "fedora" ] ; then echo 'fc' ; else echo 'el' ; fi)
DISTID         := $(shell source /etc/os-release && echo $${VERSION_ID})
DISTIDNEXT     := $(shell echo $(DISTID)+1 | bc)
DISTRIB        := $(DISTNAME)-$(DISTID)
DISTRIBNEXT    := $(DISTNAME)-$(DISTIDNEXT)
TARGET         := $(DISTRIB)-$(ARCH)
TARGETNEXT     := $(DISTRIBNEXT)-$(ARCH)

SRCURIS        := $(shell rpmspec -P $(NAME).spec | grep -i '^source' | awk -F ':' '{print $$2":"$$3}' | tr -d ' ')
MOCKOPTS       := "--disable-plugin=package_state"
SRCDIR         := $(shell pwd)
RESULT         := result

LIVECD_PKGS    := livecd-build bash coreutils dbus-python dmraid \
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

all:         fedora
next:        fedora-next
fedora:      clean sources srpm rpmlint build rpmlint
fedora-next: clean sources srpm rpmlint fedora-next-build rpmlint
centos-6:    clean sources srpm rpmlint el6-build rpmlint
centos-7:    clean sources srpm rpmlint el7-build rpmlint
.PHONY:      prepare sources

showvars:
	@echo "ARCH:        $(ARCH)"
	@echo "DISTNAME:    $(DISTNAME)"
	@echo "DISTSHORT:   $(DISTSHORT)"
	@echo "DISTID:      $(DISTID)"
	@echo "DISTIDNEXT:  $(DISTIDNEXT)"
	@echo "DISTRIB:     $(DISTRIB)"
	@echo "DISTRIBNEXT: $(DISTRIBNEXT)"
	@echo "TARGET:      $(TARGET)"
	@echo "TARGETNEXT:  $(TARGETNEXT)"
	@echo "RESULT:      $(RESULT)"

clean:
	@echo -e "\033[1;32mCleaning" $(shell basename $(SRCDIR) ) "directory \033[0m"
	@rm -rfv \
		*~ \
		$(SRCDIR)/{build,root,state,available_pkgs,installed_pkgs}.log \
		$(SRCDIR)/*fc$(DISTID)*.rpm \
		$(SRCDIR)/$(RESULT)/$(NAME)*.src.rpm \
		$(SRCDIR)/$(RESULT)/{build,root,state,available_pkgs,installed_pkgs}.log

rpmlint:
	@echo -e "\033[1;32mChecking "$(NAME)".spec file\033[0m"
	-rpmlint $(NAME).spec $(RESULT)/$(NAME)*.rpm

srpm:
	@echo -e "\033[1;32mBuilding SRPM file\033[0m"
	@rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME).spec

build: srpm
	@echo -e "\033[1;32mBuilding RPMs files for Fedora $(DISTID)\033[0m"
	@mock $(MOCKOPTS) -r '$(TARGET)' --$(RESULT)dir=$(SRCDIR)/$(RESULT) rebuild $(SRCDIR)/$(RESULT)/$(NAME)*$(DISTSHORT)$(DISTID)*.src.rpm

fedora-next-build: srpm
	@echo -e "\033[1;32mBuilding RPMs files for Fedora $(DISTIDNEXT)\033[0m"
	@mock $(MOCKOPTS) -r '$(TARGETNEXT)' --$(RESULT)dir=$(SRCDIR)/$(RESULT) rebuild $(SRCDIR)/$(RESULT)/$(NAME)*$(DISTSHORT)$(DISTID)*.src.rpm

el6-build: srpm
	@echo -e "\033[1;32mBuild RPMs files for CentOS 6\033[0m"
	@rm -rf $(SRCDIR)/$(RESULT)-el6
	@mkdir -p $(SRCDIR)/$(RESULT)-el6
	@mock $(MOCKOPTS) -r 'centos-6-$(ARCH)' --$(RESULT)dir=$(SRCDIR)/$(RESULT)-el6 rebuild $(SRCDIR)/$(RESULT)/$(NAME)*$(DISTSHORT)$(DISTID)*.src.rpm

el7-build: srpm
	@echo -e "\033[1;32mBuild RPMs files for CentOS 7\033[0m"
	@rm -rf $(SRCDIR)/$(RESULT)-el7
	@mkdir -p $(SRCDIR)/$(RESULT)-el7
	@mock $(MOCKOPTS) -r 'centos-7-$(ARCH)' --$(RESULT)dir=$(SRCDIR)/$(RESULT)-el7 rebuild $(SRCDIR)/$(RESULT)/$(NAME)*$(DISTSHORT)$(DISTID)*.src.rpm

help:
	@echo -e "\033[1;32mAvailable targets:\033[0m"
	@echo " - fedora:    Building SRPM and RPMs for current Fedora release"
	@echo " - next:      Building SRPM and RPMs for the next Fedora release"
	@echo " - centos:    Building SRPM and RPMs for CentOS 6"
	@echo " - rpmlint:   Test spec and SRPM files"
	@echo " - srpm:      Make SRPM"
	@echo " - build:     Make RPMs from SRPM"
	@echo " - clean:     Delete mock log files and all (S)RPMs"

appliance:
	@echo -e "\033[1;32mBuilding appliance\033[0m"
	@mock $(MOCKOPTS) -r '$(TARGET)' --init --$(RESULT)dir=$(SRCDIR)
	@mock $(MOCKOPTS) -r '$(TARGET)' --install $(APPLIANCE_PKGS) --$(RESULT)dir=$(SRCDIR)
	@mock $(MOCKOPTS) -r '$(TARGET)' --copyin kickstart/graphical.ks /tmp --$(RESULT)dir=$(SRCDIR)
	@mock $(MOCKOPTS) -r '$(TARGET)' --shell 'appliance-creator -n Fedora -c /tmp/graphical.ks' --$(RESULT)dir=$(SRCDIR)
	#@mock $(MOCKOPTS) --clean

livecd:
	@echo -e "\033[1;32mBuilding livecd\033[0m"
	@mock $(MOCKOPTS) -r '$(TARGET)' --init --$(RESULT)dir=$(SRCDIR)
	@mock $(MOCKOPTS) -r '$(TARGET)' --install $(LIVECD_PKGS) --$(RESULT)dir=$(SRCDIR)
	@mock $(MOCKOPTS) -r '$(TARGET)' --copyin kickstart/graphical.ks /tmp --$(RESULT)dir=$(SRCDIR)
	@mock $(MOCKOPTS) -r '$(TARGET)' --shell 'appliance-creator -n Fedora -c /tmp/graphical.ks' --$(RESULT)dir=$(SRCDIR)
	#@mock $(MOCKOPTS) --clean

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

prepare::
