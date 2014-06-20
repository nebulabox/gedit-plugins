if ENABLE_PYTHON
plugins_textsizedir = $(plugindir)/textsize
plugins_textsize_PYTHON =				\
	plugins/textsize/textsize/__init__.py		\
	plugins/textsize/textsize/viewactivatable.py	\
	plugins/textsize/textsize/signals.py

plugin_in_files += plugins/textsize/textsize.plugin.desktop.in
appstream_in_files += plugins/textsize/gedit-textsize.metainfo.xml.in
else
dist_plugin_in_files += plugins/textsize/textsize.plugin.desktop.in
dist_appstream_in_files += plugins/textsize/gedit-textsize.metainfo.xml.in
endif
