# -*- coding: utf-8 -*-
#
#  Copyrignt (C) 2017 Jordi Mas <jmas@softcatala.org>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110-1301, USA.

import os
from gi.repository import Gio, Gtk
import gettext
from gpdefs import *
from .services.services import Services
from .settings import Settings


class Preferences(object):

    LANG_NAME = 0
    LANG_CODE = 1

    def __init__(self, datadir, language_names, language_codes):
        object.__init__(self)
        self._language_codes = language_codes
        self._language_names = language_names

        self._settings = Settings()
        self._ui_path = os.path.join(datadir, 'ui', 'preferences.ui')
        self._ui = Gtk.Builder()
        self._ui.set_translation_domain(GETTEXT_PACKAGE)
        self._ui.add_from_file(self._ui_path)

        self._init_radiobuttons()
        self._init_combobox_languages()
        self._init_combobox_services()
        self._init_api_entry()

    def _init_api_entry(self):

        service_id = self._settings.get_service()
        service = Services.get(service_id)
        if service.has_api_key() is True:
            self._update_api_key_ui(True)
            return
        else:
            self._apikey = None
            return

    def _update_api_key_ui(self, show):
        apibox = self._ui.get_object('api_box')

        print("_update_api_key_ui show:" + str(show))
        if show is True:
            self._apilabel = Gtk.Label("API Key")
            self._apikey= Gtk.Entry(expand=True)

            self._apikey.connect('changed', self._changed_apikey)
            key = self._settings.get_apikey()
            self._apikey.set_text(key)

            apibox.add(self._apilabel)
            apibox.add(self._apikey)
            apibox.show_all()
        else:
            apibox.remove(self._apilabel)
            apibox.remove(self._apikey)
            self._apilabel = None
            self._apikey = None

    def _init_radiobuttons(self):
        self._radio_samedoc = self._ui.get_object('same_document')
        self._output_window = self._ui.get_object('output_window')
        self._radio_samedoc.connect("toggled", self._radio_samedoc_callback)
        active = self._settings.get_output_document()

        if active:
            self._radio_samedoc.set_active(active)
        else:
            self._output_window.set_active(active is False)

    def _init_combobox_services(self):
        self._services = self._ui.get_object('services')

        cell = Gtk.CellRendererText()
        self._services.pack_start(cell, 1)
        self._services.add_attribute(cell, 'text', 0)
        services = Services.get_names_and_ids()

        model = Gtk.ListStore(str, int)
        for service_id in services.keys():
            model.append((services[service_id], service_id))

        self._services.set_model(model)
        service_id = self._settings.get_service()
        self._services.set_active(service_id)
        self._services.connect('changed', self._changed_services)

    def _init_combobox_languages(self):
        self._languages = self._ui.get_object('languages')

        cell = Gtk.CellRendererText()
        self._languages.pack_start(cell, 1)
        self._languages.add_attribute(cell, 'text', 0)

        self._model = self._get_languages_stored_model()
        self._languages.set_model(self._model)
        self._languages.connect('changed', self._changed_lang_pair)

        selected = self._settings.get_language_pair()
        index = self._get_index(selected)
        self._languages.set_active(index)

    def _get_languages_stored_model(self):
        sorted_language_names = set()

        for i in range(len(self._language_names)):
            sorted_language_names.add((self._language_names[i], self._language_codes[i]))

        sorted_language_names = sorted(sorted_language_names,
                                       key=lambda tup: tup[Preferences.LANG_NAME])

        model = Gtk.ListStore(str, str)
        for name_code in sorted_language_names:
            model.append(name_code)

        return model

    def _get_index(self, selected):
        for i in range(len(self._model)):
            if self._model[i][Preferences.LANG_CODE] == selected:
                return i
        return -1

    def _changed_lang_pair(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        if index > -1:
            item = model[index]
            self._settings.set_language_pair(item[Preferences.LANG_CODE])

    def _changed_services(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        if index > -1:
            item = model[index]
            service_id = item[1]
            self._settings.set_service(service_id)
            service = Services.get(service_id)
            self._update_api_key_ui(service.has_api_key())

    def _changed_apikey(self, text_entry):
        text = text_entry.get_text()
        self._settings.set_apikey(text)

    def _radio_samedoc_callback(self, widget, data=None):
        self._settings.set_output_document(widget.get_active())

    def configure_widget(self):
        self._ui.connect_signals(self)
        widget = self._ui.get_object('grid')
        return widget
