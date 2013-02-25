========================================
 My personnal RPM repository for Fedora
========================================

How to use it
-------------

You need a mock RPM build environment. see http://fedoraproject.org/wiki/How_to_create_an_RPM_package for more informations.

then on each directory just type

 make

Sources will be automatically downloaded if they are not exists yet.

Common Makefile contains help target. So just type the following command to get help.

 make help

Some packages ( hfc, jpatch for now ) need additionnal build dependancies available on jpackage website. For more informations about installing the jpackage repository, see http://www.jpackage.org/yum.php