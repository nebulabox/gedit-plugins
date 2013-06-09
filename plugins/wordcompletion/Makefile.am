# Word Completion plugin
plugindir = $(GEDIT_PLUGINS_LIBS_DIR)

INCLUDES = \
	-I$(top_srcdir) 				\
	$(GEDIT_CFLAGS) 				\
	$(WARN_CFLAGS)					\
	$(DISABLE_DEPRECATED_CFLAGS)

plugin_LTLIBRARIES = libwordcompletion.la

BUILT_SOURCES = \
	gedit-word-completion-resources.c

libwordcompletion_la_SOURCES = \
	gedit-word-completion-plugin.h				\
	gedit-word-completion-plugin.c				\
	$(BUILT_SOURCES)

libwordcompletion_la_LDFLAGS = $(PLUGIN_LIBTOOL_FLAGS)
libwordcompletion_la_LIBADD = $(GEDIT_LIBS)

gedit-word-completion-resources.c: gedit-word-completion.gresource.xml $(shell $(GLIB_COMPILE_RESOURCES) --sourcedir=$(srcdir) --generate-dependencies $(srcdir)/gedit-word-completion.gresource.xml)
	$(AM_V_GEN) $(GLIB_COMPILE_RESOURCES) --target=$@ --sourcedir=$(srcdir) --generate-source $(srcdir)/gedit-word-completion.gresource.xml

# Plugin Info

plugin_in_files = wordcompletion.plugin.desktop.in

%.plugin: %.plugin.desktop.in $(INTLTOOL_MERGE) $(wildcard $(top_srcdir)/po/*po) ; $(INTLTOOL_MERGE) $(top_srcdir)/po $< $@ -d -u -c $(top_builddir)/po/.intltool-merge-cache

plugin_DATA = $(plugin_in_files:.plugin.desktop.in=.plugin)

gsettings_SCHEMAS = org.gnome.gedit.plugins.wordcompletion.gschema.xml

@INTLTOOL_XML_NOMERGE_RULE@
@GSETTINGS_RULES@

EXTRA_DIST = \
	$(plugin_in_files) \
	org.gnome.gedit.plugins.wordcompletion.gschema.xml.in.in \
	gedit-word-completion.gresource.xml \
	gedit-word-completion-configure.ui

CLEANFILES = $(plugin_DATA)
DISTCLEANFILES = $(plugin_DATA)

-include $(top_srcdir)/git.mk
