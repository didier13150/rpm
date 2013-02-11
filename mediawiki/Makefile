SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
SRC := mediawiki-1.20.2.tar.gz
include ../common/Makefile
sources:
	[ -f $(SRC) ] || wget http://download.wikimedia.org/mediawiki/1.20/$(SRC)
	rm -f Math.tgz
	wget -O Math.tgz https://gerrit.wikimedia.org/r/gitweb?p=mediawiki/extensions/Math.git;a=snapshot;h=refs/heads/master;sf=tgz