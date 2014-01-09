# -*- coding: utf-8 -*-
#  Join lines plugin
#  This file is part of gedit
#
#  Copyright (C) 2006-2007 Steve Frécinaux, André Homeyer
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

try:
    gettext.bindtextdomain(GETTEXT_PACKAGE, GP_LOCALEDIR)
    _ = lambda s: gettext.dgettext(GETTEXT_PACKAGE, s)
except:
    _ = lambda s: s

class JoinLinesAppActivatable(GObject.Object, Gedit.AppActivatable):
    app = GObject.property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self.app.add_accelerator("<Primary>J", "win.joinlines", None)
        self.app.add_accelerator("<Primary><Shift>J", "win.splitlines", None)

    def do_deactivate(self):
        self.app.remove_accelerator("win.joinlines", None)
        self.app.remove_accelerator("win.splitlines", None)


class JoinLinesWindowActivatable(GObject.Object, Gedit.WindowActivatable):

    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self._insert_menu()

    def do_deactivate(self):
        self._remove_menu()

    def do_update_state(self):
        view = self.window.get_active_view()
        self.window.lookup_action("joinlines").set_enabled(view is not None and \
                                                           view.get_editable())
        self.window.lookup_action("splitlines").set_enabled(view is not None and \
                                                            view.get_editable())

    def _remove_menu(self):
        self.window.remove_action("joinlines")
        self.window.remove_action("splitlines")

    def _insert_menu(self):
        action = Gio.SimpleAction(name="joinlines")
        action.connect('activate', lambda a, p: join_lines(self.window))
        self.window.add_action(action)

        action = Gio.SimpleAction(name="splitlines")
        action.connect('activate', lambda a, p: split_lines(self.window))
        self.window.add_action(action)

        self.menu = self.extend_gear_menu("ext9")

        item = Gio.MenuItem.new(_('_Split Lines'), "win.splitlines")
        self.menu.prepend_menu_item(item)

        item = Gio.MenuItem.new(_("_Join Lines"), "win.joinlines")
        self.menu.prepend_menu_item(item)

def join_lines(window):
    doc = window.get_active_document()
    if doc is None:
        return

    doc.begin_user_action()

    # If there is a selection use it, otherwise join the
    # next line
    try:
        start, end = doc.get_selection_bounds()
    except ValueError:
        start = doc.get_iter_at_mark(doc.get_insert())
        end = start.copy()
        end.forward_line()

    end_mark = doc.create_mark(None, end)

    if not start.ends_line():
        start.forward_to_line_end()

    # Include trailing spaces in the chunk to be removed
    while start.backward_char() and start.get_char() in ('\t', ' '):
        pass
    start.forward_char()

    while doc.get_iter_at_mark(end_mark).compare(start) == 1:
        end = start.copy()
        while end.get_char() in ('\r', '\n', ' ', '\t'):
            end.forward_char()
        doc.delete(start, end)

        doc.insert(start, ' ')
        start.forward_to_line_end()

    doc.delete_mark(end_mark)
    doc.end_user_action()

def split_lines(window):
    view = window.get_active_view()
    if view is None:
        return

    doc = view.get_buffer()

    width = view.get_right_margin_position()
    tabwidth = view.get_tab_width()

    doc.begin_user_action()

    try:
        # get selection bounds
        start, end = doc.get_selection_bounds()

        # measure indent until selection start
        indent_iter = start.copy()
        indent_iter.set_line_offset(0)
        indent = ''
        while indent_iter.get_offset() != start.get_offset():
            if indent_iter.get_char() == '\t':
                indent = indent + '\t'
            else:
                indent = indent + ' '
            indent_iter.forward_char()
    except ValueError:
        # select from start to line end
        start = doc.get_iter_at_mark(doc.get_insert())
        start.set_line_offset(0)
        end = start.copy()
        if not end.ends_line():
            end.forward_to_line_end()

        # measure indent of line
        indent_iter = start.copy()
        indent = ''
        while indent_iter.get_char() in (' ', '\t'):
            indent = indent + indent_iter.get_char()
            indent_iter.forward_char()

    end_mark = doc.create_mark(None, end)

    # ignore first word
    previous_word_end = start.copy()
    forward_to_word_start(previous_word_end)
    forward_to_word_end(previous_word_end)

    while 1:
        current_word_start = previous_word_end.copy()
        forward_to_word_start(current_word_start)

        current_word_end = current_word_start.copy()
        forward_to_word_end(current_word_end)

        if ord(current_word_end.get_char()) and \
           doc.get_iter_at_mark(end_mark).compare(current_word_end) >= 0:

            word_length = current_word_end.get_offset() - \
                          current_word_start.get_offset()

            doc.delete(previous_word_end, current_word_start)

            line_offset = get_line_offset(current_word_start, tabwidth) + word_length
            if line_offset > width - 1:
                doc.insert(current_word_start, '\n' + indent)
            else:
                doc.insert(current_word_start, ' ')

            previous_word_end = current_word_start.copy()
            previous_word_end.forward_chars(word_length)
        else:
            break

    doc.delete_mark(end_mark)
    doc.end_user_action()

def get_line_offset(text_iter, tabwidth):
    offset_iter = text_iter.copy()
    offset_iter.set_line_offset(0)

    line_offset = 0
    while offset_iter.get_offset() < text_iter.get_offset():
        char = offset_iter.get_char()
        if char == '\t':
            line_offset += tabwidth
        else:
            line_offset += 1
        offset_iter.forward_char()

    return line_offset

def forward_to_word_start(text_iter):
    char = text_iter.get_char()
    while ord(char) and (char in (' ', '\t', '\n', '\r')):
        text_iter.forward_char()
        char = text_iter.get_char()

def forward_to_word_end(text_iter):
    char = text_iter.get_char()
    while ord(char) and (not (char in (' ', '\t', '\n', '\r'))):
        text_iter.forward_char()
        char = text_iter.get_char()

# ex:ts=4:et:
