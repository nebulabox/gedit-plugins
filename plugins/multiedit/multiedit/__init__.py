# -*- coding: utf-8 -*-
#
#  multiedit.py - Multi Edit
#
#  Copyright (C) 2009 - Jesse van den Kieboom
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

from gi.repository import GLib, GObject, Gio, Gtk, Gedit
from .signals import Signals
from .documenthelper import DocumentHelper
import gettext
from gpdefs import *

try:
    gettext.bindtextdomain(GETTEXT_PACKAGE, GP_LOCALEDIR)
    _ = lambda s: gettext.dgettext(GETTEXT_PACKAGE, s);
except:
    _ = lambda s: s


class MultiEditAppActivatable(GObject.Object, Gedit.AppActivatable):

    app = GObject.property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self.app.add_accelerator("<Primary><Shift>C", "win.multiedit", None)

    def do_deactivate(self):
        self.app.remove_accelerator("win.multiedit", None)

class MultiEditWindowActivatable(GObject.Object, Gedit.WindowActivatable, Signals):

    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)
        Signals.__init__(self)

    def do_activate(self):
        for view in self.window.get_views():
            self.add_document_helper(view)

        self.connect_signal(self.window, 'tab-added', self.on_tab_added)
        self.connect_signal(self.window, 'tab-removed', self.on_tab_removed)
        self.connect_signal(self.window, 'active-tab-changed', self.on_active_tab_changed)

        self._insert_menu()

    def do_deactivate(self):
        self.disconnect_signals(self.window)

        for view in self.window.get_views():
            self.remove_document_helper(view)

        self._remove_menu()

    def _insert_menu(self):
        action = Gio.SimpleAction.new_stateful("multiedit", None, GLib.Variant.new_boolean(False))
        action.connect('activate', self.activate_toggle)
        action.connect('change-state', self.multi_edit_mode)
        self.window.add_action(action)

        self.menu = self.extend_gear_menu("ext9")
        item = Gio.MenuItem.new(_('Multi Edit Mode'), "win.multiedit")
        self.menu.append_menu_item(item)

    def _remove_menu(self):
        self.window.remove_action("multiedit")

    def do_update_state(self):
        pass

    def get_helper(self, view):
        if not hasattr(view, "multiedit_document_helper"):
            return None
        return view.multiedit_document_helper

    def add_document_helper(self, view):
        if self.get_helper(view) != None:
            return

        helper = DocumentHelper(view)
        helper.set_toggle_callback(self.on_multi_edit_toggled, helper)

    def remove_document_helper(self, view):
        helper = self.get_helper(view)

        if helper != None:
            helper.stop()

    def get_action(self):
        return self.window.lookup_action("multiedit")

    def on_multi_edit_toggled(self, helper):
        if helper.get_view() == self.window.get_active_view():
            self.get_action().set_state(GLib.Variant.new_boolean(helper.enabled()))

    def on_tab_added(self, window, tab):
        self.add_document_helper(tab.get_view())

    def on_tab_removed(self, window, tab):
        self.remove_document_helper(tab.get_view())

    def on_active_tab_changed(self, window, tab):
        view = tab.get_view()
        helper = self.get_helper(view)

        self.get_action().set_state(GLib.Variant.new_boolean(helper != None and helper.enabled()))

    def activate_toggle(self, action, parameter):
        state = action.get_state()
        action.change_state(GLib.Variant.new_boolean(not state.get_boolean()))

    def multi_edit_mode(self, action, state):
        view = self.window.get_active_view()
        helper = self.get_helper(view)

        active = state.get_boolean()

        if helper != None:
            helper.toggle_multi_edit(active)

        action.set_state(GLib.Variant.new_boolean(active))

# ex:ts=4:et:
