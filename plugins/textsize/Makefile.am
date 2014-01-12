if ENABLE_PYTHON
plugins_textsizedir = $(plugindir)/textsize
plugins_textsize_PYTHON =				\
	plugins/textsize/textsize/__init__.py		\
	plugins/textsize/textsize/viewactivatable.py	\
	plugins/textsize/textsize/signals.py

plugin_in_files += plugins/textsize/textsize.plugin.desktop.in
else
dist_plugin_in_files += plugins/textsize/textsize.plugin.desktop.in
endif
