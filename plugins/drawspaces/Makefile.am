plugin_LTLIBRARIES += plugins/drawspaces/libdrawspaces.la

plugins_drawspaces_libdrawspaces_la_CPPFLAGS =			\
	-I$(top_srcdir)						\
	-I$(top_srcdir)/plugins/drawspaces

plugins_drawspaces_libdrawspaces_la_CFLAGS =			\
	$(GEDIT_CFLAGS) 					\
	$(WARN_CFLAGS)						\
	$(DISABLE_DEPRECATED_CFLAGS)

plugins_drawspaces_libdrawspaces_la_LDFLAGS = $(PLUGIN_LIBTOOL_FLAGS)
plugins_drawspaces_libdrawspaces_la_LIBADD = $(GEDIT_LIBS)

plugins_drawspaces_resourcedeps =						\
	plugins/drawspaces/gedit-drawspaces.gresource.xml			\
	$(shell $(GLIB_COMPILE_RESOURCES) 					\
		--sourcedir=$(srcdir)/plugins/drawspaces			\
		--generate-dependencies						\
		$(srcdir)/plugins/drawspaces/gedit-drawspaces.gresource.xml)

plugins/drawspaces/gedit-drawspaces-resources.c: $(plugins_drawspaces_resourcedeps)
	$(AM_V_GEN) $(GLIB_COMPILE_RESOURCES)			\
		--target=$@					\
		--sourcedir=$(srcdir)/plugins/drawspaces	\
		--generate-source $<

BUILT_SOURCES +=						\
	plugins/drawspaces/gedit-drawspaces-resources.c

plugins_drawspaces_libdrawspaces_la_SOURCES =			\
	plugins/drawspaces/gedit-drawspaces-plugin.h		\
	plugins/drawspaces/gedit-drawspaces-plugin.c		\
	plugins/drawspaces/gedit-drawspaces-app-activatable.h	\
	plugins/drawspaces/gedit-drawspaces-app-activatable.c	\
	$(BUILT_SOURCES)

plugin_in_files += plugins/drawspaces/drawspaces.plugin.desktop.in
gsettings_SCHEMAS += plugins/drawspaces/org.gnome.gedit.plugins.drawspaces.gschema.xml

EXTRA_DIST += 							\
	plugins/drawspaces/gedit-drawspaces.gresource.xml	\
	plugins/drawspaces/gedit-drawspaces-plugin.ui
