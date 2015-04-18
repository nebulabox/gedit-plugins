if ENABLE_VALA

plugin_LTLIBRARIES += plugins/findinfiles/libfindinfiles.la

plugins_findinfiles_libfindinfiles_la_CPPFLAGS =	\
	-DGETTEXT_PACKAGE=\""$(GETTEXT_PACKAGE)"\"	\
	-DGP_LOCALEDIR=\""$(localedir)"\"		\
	-I$(top_srcdir)					\
	-I$(top_srcdir)/plugins/findinfiles

plugins_findinfiles_libfindinfiles_la_CFLAGS =	\
	$(GEDIT_CFLAGS)				\
	$(WARN_CFLAGS)				\
	$(DISABLE_DEPRECATED_CFLAGS)

plugins_findinfiles_libfindinfiles_la_VALAFLAGS =	\
	--vapidir $(top_srcdir)/plugins			\
	--pkg config					\
	--pkg gedit					\
	--pkg PeasGtk-1.0				\
	--pkg GtkSource-3.0				\
	--pkg gtk+-3.0					\
	--pkg gio-2.0					\
	--pkg posix					\
	--target-glib=2.38				\
	--gresources=$(top_srcdir)/plugins/findinfiles/findinfiles.gresource.xml

plugins_findinfiles_libfindinfiles_la_LDFLAGS = $(PLUGIN_LIBTOOL_FLAGS)
plugins_findinfiles_libfindinfiles_la_LIBADD = $(GEDIT_LIBS)

VALASOURCES =					\
	plugins/findinfiles/dialog.vala		\
	plugins/findinfiles/job.vala		\
	plugins/findinfiles/matcher.vala	\
	plugins/findinfiles/plugin.vala		\
	plugins/findinfiles/result-panel.vala

BUILT_SOURCES +=				\
	plugins/findinfiles/resources.c

resource_files = $(shell $(GLIB_COMPILE_RESOURCES)					\
			--generate-dependencies						\
			--sourcedir=$(top_srcdir)/plugins/findinfiles/			\
			$(top_srcdir)/plugins/findinfiles/findinfiles.gresource.xml)

plugins/findinfiles/resources.c: $(top_srcdir)/plugins/findinfiles/findinfiles.gresource.xml $(resource_files)
	$(AM_V_GEN) $(GLIB_COMPILE_RESOURCES) --target=$@ --sourcedir=$(top_srcdir)/plugins/findinfiles/ --generate-source $<

plugins_findinfiles_libfindinfiles_la_SOURCES =	\
	$(VALASOURCES)				\
	$(BUILT_SOURCES)

plugin_in_files += plugins/findinfiles/findinfiles.plugin.desktop.in
appstream_in_files += plugins/findinfiles/gedit-findinfiles.metainfo.xml.in

EXTRA_DIST +=						\
	$(resource_files)				\
	plugins/findinfiles/dialog.ui			\
	plugins/findinfiles/findinfiles.gresource.xml

else
dist_plugin_in_files += plugins/findinfiles/findinfiles.plugin.desktop.in
dist_appstream_in_files += plugins/findinfiles/gedit-findinfiles.metainfo.xml.in
endif
