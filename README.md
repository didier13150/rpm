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

See http://fedoraproject.org/wiki/How_to_create_an_RPM_package for more informations.

then on each directory just type

 make

Sources will be automatically downloaded if they are not exists yet.

Common Makefile contains help target. So just type the following command to get help.

 make help
