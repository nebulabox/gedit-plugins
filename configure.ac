dnl Process this file with autoconf to produce a configure script.

AC_PREREQ([2.63])

m4_define(gedit_plugins_major_version, 3)
m4_define(gedit_plugins_minor_version, 27)
m4_define(gedit_plugins_micro_version, 92)
m4_define(gedit_plugins_version, gedit_plugins_major_version.gedit_plugins_minor_version.gedit_plugins_micro_version)

AC_INIT([gedit-plugins],
        [gedit_plugins_version],
        [http://bugzilla.gnome.org/enter_bug.cgi?product=gedit],
        [gedit-plugins])

AC_CONFIG_HEADERS([config.h])
AC_CONFIG_SRCDIR([plugins])
AC_CONFIG_MACRO_DIR([m4])
AC_PREFIX_PROGRAM([gedit])

AM_INIT_AUTOMAKE([1.11 tar-ustar dist-xz no-dist-gzip subdir-objects -Wno-portability])
AM_MAINTAINER_MODE([enable])

AM_SILENT_RULES([yes])

# Check for programs
AC_PROG_CC
AC_PROG_INSTALL
AC_PROG_MAKE_SET

# Initialize libtool
LT_PREREQ([2.2])
LT_INIT([disable-static])

dnl check for win32 platform
AC_MSG_CHECKING([for some Win32 platform])
case "$host" in
  *-*-mingw*|*-*-cygwin*)
    platform_win32=yes
    ;;
  *)
    platform_win32=no
    ;;
esac
AC_MSG_RESULT([$platform_win32])
AM_CONDITIONAL(PLATFORM_WIN32, test "$platform_win32" = "yes")

IT_PROG_INTLTOOL([0.50.2])

AM_GNU_GETTEXT_VERSION([0.17])
AM_GNU_GETTEXT([external])

GETTEXT_PACKAGE=gedit-plugins
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE,"$GETTEXT_PACKAGE", [Gettext package])

PKG_CHECK_MODULES(GEDIT, [
	glib-2.0 >= 2.32.0
	gio-2.0 >= 2.32.0
	gtk+-3.0 >= 3.9.0
	gtksourceview-3.0 >= 3.21.3
	libpeas-1.0 >= 1.7.0
	libpeas-gtk-1.0 >= 1.7.0
	gedit >= 3.16.0
])

GLIB_GSETTINGS

# C plugins that don't need special dependencies
C_PLUGINS="bookmarks drawspaces wordcompletion"

# Python plugins that don't need special dependencies, besides Python
PY_PLUGINS="bracketcompletion codecomment colorpicker colorschemer commander joinlines multiedit smartspaces textsize translate"

# Vala plugins that don't need special dependencies, besides Vala
VALA_PLUGINS="findinfiles"

PLUGINS="$C_PLUGINS"
disabled_plugins=""

# Check all plugins are built
AC_ARG_ENABLE([verify-all],
              AC_HELP_STRING([--enable-verify-all], [verify that all plugins are enabled]),
              [enable_verify_all=$enableval],
              [enable_verify_all="no"])

# Python
AC_MSG_CHECKING([whether Python support is requested])
AC_ARG_ENABLE([python],
              AS_HELP_STRING([--enable-python], [Enable Python support]),
              [enable_python=$enableval],
              [enable_python=auto])
AC_MSG_RESULT([$enable_python])

if test "x$enable_python" != "xno"
then
	AM_PATH_PYTHON(3, [have_python=yes], [have_python=no])
	if test "x$enable_python" = "xyes" -a "x$have_python" = "xno"; then
		AC_MSG_ERROR([Python support explicitly requested, but not found])
	fi
fi

AM_CONDITIONAL([ENABLE_PYTHON], [test "x$have_python" = "xyes"])

# Vala
AC_MSG_CHECKING([whether Vala support is requested])
AC_ARG_ENABLE([vala],
              AS_HELP_STRING([--enable-vala], [Enable Vala support]),
              [enable_vala=$enableval],
              [enable_vala=auto])
AC_MSG_RESULT([$enable_vala])

if test "x$enable_vala" != "xno"
then
	# This could probably be lower, but let's take the current version
	VALA_REQUIRED=0.28.0
	AM_PROG_VALAC([$VALA_REQS])
	if test "x$VALAC" = "x"; then
		if test "x$enable_vala" = "xyes"; then
			AC_MSG_ERROR([Vala support explicitly requested, but not found])
		fi
		have_vala=no
	else
		have_vala=yes
	fi
else
	have_vala=no
fi

AM_CONDITIONAL([ENABLE_VALA], [test "x$have_vala" = "xyes"])

# zeitgeist (libzeitgeist)
AC_MSG_CHECKING([whether Zeitgeist support is requested])
AC_ARG_ENABLE([zeitgeist],
              AS_HELP_STRING([--enable-zeitgeist], [Enable zeitgeist support]),
              [enable_zeitgeist=$enableval],
              [enable_zeitgeist=auto])
AC_MSG_RESULT([$enable_zeitgeist])

if test "x$enable_zeitgeist" != "xno"
then
	LIBZEITGEIST_REQUIRED=0.9.12
	PKG_CHECK_MODULES([ZEITGEIST], \
		[zeitgeist-2.0 >= $LIBZEITGEIST_REQUIRED],
		[have_zeitgeist=yes],
		[have_zeitgeist=no])
	if test "x$enable_zeitgeist" = "xyes" -a "x$have_zeitgeist" = "xno"; then
		AC_MSG_ERROR([Zeitgeist support explicitly requested, but not found])
	fi
else
	have_zeitgeist=no
fi

if test "x$have_zeitgeist" = "xyes"; then
	PLUGINS="$PLUGINS zeitgeist"
else
	disabled_plugins="$disabled_plugins zeitgeist"
fi

AM_CONDITIONAL([ENABLE_ZEITGEIST], [test "x$have_zeitgeist" = "xyes"])

# disable all python plugins if there is no python support
if test "x$have_python" = "xyes"
then
	PLUGINS="$PLUGINS $PY_PLUGINS"

	# Synctex (dbus-python)
	DBUSPYTHON_REQUIRED=0.82
	PKG_CHECK_MODULES([DBUSPYTHON],
		[dbus-python >= $DBUSPYTHON_REQUIRED],
		[have_synctex=yes],
		[have_synctex=no])

	AC_SUBST([DBUS_PYTHON_CFLAGS])
	AC_SUBST([DBUS_PYTHON_LIBS])

	AC_MSG_CHECKING([for synctex dependency dbus-python])
	AC_MSG_RESULT($have_synctex)

	if test "x$have_synctex" = "xyes"; then
		PLUGINS="$PLUGINS synctex"
	else
		AC_MSG_RESULT([yes])
		disabled_plugins="$disabled_plugins synctex (dbus-python not found)"
	fi

	# Terminal (vte)
	AC_MSG_CHECKING([for terminal dependency vte])

	if `$PYTHON -c "import gi; gi.require_version('Vte', '2.91')" 2>/dev/null`;
	then
		have_vte=yes
		PLUGINS="$PLUGINS terminal"
	else
		have_vte=no
		disabled_plugins="$disabled_plugins terminal (vte not found)"
	fi

	AC_MSG_RESULT($have_vte)

	# Dashboard (Zeitgeist)
	if test "x$have_zeitgeist" = "xyes"
	then
		AC_MSG_CHECKING([for dashboard dependency zeitgeist])
		if `$PYTHON -c "import gi; gi.require_version('Zeitgeist', '2.0')" 2>/dev/null`;
		then
			have_dashboard=yes
			PLUGINS="$PLUGINS dashboard"
		else
			have_dashboard=no
			disabled_plugins="$disabled_plugins dashboard (Zeitgeist gi not found)"
		fi
	else
		have_dashboard=no
		disabled_plugins="$disabled_plugins dashboard (Zeitgeist disabled)"
	fi

	AC_MSG_RESULT($have_dashboard)

	# Charmap (Gucharmap)
	AC_MSG_CHECKING([for charmap dependency gucharmap])
	if `$PYTHON -c "import gi; gi.require_version('Gucharmap', '2.90')" 2>/dev/null`;
	then
		have_gucharmap=yes
		PLUGINS="$PLUGINS charmap"
	else
		have_gucharmap=no
		disabled_plugins="$disabled_plugins charmap (Gucharmap gi not found)"
	fi

	AC_MSG_RESULT($have_gucharmap)

	# Git (libgit2-glib)
	LIBGIT2_GLIB_REQUIRED=0.0.6
	PKG_CHECK_MODULES([GIT2_GLIB],
		[libgit2-glib-1.0 >= $LIBGIT2_GLIB_REQUIRED],
		[have_git2=yes],
		[have_git2=no])

	AC_MSG_CHECKING([for git dependency libgit2-glib])
	AC_MSG_RESULT($have_git2)

	if test "x$have_git2" = "xyes"; then
		PLUGINS="$PLUGINS git"
	else
		disabled_plugins="$disabled_plugins git"
	fi
else
	disabled_plugins="$disabled_plugins $PY_PLUGINS synctex terminal dashboard charmap git (python not found)"
fi

AM_CONDITIONAL([ENABLE_SYNCTEX], test "x$have_synctex" = "xyes")
AM_CONDITIONAL([ENABLE_TERMINAL], test "x$have_vte" = "xyes")
AM_CONDITIONAL([ENABLE_DASHBOARD], test "x$have_dashboard" = "xyes")
AM_CONDITIONAL([ENABLE_CHARMAP], test "x$have_gucharmap" = "xyes")
AM_CONDITIONAL([ENABLE_GIT], test "x$have_git2" = "xyes")

# disable all Vala plugins if there is no Vala support
if test "x$have_vala" = "xyes"; then
	PLUGINS="$PLUGINS $VALA_PLUGINS"
else
	disabled_plugins="$disabled_plugins $VALA_PLUGINS"
fi

AC_SUBST(PLUGINS)

# ================================================================
# Misc
# ================================================================
AC_PATH_PROG(GLIB_COMPILE_RESOURCES, glib-compile-resources)
AC_PATH_PROG(GLIB_GENMARSHAL, glib-genmarshal)

YELP_HELP_INIT

AC_ARG_ENABLE(deprecations,
              [AS_HELP_STRING([--enable-deprecations],
                              [warn about deprecated usages [default=no]])],,
              [enable_deprecations=no])

if test "x$enable_deprecations" = "xyes"
then
	DISABLE_DEPRECATED_CFLAGS="\
		-DG_DISABLE_DEPRECATED		\
		-DGDK_DISABLE_DEPRECATED	\
		-DGTK_DISABLE_DEPRECATED	\
		-DGDK_PIXBUF_DISABLE_DEPRECATED	\
		-DGNOME_DISABLE_DEPRECATED"
	AC_SUBST(DISABLE_DEPRECATED_CFLAGS)
fi

if test "$platform_win32" = yes; then
	PLUGIN_LIBTOOL_FLAGS="-module -avoid-version -no-undefined"
else
	PLUGIN_LIBTOOL_FLAGS="-module -avoid-version"
fi
AC_SUBST(PLUGIN_LIBTOOL_FLAGS)

GEDIT_PLUGINS_LIBS_DIR="$libdir/gedit/plugins"
AC_SUBST(GEDIT_PLUGINS_LIBS_DIR)

GEDIT_PLUGINS_DATA_DIR="$datadir/gedit/plugins"
AC_SUBST(GEDIT_PLUGINS_DATA_DIR)

if test "x$enable_verify_all" != "xno" && test ! -z "$disabled_plugins"; then
AC_MSG_ERROR([some plugins are not being built: $disabled_plugins])
fi

AC_CONFIG_FILES([
Makefile
help/Makefile
plugins/gpdefs.py
plugins/bookmarks/bookmarks.plugin.desktop.in
plugins/bracketcompletion/bracketcompletion.plugin.desktop.in
plugins/charmap/charmap.plugin.desktop.in
plugins/codecomment/codecomment.plugin.desktop.in
plugins/colorpicker/colorpicker.plugin.desktop.in
plugins/colorschemer/colorschemer.plugin.desktop.in
plugins/commander/commander.plugin.desktop.in
plugins/dashboard/dashboard.plugin.desktop.in
plugins/drawspaces/drawspaces.plugin.desktop.in
plugins/findinfiles/findinfiles.plugin.desktop.in
plugins/git/git.plugin.desktop.in
plugins/joinlines/joinlines.plugin.desktop.in
plugins/multiedit/multiedit.plugin.desktop.in
plugins/smartspaces/smartspaces.plugin.desktop.in
plugins/synctex/synctex.plugin.desktop.in
plugins/terminal/terminal.plugin.desktop.in
plugins/textsize/textsize.plugin.desktop.in
plugins/translate/translate.plugin.desktop.in
plugins/wordcompletion/wordcompletion.plugin.desktop.in
po/Makefile.in])

AC_OUTPUT

echo "

Configuration:

	Source code location:   ${srcdir}
	Compiler:               ${CC}
	Prefix:                 ${prefix}
	Python Plugins Support: ${have_python}
	Vala Plugins Support:   ${have_vala}

	Plugins:
	  ${PLUGINS}

	Disabled plugins:
	  ${disabled_plugins}

Note: you have to install these plugins into the same prefix as your gedit
installation (probably /usr if you're using your distro packages, /usr/local
if you have compiled it on your own).
"

