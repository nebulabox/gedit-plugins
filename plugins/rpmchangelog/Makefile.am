if ENABLE_PYTHON
plugin_PYTHON +=	plugins/rpmchangelog/rpmchangelog.py
plugin_in_files += plugins/rpmchangelog/rpmchangelog.plugin.desktop.in
appstream_in_files += plugins/rpmchangelog/gedit-rpmchangelog.metainfo.xml.in
gsettings_SCHEMAS += plugins/rpmchangelog/org.gnome.gedit.plugins.rpmchangelog.gschema.xml
else
dist_plugin_in_files += plugins/rpmchangelog/rpmchangelog.plugin.desktop.in
dist_appstream_in_files += plugins/rpmchangelog/gedit-rpmchangelog.metainfo.xml.in
dist_gsettings_SCHEMAS += plugins/rpmchangelog/org.gnome.gedit.plugins.rpmchangelog.gschema.xml
endif
