# -*- coding: utf-8 -*-

#  Copyright (C) 2013 - Garrett Regier
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
#  Foundation, Inc., 59 Temple Place, Suite 330,
#  Boston, MA 02111-1307, USA.

from gi.repository import GLib, GObject, Gio, Gtk, Gedit, Ggit

import weakref


class GitWindowActivatable(GObject.Object, Gedit.WindowActivatable):
    window = GObject.property(type=Gedit.Window)

    windows = weakref.WeakValueDictionary()

    def __init__(self):
        super().__init__()

        Ggit.init()

        self.view_activatables = weakref.WeakSet()

        self.files = {}
        self.monitors = {}

        self.repo = None
        self.tree = None

    @classmethod
    def register_view_activatable(cls, view_activatable):
        window = view_activatable.view.get_toplevel()

        if window not in cls.windows:
            return None

        window_activatable = cls.windows[window]

        window_activatable.view_activatables.add(view_activatable)
        view_activatable.connect('notify::status',
                                 window_activatable.notify_status)

        return window_activatable

    def do_activate(self):
        # self.window is not set until now
        self.windows[self.window] = self

        self.bus = self.window.get_message_bus()

        self.files = {}
        self.file_names = {}
        self.monitors = {}

        self.window_signals = [
            self.window.connect('tab-removed', self.tab_removed),
            self.window.connect('focus-in-event', self.focus_in_event)
        ]

        self.bus_signals = [
            self.bus.connect('/plugins/filebrowser', 'root_changed',
                             self.root_changed, None),
            self.bus.connect('/plugins/filebrowser', 'inserted',
                             self.inserted, None),
            self.bus.connect('/plugins/filebrowser', 'deleted',
                             self.deleted, None)
        ]

        self.refresh();

    def do_deactivate(self):
        self.clear_monitors()

        for sid in self.window_signals:
            self.window.disconnect(sid)

        for sid in self.bus_signals:
            self.bus.disconnect(sid)

        self.files = {}
        self.file_names = {}
        self.repo = None
        self.tree = None
        self.window_signals = []
        self.bus_signals = []

        self.refresh();

    def refresh(self):
        if self.bus.is_registered('/plugins/filebrowser', 'refresh'):
            self.bus.send('/plugins/filebrowser', 'refresh')

    def notify_status(self, view_activatable, psepc):
        location = view_activatable.view.get_buffer().get_location()

        if location is not None:
            self.update_location(location)

    def tab_removed(self, window, tab):
        view = tab.get_view()
        location = view.get_buffer().get_location()

        if location is None:
            return

        # Need to remove the view activatable otherwise update_location()
        # will might use the view's status and not the file's actual status
        for view_activatable in self.view_activatables:
            if view_activatable.view == view:
                self.view_activatables.remove(view_activatable)
                break

        self.update_location(location)

    def focus_in_event(self, window, event):
        for view_activatable in self.view_activatables:
            view_activatable.update()

        for uri in self.files:
            self.update_location(Gio.File.new_for_uri(uri))

    def root_changed(self, bus, msg, data=None):
        self.clear_monitors()

        try:
            repo_file = Ggit.Repository.discover(msg.location)
            self.repo = Ggit.Repository.open(repo_file)
            head = self.repo.get_head()
            commit = self.repo.lookup(head.get_target(), Ggit.Commit.__gtype__)
            self.tree = commit.get_tree()

        except Exception as e:
            self.repo = None
            self.tree = None

        else:
            self.monitor_directory(msg.location)

    def inserted(self, bus, msg, data=None):
        self.files[msg.location.get_uri()] = msg.id
        self.file_names[msg.location.get_uri()] = msg.name

        self.update_location(msg.location)

        if msg.is_directory:
            self.monitor_directory(msg.location)

    def deleted(self, bus, msg, data=None):
        # File browser's deleted signal is broken
        return

        uri = msg.location.get_uri()

        del self.files[uri]
        del self.file_names[uri]

        if uri in self.monitors:
            self.monitors[uri].cancel()
            del self.monitors[uri]

    def update_location(self, location):
        if self.repo is None:
            return

        if location.get_uri() not in self.files:
            return

        status = None

        # First get the status from the open documents
        for view_activatable in self.view_activatables:
            doc_location = view_activatable.view.get_buffer().get_location()

            if doc_location is not None and doc_location.equal(location):
                status = view_activatable.status
                break

        try:
            git_status = self.repo.file_status(location)

        except Exception:
            pass

        else:
            # Don't use the view activatable's
            # status if the file is ignored
            if status is None or git_status & Ggit.StatusFlags.IGNORED:
                status = git_status

        markup = GLib.markup_escape_text(self.file_names[location.get_uri()]) 

        if status is not None:
            if status & Ggit.StatusFlags.INDEX_NEW or \
                    status & Ggit.StatusFlags.WORKING_TREE_NEW or \
                    status & Ggit.StatusFlags.INDEX_MODIFIED or \
                    status & Ggit.StatusFlags.WORKING_TREE_MODIFIED:
                markup = '<span weight="bold">%s</span>' % (markup)

            elif status & Ggit.StatusFlags.INDEX_DELETED or \
                    status & Ggit.StatusFlags.WORKING_TREE_DELETED:
                markup = '<span strikethrough="true">%s</span>' % (markup)

        self.bus.send('/plugins/filebrowser', 'set_markup',
                      id=self.files[location.get_uri()], markup=markup)

    def clear_monitors(self):
        for uri in self.monitors:
            self.monitors[uri].cancel()

        self.monitors = {}

    def monitor_directory(self, location):
        monitor = location.monitor(Gio.FileMonitorFlags.NONE, None)
        self.monitors[location.get_uri()] = monitor

        monitor.connect('changed', self.monitor_changed)

    def monitor_changed(self, monitor, file, other_file, event_type):
        # Only monitor for changes as the file browser will monitor
        # file created and deleted files and emit inserted and deleted
        if event_type == Gio.FileMonitorEvent.CHANGED:
            for f in (file, other_file):
                if f in self.files:
                    self.update_location(f)

# ex:ts=4:et:
