if ENABLE_PYTHON
plugins_translatedir = $(plugindir)/translate
plugins_translate_PYTHON = \
    plugins/translate/translate/__init__.py	\
	plugins/translate/translate/preferences.py	\
	plugins/translate/translate/translateview.py \
	plugins/translate/translate/settings.py

plugins_servicesdir = $(plugindir)/translate/services
dist_plugins_services_DATA = plugins/translate/translate/services/apertium.py \
	plugins/translate/translate/services/service.py \
	plugins/translate/translate/services/services.py \
	plugins/translate/translate/services/yandex.py

plugins_preferences_uidir = $(GEDIT_PLUGINS_DATA_DIR)/translate/ui
dist_plugins_preferences_ui_DATA = plugins/translate/translate/ui/preferences.ui

plugin_in_files += plugins/translate/translate.plugin.desktop.in
appstream_in_files += plugins/translate/gedit-translate.metainfo.xml.in
gsettings_SCHEMAS += plugins/translate/org.gnome.gedit.plugins.translate.gschema.xml
else
dist_plugin_in_files += plugins/translate/translate.plugin.desktop.in
dist_appstream_in_files += plugins/translate/gedit-translate.metainfo.xml.in
endif

