========================================
 My personnal RPM repository for Fedora
========================================

How to use it
=============

You need a mock RPM build environment.

Short story
-----------

  # yum install mock rpmlint
  
  # usermod -a -G mock <USER>

See http://fedoraproject.org/wiki/How_to_create_an_RPM_package and http://fedoraproject.org/wiki/Projects/Mock for more informations.

Declare our repository to the current mock file by adding following lines
*  Fedora 19 x86_64 -> /etc/mock/fedora-19-x86_64.cfg
*  Fedora 19 i386 -> /etc/mock/fedora-19-i386.cfg

 [didier]
 name=didier
 baseurl=http://localhost/repository/
 cost=500

then on each directory just type

 make

Sources will be automatically downloaded if they are not exists yet.

Common Makefile contains help target. So just type the following command to get help.

 make help
