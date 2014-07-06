# -*- coding: utf-8 -*-
#  RPM ChangeLog plugin
#  This file is part of gedit
#
#  Copyright (C) 2014 Igor Gnatenko
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

from gi.repository import GObject, Gio, Gtk, Gedit
import gettext
from gpdefs import *
from datetime import datetime

try:
    gettext.bindtextdomain(GETTEXT_PACKAGE, GP_LOCALEDIR)
    _ = lambda s: gettext.dgettext(GETTEXT_PACKAGE, s)
except:
    _ = lambda s: s

class RPMChangeLogAppActivatable(GObject.Object, Gedit.AppActivatable):
    app = GObject.property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)
        self.settings = Gio.Settings.new("org.gnome.gedit.plugins.rpmchangelog")

    def do_activate(self):
        self.app.add_accelerator(self.settings.get_string("hotkey"), "win.addchangelogentry", None)

    def do_deactivate(self):
        self.app.remove_accelerator("win.addchangelogentry", None)


class RPMChangeLogWindowActivatable(GObject.Object, Gedit.WindowActivatable):
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        action = Gio.SimpleAction(name="addchangelogentry")
        action.connect('activate', lambda a, p: self.add_changelog_entry())
        self.window.add_action(action)

    def do_deactivate(self):
        self.window.remove_action("addchangelogentry")

    def do_update_state(self):
        view = self.window.get_active_view()
        self.window.lookup_action("addchangelogentry").set_enabled(
                view is not None and view.get_editable())

    def add_changelog_entry(self):
        view = self.window.get_active_view()
        if view and hasattr(view, "rpm_changelog_view_activatable"):
            view.rpm_changelog_view_activatable.add_changelog_entry()

class RPMChangeLogViewActivatable(GObject.Object, Gedit.ViewActivatable):
    view = GObject.property(type=Gedit.View)

    def __init__(self):
        GObject.Object.__init__(self)
        self.settings = Gio.Settings.new("org.gnome.gedit.plugins.rpmchangelog")

    def do_activate(self):
        self.view.rpm_changelog_view_activatable = self
        self.view.connect('populate-popup', self.populate_popup)
        self.username = self.settings.get_string("username")
        self.email = self.settings.get_string("email")

    def do_deactivate(self):
        delattr(self.view, "rpm_changelog_view_activatable")

    def populate_popup(self, view, popup):
        if not isinstance(popup, Gtk.MenuShell):
            return

        item = Gtk.SeparatorMenuItem()
        item.show()
        popup.append(item)

        item = Gtk.MenuItem.new_with_mnemonic(_("Add _ChangeLog Entry"))
        item.set_sensitive(self.view.get_editable())
        item.show()
        item.connect('activate', lambda i: self.add_changelog_entry())
        popup.append(item)

    def _get_val(self, start):
        stop = start.copy()
        stop.forward_to_line_end()
        while not start.get_char() in (' ', '\t'):
            start.forward_char()
        while start.get_char() in (' ', '\t'):
            start.forward_char()
        return start.get_text(stop)

    def add_changelog_entry(self):
        doc = self.view.get_buffer()
        if doc is None:
            return

        doc.begin_user_action()

        start_iter = doc.get_start_iter()
        end_iter = doc.get_end_iter()
        start_mark = doc.create_mark(None, start_iter)
        end_mark = doc.create_mark(None, end_iter)

        version = doc.get_iter_at_mark(start_mark).forward_search("Version:", 0, None)
        if version:
            start, stop = version
        else:
            return
        version_str = self._get_val(start)

        release = doc.get_iter_at_mark(start_mark).forward_search("Release:", 0, None)
        if release:
            start, stop = release
        else:
            return
        release_str = self._get_val(start)
        release_str = release_str.replace("%{?dist}", "")

        changelog = doc.get_iter_at_mark(start_mark).forward_search("%changelog", 0, None)
        if changelog:
            start, stop = changelog
        else:
            stop = end_iter.copy()
            stop.backward_char()
            if stop.get_char() != '\n':
                stop.forward_char()
                doc.insert(stop, "\n", -1)
            else:
                stop.forward_char()
            doc.insert(stop, "\n%changelog", -1)
        d = datetime.utcnow().strftime("%a %b %d %Y")
        str_ins = "\n* {} {} <{}> - {}-{}".format(d, self.username, self.email, version_str, release_str)
        doc.insert(stop, str_ins, -1)
        doc.insert(stop, "\n- ", -1)
        cursor = stop.copy()
        cursor.forward_to_line_end()
        stop.forward_char()
        if stop.get_char() != '\n':
            stop.backward_char()
            doc.insert(stop, "\n", -1)


        doc.end_user_action()
        doc.place_cursor(cursor)

# ex:ts=4:et:
