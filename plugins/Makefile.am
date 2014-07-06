plugindir = $(GEDIT_PLUGINS_LIBS_DIR)

if ENABLE_PYTHON
plugin_PYTHON = plugins/gpdefs.py
endif

plugin_LTLIBRARIES =
plugin_in_files =
dist_plugin_in_files =
appstreamdir = $(datadir)/appdata/
appstream_in_files =
dist_appstream_in_files =
gsettings_SCHEMAS =
dist_gsettings_SCHEMAS =

include plugins/bookmarks/Makefile.am
include plugins/bracketcompletion/Makefile.am
include plugins/charmap/Makefile.am
include plugins/codecomment/Makefile.am
include plugins/colorpicker/Makefile.am
include plugins/colorschemer/Makefile.am
include plugins/commander/Makefile.am
include plugins/dashboard/Makefile.am
include plugins/drawspaces/Makefile.am
include plugins/git/Makefile.am
include plugins/joinlines/Makefile.am
include plugins/multiedit/Makefile.am
include plugins/rpmchangelog/Makefile.am
include plugins/smartspaces/Makefile.am
include plugins/synctex/Makefile.am
include plugins/terminal/Makefile.am
include plugins/textsize/Makefile.am
include plugins/wordcompletion/Makefile.am
include plugins/zeitgeist/Makefile.am

@INTLTOOL_XML_NOMERGE_RULE@
@GSETTINGS_RULES@

%.plugin: %.plugin.desktop.in $(INTLTOOL_MERGE) $(wildcard $(top_srcdir)/po/*po) ; $(INTLTOOL_MERGE) $(top_srcdir)/po $< $@ -d -u -c $(top_builddir)/po/.intltool-merge-cache

GENERATED_PLUGIN_FILES = $(plugin_in_files:.plugin.desktop.in=.plugin)

plugin_DATA = $(GENERATED_PLUGIN_FILES)

GENERATED_APPSTREAM_FILES = $(appstream_in_files:.xml.in=.xml)

appstream_DATA = $(GENERATED_APPSTREAM_FILES)

DISTCLEANFILES +=			\
	plugins/gpdefs.py		\
	$(GENERATED_PLUGIN_FILES)	\
	$(GENERATED_APPDATA_FILES)

CLEANFILES +=				\
	$(GENERATED_PLUGIN_FILES)	\
	$(GENERATED_APPSTREAM_FILES)	\
	$(gsettings_SCHEMAS)

EXTRA_DIST +=								\
	plugins/gpdefs.py.in						\
	$(plugin_in_files)						\
	$(dist_plugin_in_files)						\
	$(appstream_in_files)						\
	$(dist_appstream_in_files)					\
	$(gsettings_SCHEMAS:%.gschema.xml=%.gschema.xml.in.in)		\
	$(dist_gsettings_SCHEMAS:%.gschema.xml=%.gschema.xml.in.in)
