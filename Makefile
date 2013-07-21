PKGS := $(shell ls -l | grep ^d | grep -v common | grep -v doc | awk '{print $$9}')
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
	@for dir in $(PKGS) ; do cd $$dir ; make srpm ; cd .. ; done

clean:
	@for dir in $(PKGS) ; do cd $$dir ; make clean ; cd .. ; done

rpmlint:
	@for dir in $(PKGS) ; do cd $$dir ; make rpmlint ; cd .. ; done

repository:
	@echo -e "\033[1;32mUpdating repository on $(REPODIR)\033[0m"
	@for dir in $(PKGS) ; \
		do mkdir -p $(REPODIR)/$$dir ; \
		cp $$dir/result/*.rpm $(REPODIR)/$$dir/ || true; \
	done
	@createrepo --update -d $(REPODIR)

repoview:
	repoview $(REPODIR) -o $(REPODIR)/repoview --url "http://$(HOSTNAME)/repoview" --title "RPM for $(DISTRIB) $(ARCH)"

dirlist:
	@echo "Processing directories: $(PKGS)"
