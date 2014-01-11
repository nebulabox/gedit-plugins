if ENABLE_PYTHON
plugins_charmapdir = $(plugindir)/charmap
plugins_charmap_PYTHON =			\
	plugins/charmap/charmap/__init__.py	\
	plugins/charmap/charmap/panel.py

plugin_in_files += plugins/charmap/charmap.plugin.desktop.in
else
dist_plugin_in_files += plugins/charmap/charmap.plugin.desktop.in
endif
