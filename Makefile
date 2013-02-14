PKGS := chaplin fracplanet knock kpovmodeler ossec-hids pam_usb povray
#not working yet: mediawiki shinken

all:
	@for dir in $(PKGS) ; do cd $$dir ; make ; cd .. ; done
	
srpm:
	@for dir in $(PKGS) ; do cd $$dir ; make srpm ; cd .. ; done

clean:
	@for dir in $(PKGS) ; do cd $$dir ; make clean ; cd .. ; done
