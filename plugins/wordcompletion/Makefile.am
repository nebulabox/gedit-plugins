plugin_LTLIBRARIES += plugins/wordcompletion/libwordcompletion.la

plugins_wordcompletion_libwordcompletion_la_CPPFLAGS =		\
	-I$(top_srcdir)						\
	-I$(top_srcdir)/plugins/wordcompletion

plugins_wordcompletion_libwordcompletion_la_CFLAGS =		\
	$(GEDIT_CFLAGS) 					\
	$(WARN_CFLAGS)						\
	$(DISABLE_DEPRECATED_CFLAGS)

plugins_wordcompletion_libwordcompletion_la_LDFLAGS = $(PLUGIN_LIBTOOL_FLAGS)
plugins_wordcompletion_libwordcompletion_la_LIBADD = $(GEDIT_LIBS)

plugin_in_files += plugins/wordcompletion/wordcompletion.plugin.desktop.in

appdata_in_files += plugins/wordcompletion/gedit-wordcompletion.metainfo.xml.in

plugins_wordcompletion_resourcedeps =						\
	plugins/wordcompletion/gedit-word-completion.gresource.xml		\
	$(shell $(GLIB_COMPILE_RESOURCES) 					\
		--sourcedir=$(srcdir)/plugins/wordcompletion			\
		--generate-dependencies						\
		$(srcdir)/plugins/wordcompletion/gedit-word-completion.gresource.xml)

plugins/wordcompletion/gedit-word-completion-resources.c: $(plugins_wordcompletion_resourcedeps)
	$(AM_V_GEN) $(GLIB_COMPILE_RESOURCES)			\
		--target=$@					\
		--sourcedir=$(srcdir)/plugins/wordcompletion	\
		--generate-source $<

BUILT_SOURCES +=						\
	plugins/wordcompletion/gedit-word-completion-resources.c

plugins_wordcompletion_libwordcompletion_la_SOURCES =		\
	plugins/wordcompletion/gedit-word-completion-plugin.h	\
	plugins/wordcompletion/gedit-word-completion-plugin.c	\
	$(BUILT_SOURCES)

gsettings_SCHEMAS += plugins/wordcompletion/org.gnome.gedit.plugins.wordcompletion.gschema.xml

EXTRA_DIST += $(plugins_wordcompletion_resourcedeps)
