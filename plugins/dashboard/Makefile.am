if ENABLE_PYTHON
plugins_dashboarddir = $(plugindir)/dashboard
plugins_dashboard_PYTHON =				\
	plugins/dashboard/dashboard/__init__.py		\
	plugins/dashboard/dashboard/dashboard.py	\
	plugins/dashboard/dashboard/utils.py

plugin_in_files += plugins/dashboard/dashboard.plugin.desktop.in
else
dist_plugin_in_files += plugins/dashboard/dashboard.plugin.desktop.in
endif

appdata_in_files += plugins/dashboard/gedit-dashboard.metainfo.xml.in
