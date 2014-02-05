if ENABLE_PYTHON
plugins_multieditdir = $(plugindir)/multiedit
plugins_multiedit_PYTHON =					\
	plugins/multiedit/multiedit/__init__.py 		\
	plugins/multiedit/multiedit/appactivatable.py 	\
	plugins/multiedit/multiedit/windowactivatable.py 	\
	plugins/multiedit/multiedit/viewactivatable.py 		\
	plugins/multiedit/multiedit/signals.py

plugin_in_files += plugins/multiedit/multiedit.plugin.desktop.in
else
dist_plugin_in_files += plugins/multiedit/multiedit.plugin.desktop.in
endif
