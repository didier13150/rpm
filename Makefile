PKGS := arbaro chaplin fracplanet geomorph knock kpovmodeler mediawiki ossec-hids pam_usb povray shinken
REPODIR := /var/www/html/fedora-repo
LOGFILE := build.log
DISTRIB := $(shell source /etc/os-release && echo $${ID}-$${VERSION_ID})
ARCH := $(shell uname -i)
HOSTNAME := $(shell hostname --fqdn)

all: clean build repo repoview

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
	@for dir in $(PKGS) ; do cd $$dir ; make srpm ; cd .. ; done

clean:
	@for dir in $(PKGS) ; do cd $$dir ; make clean ; cd .. ; done

rpmlint:
	@for dir in $(PKGS) ; do cd $$dir ; make rpmlint ; cd .. ; done

repo:
	@echo -e "\033[1;32mUpdating repository on $(REPODIR)\033[0m"
	@for dir in $(PKGS) ; \
		do mkdir -p $(REPODIR)/$$dir ; \
		cp $$dir/*.rpm $$dir/{build,root,state}.log $(REPODIR)/$$dir/ ; \
	done
	@createrepo --update -d $(REPODIR)

repoview:
	repoview $(REPODIR) -o $(REPODIR)/repoview --url "http://$(HOSTNAME)/repoview" --title "RPM for $(DISTRIB) $(ARCH)"