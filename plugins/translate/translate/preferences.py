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


class Preferences(object):

    TRANSLATE_KEY_BASE = 'org.gnome.gedit.plugins.translate'
    OUTPUT_TO_DOCUMENT = 'output-to-document'
    LANGUAGE_PAIR = 'language-pair'
    LANG_NAME = 0
    LANG_CODE = 1

    def __init__(self, datadir, language_names, language_codes):
        object.__init__(self)
        self._language_codes = language_codes
        self._language_names = language_names

        self._settings = Gio.Settings.new(self.TRANSLATE_KEY_BASE)
        self._ui_path = os.path.join(datadir, 'ui', 'preferences.ui')
        self._ui = Gtk.Builder()
        self._ui.add_from_file(self._ui_path)

        self.init_radiobuttons()
        self.init_combobox()

    def init_radiobuttons(self):

        self._radio_samedoc = self._ui.get_object('same_document')
        self._output_window = self._ui.get_object('output_window')
        active = self._settings.get_boolean(self.OUTPUT_TO_DOCUMENT)

        if active:
            self._radio_samedoc.set_active(active)
        else:
            self._output_window.set_active(active is False)

    def init_combobox(self):
        self._languages = self._ui.get_object('languages')

        cell = Gtk.CellRendererText()
        self._languages.pack_start(cell, 1)
        self._languages.add_attribute(cell, 'text', 0)

        self._model = self._get_stored_model()
        self._languages.set_model(self._model)
        self._languages.connect('changed', self.changed_cb)

        selected = self._settings.get_string(self.LANGUAGE_PAIR)
        index = self.get_index(selected)
        self._languages.set_active(index)

    def _get_stored_model(self):
        sorted_language_names = set()

        for i in range(len(self._language_names)):
            sorted_language_names.add((self._language_names[i], self._language_codes[i]))

        sorted_language_names = sorted(sorted_language_names,
                                       key=lambda tup: tup[Preferences.LANG_NAME])

        model = Gtk.ListStore(str, str)
        for name_code in sorted_language_names:
            model.append(name_code)

        return model

    def get_index(self, selected):
        for i in range(len(self._model)):
            if self._model[i][Preferences.LANG_CODE] == selected:
                return i
        return -1

    def changed_cb(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        if index > -1:
            item = model[index]
            self._settings.set_string(self.LANGUAGE_PAIR, item[Preferences.LANG_CODE])
        return

    def set_output_to_doc(self, active):
        self._settings.set_boolean(self.OUTPUT_TO_DOCUMENT, active)

    def radio_samedoc_callback(self, widget, data=None):
        self.set_output_to_doc(widget.get_active())

    def configure_widget(self):
        self._ui.connect_signals(self)
        self._radio_samedoc.connect("toggled", self.radio_samedoc_callback)

        widget = self._ui.get_object('grid')
        return widget

