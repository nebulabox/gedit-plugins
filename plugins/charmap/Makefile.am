if ENABLE_CHARMAP
plugins_charmapdir = $(plugindir)/charmap
plugins_charmap_PYTHON =			\
	plugins/charmap/charmap/__init__.py	\
	plugins/charmap/charmap/panel.py

plugin_in_files += plugins/charmap/charmap.plugin.desktop.in
appstream_in_files += plugins/charmap/gedit-charmap.metainfo.xml.in
else
dist_plugin_in_files += plugins/charmap/charmap.plugin.desktop.in
dist_appstream_in_files += plugins/charmap/gedit-charmap.metainfo.xml.in
endif
