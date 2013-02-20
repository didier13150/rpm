PKGS := arbaro chaplin fracplanet geomorph knock kpovmodeler mediawiki ossec-hids pam_usb povray shinken
REPODIR := /var/www/html/fedora-repo

all:
	@for dir in $(PKGS) ; do cd $$dir ; make ; cd .. ; done
	
srpm:
	@for dir in $(PKGS) ; do cd $$dir ; make srpm ; cd .. ; done

clean:
	@for dir in $(PKGS) ; do cd $$dir ; make clean ; cd .. ; done

repo:
	@echo -e "\033[1;32mUpdating repository on $(REPODIR)\033[0m"
	@for dir in $(PKGS) ; \
		do mkdir -p $(REPODIR)/$$dir ; \
		cp $$dir/*.rpm $$dir/{build,root,state}.log $(REPODIR)/$$dir/ ; \
	done
	@createrepo -u -d $(REPODIR)
