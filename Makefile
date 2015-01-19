PKGS := $(shell ls -l | grep ^d | grep -v '^common$$' | grep -v '^doc$$' | awk '{print $$9}' | grep -v '^povray' )
LOGFILE := globalbuild.log
ARCH := $(shell uname -i)
DISTNAME := $(shell source /etc/os-release && echo $${ID})
DISTRELEASE := $(shell source /etc/os-release && echo $${VERSION_ID})
DISTRIB := $(DISTNAME)-$(DISTRELEASE)
TARGET := $(DISTRIB)-$(ARCH)
HOSTNAME := $(shell hostname --fqdn)
REPOPATH := /var/www/fedora-repo
REPODIR := $(REPOPATH)/fc$(DISTRELEASE)
SRCDIR := $(shell pwd)

dummy:
	@echo "Type make all to (re)build all packages"

all: clean build repo
repo: dirlist copy sign refresh repoview

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
	@for dir in $(PKGS) ; do \
		pushd $$dir 1>/dev/null 2>&1 ; \
		make srpm ; \
		popd 1>/dev/null 2>&1 ; \
	done

clean:
	@for dir in $(PKGS) ; do \
		pushd $$dir 1>/dev/null 2>&1 ; \
		make clean ; \
		popd 1>/dev/null 2>&1 ; \
	done

rpmlint:
	@for dir in $(PKGS) ; do \
		pushd $$dir 1>/dev/null 2>&1 ; \
		make rpmlint ; \
		popd 1>/dev/null 2>&1 ; \
	done

copy:
	@echo -e "\033[1;32mCopy RPM to $(REPODIR)\033[0m"
	@mkdir -p $(REPODIR)
	@for dir in $(PKGS) ; do \
		if [ -d $$dir/result ] ; then \
			mkdir -p $(REPODIR)/$$dir ; \
			cp -u $$dir/result/*fc$(DISTRELEASE)*.rpm $(REPODIR)/$$dir/ || true ; \
		fi ; \
	done

refresh:
	@echo -e "\033[1;32mUpdating repository on $(REPODIR)\033[0m"
	@createrepo --update -d $(REPODIR)

repoview:
	@echo -e "\033[1;32mRun repoview on $(REPODIR)\033[0m"
	@rm -rf $(REPODIR)/repoview
	@repoview $(REPODIR) -k ./common/repoview/templates -f \
		-o $(REPODIR)/repoview \
		--url "http://$(HOSTNAME)/repository/repoview" \
		--title "RPM for $(DISTRIB) $(ARCH)"
	@rsync -avzr ./common/repoview/images $(REPODIR)/repoview/

sign:   
	@echo -e "\033[1;32mSigning RPM on $(REPODIR)\033[0m"
	@for rpm in `find $(REPOPATH) -name '*.rpm' -exec rpm --checksig {} \; | grep -v pgp | awk -F ':' '{print $$1}'` ; do \
		rpm --checksig $$rpm ; \
		LANG=C rpm --addsign $$rpm ; \
		rpm --checksig $$rpm ; \
	done
	# $(SRCDIR)/rpmwrap.sh --addsign $$rpm;

dirlist:
	@echo -e "\033[1;32mProcessing directories\033[0m"
	@echo $(PKGS)

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
