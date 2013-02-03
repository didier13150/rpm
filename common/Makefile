RPMDEFINES := --define "_sourcedir $(SRCDIR)" \
              --define "_specdir $(SRCDIR)" \
              --define "_srcrpmdir $(SRCDIR)" \
              --define "_rpmdir $(SRCDIR)"

SRCDEFINES := --define "_source_filedigest_algorithm 1" \
              --define "_binary_filedigest_algorithm 1"

ARCH := $(shell uname -i)
DISTRIB := $(shell source /etc/os-release && echo $${ID}-$${VERSION_ID})
TARGET := $(DISTRIB)-$(ARCH)

all: fedora

fedora: clean sources build log

clean:
	@echo Clean $(NAME) in $(SRCDIR)
	@rm -rfv *~ *.log *.rpm

rpmlint:
	rpmlint *.spec
	rpmlint *.rpm

sources:
	@if test -f $(SRCFILE); then \
		echo "$(SRCFILE) already exists"; \
	else \
		echo "Download Source $(SRCURL)"; \
		$(shell $(DOWNLOAD)) \
	fi

srpm: sources
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME).spec

build: srpm
	-mock -r '$(TARGET)' rebuild *.src.rpm
	-mv /var/lib/mock/$(TARGET)/result/*.rpm $(SRCDIR)

log:
	@mv /var/lib/mock/$(TARGET)/result/*.log $(SRCDIR)
