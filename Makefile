PKGS := $(shell ls -l | grep ^d | grep -v '^common$$' | grep -v '^doc$$' | awk '{print $$9}')
LOGFILE := globalbuild.log
ARCH := $(shell uname -i)
DISTNAME := $(shell source /etc/os-release && echo $${ID})
DISTRELEASE := $(shell source /etc/os-release && echo $${VERSION_ID})
DISTRIB := $(DISTNAME)-$(DISTRELEASE)
TARGET := $(DISTRIB)-$(ARCH)
HOSTNAME := $(shell hostname --fqdn)
REPOPATH := /var/www/fedora-repo
REPODIR := $(REPOPATH)/fc$(DISTRELEASE)

all: clean build repo
repo: dirlist repository repoview sign

build:
	@rm -f $(LOGFILE)
	@touch $(LOGFILE)
	@for dir in $(PKGS) ; \
	do \
		echo -e "\033[1;32mBuilding $$dir\033[0m" ; \
		cd $$dir ; \
		make 1>>../$(LOGFILE) 2>&1; \
		cd .. ; \
	done

srpm:
	@for dir in $(PKGS) ; do pushd $$dir 1>/dev/null 2>&1; make srpm ; popd 1>/dev/null 2>&1 ; done

clean:
	@for dir in $(PKGS) ; do pushd $$dir 1>/dev/null 2>&1 ; make clean ; popd 1>/dev/null 2>&1 ; done

rpmlint:
	@for dir in $(PKGS) ; do pushd $$dir 1>/dev/null 2>&1 ; make rpmlint ; popd 1>/dev/null 2>&1 ; done

repository:
	@echo -e "\033[1;32mUpdating repository on $(REPODIR)\033[0m"
	@mkdir -p $(REPODIR)
	@for dir in $(PKGS) ; do \
		if [ -d $$dir/result ] ; then \
			mkdir -p $(REPODIR)/$$dir ; \
			cp $$dir/result/*.rpm $(REPODIR)/$$dir/ || true ; \
		fi ; \
	done
	@createrepo --update -d $(REPODIR)

repoview:
	@rm -rf $(REPODIR)/repoview
	@repoview $(REPODIR) -k ./common/repoview/templates -f -o $(REPODIR)/repoview --url "http://$(HOSTNAME)/repository/repoview" --title "RPM for $(DISTRIB) $(ARCH)"
	@rsync -avzr ./common/repoview/images $(REPODIR)/repoview/

sign:
	@echo "Signing RPM on $(REPOPATH)"
	@for rpm in $(shell find $(REPOPATH) -name '*.rpm') ; do \
		echo $${rpm} ; \
	done

dirlist:
	@echo "Processing directories: $(PKGS)"

showvars:
	@echo "ARCH:        $(ARCH)"
	@echo "DISTNAME:    $(DISTNAME)"
	@echo "DISTRELEASE: $(DISTRELEASE)"
	@echo "DISTRIB:     $(DISTRIB)"
	@echo "TARGET:      $(TARGET)"
	@echo "HOSTNAME:    $(HOSTNAME)"
	@echo
	@echo "REPOPATH:    $(REPOPATH)"
	@echo "REPODIR:     $(REPODIR)"
	@echo "LOGFILE:     $(LOGFILE)"
	@echo "PKGS:        $(PKGS)"
	
help:
	@echo -e "\033[1;32mAvailable targets:\033[0m"
	@echo " - all:       Building all SRPM and RPMs and create repository (default target: ie when make is called without arg)"
	@echo " - repo:      Create or update local repository, and run repoview"
	@echo " - srpm:      Make SRPM"
	@echo " - build:     Make RPMs from SRPM"
	@echo " - clean:     Delete mock log files and all (S)RPMs"
