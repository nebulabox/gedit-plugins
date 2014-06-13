plugin_LTLIBRARIES += plugins/bookmarks/libbookmarks.la

plugins_bookmarks_libbookmarks_la_CPPFLAGS =			\
	-I$(top_srcdir)						\
	-I$(top_srcdir)/plugins/bookmarks

plugins_bookmarks_libbookmarks_la_CFLAGS =			\
	$(GEDIT_CFLAGS) 					\
	$(WARN_CFLAGS)						\
	$(DISABLE_DEPRECATED_CFLAGS)

plugins_bookmarks_libbookmarks_la_LDFLAGS = $(PLUGIN_LIBTOOL_FLAGS)
plugins_bookmarks_libbookmarks_la_LIBADD = $(GEDIT_LIBS)

plugins_bookmarks_libbookmarks_la_SOURCES =					\
	plugins/bookmarks/gedit-bookmarks-plugin.h				\
	plugins/bookmarks/gedit-bookmarks-plugin.c				\
	plugins/bookmarks/gedit-bookmarks-app-activatable.h			\
	plugins/bookmarks/gedit-bookmarks-app-activatable.c			\
	plugins/bookmarks/messages/gedit-bookmarks-message-add.c		\
	plugins/bookmarks/messages/gedit-bookmarks-message-add.h		\
	plugins/bookmarks/messages/gedit-bookmarks-message-goto-next.c		\
	plugins/bookmarks/messages/gedit-bookmarks-message-goto-next.h		\
	plugins/bookmarks/messages/gedit-bookmarks-message-goto-previous.c	\
	plugins/bookmarks/messages/gedit-bookmarks-message-goto-previous.h	\
	plugins/bookmarks/messages/gedit-bookmarks-message-remove.c		\
	plugins/bookmarks/messages/gedit-bookmarks-message-remove.h		\
	plugins/bookmarks/messages/gedit-bookmarks-message-toggle.c		\
	plugins/bookmarks/messages/gedit-bookmarks-message-toggle.h		\
	plugins/bookmarks/messages/messages.h

plugin_in_files += plugins/bookmarks/bookmarks.plugin.desktop.in

appdata_in_files += plugins/bookmarks/gedit-bookmarks.metainfo.xml.in
