PKGS := $(shell ls -l | grep ^d | grep -v '^common$$' | grep -v '^doc$$' | awk '{print $$9}')
REPODIR := /var/www/fedora-repo
LOGFILE := build.log
DISTRIB := $(shell source /etc/os-release && echo $${ID}-$${VERSION_ID})
ARCH := $(shell uname -i)
HOSTNAME := $(shell hostname --fqdn)

all: clean build repo
repo: dirlist repository repoview

build:
	@rm -f $(LOGFILE)
	@touch $(LOGFILE)
	@for dir in $(PKGS) ; \
	do \
		echo -e "\033[1;32mBuilding $$dir\033[0m" ; \
		cd $$dir ; \
		make 1>>../$(LOGFILE) 2>&1; cd .. ; \
	done

srpm:
	@for dir in $(PKGS) ; do pushd $$dir ; make srpm ; popd ; done

clean:
	@for dir in $(PKGS) ; do pushd $$dir ; make clean ; popd ; done

rpmlint:
	@for dir in $(PKGS) ; do pushd $$dir ; make rpmlint ; popd ; done

repository:
	@echo -e "\033[1;32mUpdating repository on $(REPODIR)\033[0m"
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

dirlist:
	@echo "Processing directories: $(PKGS)"

help:
	@echo -e "\033[1;32mAvailable targets:\033[0m"
	@echo " - all:       Building all SRPM and RPMs and create repository (default target: ie when make is called without arg)"
	@echo " - repo:      Create or update local repository, and run repoview"
	@echo " - srpm:      Make SRPM"
	@echo " - build:     Make RPMs from SRPM"
	@echo " - clean:     Delete mock log files and all (S)RPMs"
