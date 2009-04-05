#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.


AC_PREREQ(2.52)

m4_define([required_apertium_version], [3.0.0])

AC_INIT([apertium-bn-en], [0.1], [lkhatiwada@users.sourceforge.net])
AM_INIT_AUTOMAKE([apertium-bn-en], [0.1], no-define)
AC_PROG_LN_S
AC_PROG_AWK
AC_CONFIG_HEADER([config])

AC_DEFUN([PKG_CHECK_APERTIUM], [
  APERTIUM_VER=0
  PKG_CHECK_MODULES(APERTIUM, apertium-3.0 >= 3.0.0,
  [
    APERTIUM_VER=30
  ],
  [
    PKG_CHECK_MODULES(APERTIUM, apertium-3.1 >= 3.1.0)
    APERTIUM_VER=31
  ])
  AC_SUBST(APERTIUM_VER)
])

PKG_CHECK_APERTIUM

  
AC_OUTPUT([Makefile])
