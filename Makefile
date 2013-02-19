PKGS := arbaro chaplin fracplanet geomorph knock kpovmodeler mediawiki ossec-hids pam_usb povray shinken

all:
	@for dir in $(PKGS) ; do cd $$dir ; make ; cd .. ; done
	
srpm:
	@for dir in $(PKGS) ; do cd $$dir ; make srpm ; cd .. ; done

clean:
	@for dir in $(PKGS) ; do cd $$dir ; make clean ; cd .. ; done
