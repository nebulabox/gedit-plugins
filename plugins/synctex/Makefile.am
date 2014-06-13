if ENABLE_SYNCTEX
plugins_synctexdir = $(plugindir)/synctex
plugins_synctex_PYTHON =			\
	plugins/synctex/synctex/__init__.py	\
	plugins/synctex/synctex/synctex.py	\
	plugins/synctex/synctex/evince_dbus.py

plugin_in_files += plugins/synctex/synctex.plugin.desktop.in
else
dist_plugin_in_files += plugins/synctex/synctex.plugin.desktop.in
endif

appdata_in_files += plugins/synctex/gedit-synctex.metainfo.xml.in
