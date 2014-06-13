if ENABLE_GIT
plugins_gitdir = $(plugindir)/git
plugins_git_PYTHON =				\
	plugins/git/git/__init__.py		\
	plugins/git/git/diffrenderer.py		\
	plugins/git/git/viewactivatable.py	\
	plugins/git/git/windowactivatable.py

plugin_in_files += plugins/git/git.plugin.desktop.in
else
dist_plugin_in_files += plugins/git/git.plugin.desktop.in
endif

appdata_in_files += plugins/git/gedit-git.metainfo.xml.in
