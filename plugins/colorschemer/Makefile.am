if ENABLE_PYTHON
plugins_schemerdir = $(plugindir)/schemer
plugins_schemer_PYTHON =				\
	plugins/colorschemer/schemer/__init__.py	\
	plugins/colorschemer/schemer/languages.py	\
	plugins/colorschemer/schemer/schemer.py

plugins_schemer_uidir = $(GEDIT_PLUGINS_DATA_DIR)/colorschemer/ui
dist_plugins_schemer_ui_DATA = plugins/colorschemer/schemer.ui

plugin_in_files += plugins/colorschemer/colorschemer.plugin.desktop.in
else
dist_plugin_in_files += plugins/colorschemer/colorschemer.plugin.desktop.in
endif
