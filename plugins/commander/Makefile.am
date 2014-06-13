if ENABLE_PYTHON
plugins_commanderdir = $(plugindir)/commander
plugins_commander_PYTHON =					\
	plugins/commander/commander/__init__.py			\
	plugins/commander/commander/entry.py			\
	plugins/commander/commander/history.py			\
	plugins/commander/commander/info.py			\
	plugins/commander/commander/modules.py			\
	plugins/commander/commander/transparentwindow.py	\
	plugins/commander/commander/utils.py			\
	plugins/commander/commander/appactivatable.py		\
	plugins/commander/commander/windowactivatable.py

plugins_commander_commandsdir = $(plugindir)/commander/commands
plugins_commander_commands_PYTHON =					\
	plugins/commander/commander/commands/__init__.py		\
	plugins/commander/commander/commands/accel_group.py		\
	plugins/commander/commander/commands/completion.py		\
	plugins/commander/commander/commands/exceptions.py		\
	plugins/commander/commander/commands/method.py			\
	plugins/commander/commander/commands/module.py			\
	plugins/commander/commander/commands/metamodule.py		\
	plugins/commander/commander/commands/result.py			\
	plugins/commander/commander/commands/rollbackimporter.py

plugins_commander_modulesdir = $(GEDIT_PLUGINS_DATA_DIR)/commander/modules
plugins_commander_modules_PYTHON =			\
	plugins/commander/modules/align.py		\
	plugins/commander/modules/bookmark.py		\
	plugins/commander/modules/doc.py		\
	plugins/commander/modules/edit.py		\
	plugins/commander/modules/format.py		\
	plugins/commander/modules/goto.py		\
	plugins/commander/modules/grep.py		\
	plugins/commander/modules/help.py		\
	plugins/commander/modules/move.py		\
	plugins/commander/modules/reload.py		\
	plugins/commander/modules/set.py		\
	plugins/commander/modules/shell.py

plugins_commander_modules_finddir = $(GEDIT_PLUGINS_DATA_DIR)/commander/modules/find
plugins_commander_modules_find_PYTHON =			\
	plugins/commander/modules/find/__init__.py	\
	plugins/commander/modules/find/finder.py	\
	plugins/commander/modules/find/regex.py

plugin_in_files += plugins/commander/commander.plugin.desktop.in
else
dist_plugin_in_files += plugins/commander/commander.plugin.desktop.in
endif

appdata_in_files += plugins/commander/gedit-commander.metainfo.xml.in
