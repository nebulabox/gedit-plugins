# -*- coding: utf-8 -*-
#
# Copyright (©) 2012 Gustavo Noronha Silva (gns@gnome.org)
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import sys

from gi.repository import GtkSource, Gdk, GObject


# This is to allow running this file stand-alone, for running tests.
# This crazy file descriptor handling is to supress the gir error message.
dup = os.dup(2)
os.close(2)
os.open('/dev/null', os.O_RDWR)

try:
    from gi.repository import Gedit
except ImportError:
    class Gedit(object):
        class ViewActivatable:
            pass
        class View(GObject.Object):
            pass
finally:
    os.close(2)
    os.dup(dup)
    os.close(dup)


class EmacsyIndenterBase(object):
    not_space_re = re.compile('[^\s]')


    def __init__(self, plugin):
        self.plugin = plugin
        self.view = plugin.view
        self.buffer = plugin.buffer


    def is_electric(self, text):
            return False


    def indent_line(self, line):
        if line.get_line() == 0:
            return True

        previous_line = self.get_previous_line(line)
        if self.line_ends_with(previous_line, ','):
            self.indent_aligned_with_open_paren(line)
            return True

        return False


    def indent_aligned_with_open_paren(self, line):
        previous_line = self.get_previous_line(line)
        open_paren_line, position = self.find_unbalanced_bracket_line(line)

        level = position / self.view.get_tab_width()
        left_over_spaces = position % self.view.get_tab_width()

        self.set_indent_level_on_line(line, level, left_over_spaces)


    def get_text_for_line(self, line):
        end = line.copy()
        if end.get_char() != '\n':
            end.forward_to_line_end()
        return line.get_visible_text(end)


    def get_previous_line(self, line):
        if line.get_line() == 0:
            return None

        return self.buffer.get_iter_at_line(line.get_line() - 1)


    def get_line_end(self, line):
        end = line.copy()
        if end.get_char() != '\n':
            end.forward_to_line_end()
        return end


    def get_cursor_line(self):
        cursor_offset = self.buffer.get_property('cursor-position')
        cursor = self.buffer.get_iter_at_offset(cursor_offset)
        return self.buffer.get_iter_at_line(cursor.get_line())


    def line_starts_with(self, line, prefix):
        text = self.get_text_for_line(line).lstrip()
        return text.startswith(prefix)


    def line_ends_with(self, line, suffix):
        text = self.get_text_for_line(line).rstrip()
        return text.endswith(suffix)


    def find_unbalanced_bracket_line(self, line, open_bracket = '(', close_bracket = ')'):
        unbalanced = 0
        position = -1

        while True:
            previous = line.copy()
            while previous.backward_line() and previous.get_char() == '\n':
                pass

            line = previous
            text = self.get_text_for_line(line)

            # We always use spaces to calculate indentation levels.
            text = text.replace('\t', ' ' * self.view.get_tab_width())
            for i in range(len(text), 0, -1):
                if text[i - 1] == close_bracket:
                    unbalanced = unbalanced + 1
                elif text[i - 1] == open_bracket:
                    unbalanced = unbalanced - 1

                    if unbalanced == -1:
                        position = i
                        break

            if line.get_line() == 0 or position != -1:
                break

        if unbalanced != -1:
            return None, 0

        return line, position


    def find_open_bracket_line(self, line, open_bracket = '(', close_bracket = ')'):
        unbalanced = 0

        def _find_brackets_in_line(line, unbalanced):
            text = self.get_text_for_line(line)
            for i in range(len(text), 0, -1):
                if text[i - 1] == close_bracket:
                    unbalanced = unbalanced + 1
                elif text[i - 1] == open_bracket:
                    unbalanced = unbalanced - 1

                    if not unbalanced:
                        break

            return unbalanced

        unbalanced = _find_brackets_in_line(line, unbalanced)
        while True:
            previous = line.copy()
            while previous.backward_line() and previous.get_char() == '\n':
                pass

            line = previous

            unbalanced = _find_brackets_in_line(line, unbalanced)

            if line.get_line() == 0 or not unbalanced:
                break

        return line


    def get_indentation_for_line(self, line):
        text = self.get_text_for_line(line)

        # We use only spaces for finding out the indentation level.
        text = text.replace('\t', ' ' * self.view.get_tab_width())
        match = self.not_space_re.search(text)

        if not match:
            return len(text.strip('\n'))

        return match.start()


    def set_indent_level_on_line(self, line, level, left_over_spaces = 0):
        use_tabs = not self.view.get_insert_spaces_instead_of_tabs()

        if use_tabs:
            indentation = '\t' * level
        else:
            tab_width = self.view.get_tab_width()
            indentation = ' ' * tab_width * level

        # Add any left over spaces, required for aligning arguments with their
        # parens, usually.
        indentation = indentation + ' ' * left_over_spaces

        # First let's check for existing indentation.
        began_action = False
        cursor_line = self.get_cursor_line()
        self.buffer.begin_user_action()
        if cursor_line.get_char() != '\n':
            current_contents = self.get_text_for_line(cursor_line).strip('\n')
            match = self.not_space_re.search(current_contents)

            # If we have a match, the line already has contents in it, we'll
            # find out if the indentation already exists and remove incorrect
            # one if necessary.
            if match:
                end = cursor_line.copy()
                end.forward_chars(match.start())
                self.buffer.delete(cursor_line, end)
            else:
                self.buffer.delete(cursor_line, self.get_line_end(cursor_line))

        self.buffer.insert(self.get_cursor_line(), indentation)

        self.buffer.end_user_action()



class EmacsyIndenterC(EmacsyIndenterBase):
    def is_electric(self, text):
        if text == '\n' or text == '}' or text == '{':
            return True
        return False


    def indent_line(self, line):
        if EmacsyIndenterBase.indent_line(self, line):
            return True

        text = self.get_text_for_line(line)

        # A curly brace at the beginning of the line is opening a new block or
        # closing the open block, so indent at the parent block level.
        if text.lstrip().startswith('}') or text.lstrip().startswith('{'):
            self.indent_at_parent_level(line)
            return True

        level = self.get_level_for_line(line)
        self.set_indent_level_on_line(line, level)

        return True


    def indent_at_parent_level(self, line):
        level = self.get_level_for_line(line)
        level = max(0, level - 1)

        self.set_indent_level_on_line(line, level)


    def get_level_for_line(self, line):
        previous_line = self.get_previous_line(line)

        # This should deal with single-statement control structures.
        if self.line_ends_with(previous_line, ')'):
            open_paren_line = self.find_open_bracket_line(line)

            # We get the level for the open paren line, and add one, since this
            # is the one-line block.
            return self.get_level_for_line(open_paren_line) + 1

        open_block_line, position = self.find_unbalanced_bracket_line(line, '{', '}')
        if not open_block_line:
            return 0

        # We have the indentation level for the unbalanced open bracket, now
        # add one, since we are indenting a child.
        tab_width = self.view.get_tab_width()
        indentation = self.get_indentation_for_line(open_block_line)

        level = (indentation / tab_width) + 1

        return level


class EmacsyIndenterPython(EmacsyIndenterBase):
    def is_electric(self, text):
        if text == '\n':
            return True
        return False


    def get_text_for_line(self, line):
        text = EmacsyIndenterBase.get_text_for_line(self, line)
        if not '#' in text:
            return text

        return text.split('#', 1)[0]


    def indent_line(self, line):
        if EmacsyIndenterBase.indent_line(self, line):
            return True

        level = self.get_level_for_line(line)
        self.set_indent_level_on_line(line, level)
        return True

    def get_level_for_line(self, line):
        # Track if there are lines with lower indentation between the : we find
        # and the current one.
        lowest_indentation = -1

        while True:
            line = self.get_previous_line(line)

            if self.line_ends_with(line, ':'):
                indentation = self.get_indentation_for_line(line)

                # Yep, this should be the one we're looking for!
                if lowest_indentation == -1 or indentation < lowest_indentation:
                    break

                indentation = lowest_indentation
            elif line.get_char() != '\n':
                # We found a line that's not a block, let's see if it has lower
                # indentation than what we found so far.
                if self.get_indentation_for_line(line) < lowest_indentation or lowest_indentation == -1:
                    lowest_indentation = self.get_indentation_for_line(line)

            if line.get_line() == 0:
                # We hit the beginning, which means we are at indent level 0.
                return 0

        # We have the indentation level for the unbalanced open bracket, now
        # add one, since we are indenting a child.
        tab_width = self.view.get_tab_width()
        level = (indentation / tab_width) + 1

        return level


class EmacsyIndentBase(object):
    def do_activate(self):
        self.buffer = self.view.get_buffer()
        self.language_id = self.buffer.connect('notify::language', self._language_changed_cb)

        language = self.get_language_name()
        if not language:
            return

        if language != 'Python' and language != 'C' and language != 'C++':
            return

        self.wire_up(self.get_language_name())


    def do_deactivate(self):
        self.buffer.handler_disconnect(self.language_id)
        self.tear_down()


    def do_update_state(self):
        pass


    def wire_up(self, language):
        self.key_press_id = self.view.connect('key-press-event', self._key_press_event_cb)
        self.key_release_id = self.view.connect('key-release-event', self._key_release_event_cb)

        self.insert_text_id = self.buffer.connect_after('insert-text', self._text_inserted_cb)

        if language == 'Python':
            self.indenter = EmacsyIndenterPython(self)
        else:
            self.indenter = EmacsyIndenterC(self)

    def tear_down(self):
        if getattr(self, 'key_press_id', None):
            self.view.handler_disconnect(self.key_press_id)

        if getattr(self, 'key_release_id', None):
            self.view.handler_disconnect(self.key_release_id)

        if getattr(self, 'insert_text_id', None):
            self.buffer.handler_disconnect(self.insert_text_id)


    def _language_changed_cb(self, *args):
        language = self.get_language_name()

        self.tear_down()
        if language == 'Python' or language == 'C':
            self.wire_up(language)


    def _key_press_event_cb(self, view, event):
        # FIXME: need to decide whether to indent the selection when tab is
        # pressed
        if self.buffer.get_has_selection():
            return False

        # We do not check for 0 here because some systems have modifiers like
        # numlock or capslock on.
        if 'GDK_SHIFT_MASK' in event.state.value_names:
            return False

        if event.get_keyval()[1] != Gdk.KEY_Tab:
            return False

        self.indent_line(self.indenter.get_cursor_line())
        return True


    def _key_release_event_cb(self, view, event):
        # FIXME: see _key_press_event_cb
        if self.buffer.get_has_selection():
            return False

        if event.get_keyval()[1] != Gdk.KEY_Tab or event.state != 0:
            return False

        return True


    def _text_inserted_cb(self, buffer, location, text, length):
        if not self.indenter.is_electric(text):
            return

        line = self.buffer.get_iter_at_line(location.get_line())
        self.indent_line(line)

        # Revalidate the location.
        cursor_offset = self.buffer.get_property('cursor-position')
        location.assign(self.buffer.get_iter_at_offset(cursor_offset))


    def indent_line(self, line):
        if line.get_line() == 0:
            return

        self.indenter.indent_line(line)


class EmacsyIndentTest(EmacsyIndentBase):
    def __init__(self):
        self.view = GtkSource.View()
        self.language = 'Python'
        self.do_activate()


    def get_language_name(self):
        return self.language


    def run_test(self, name):
        sys.stdout.write('Running test %s: ' % (name))

        if name.startswith('python'):
            self.language = 'Python'
            self.indenter = EmacsyIndenterPython(self)
        else:
            self.language = 'C'
            self.indenter = EmacsyIndenterC(self)

        self.view.set_insert_spaces_instead_of_tabs(True)
        self.view.set_tab_width(4)

        self.cleanup()
        self.type_file_into_buffer(name)
        self.check_result(name)

        sys.stdout.write('Running test %s (tabs): ' % (name))

        self.view.set_tab_width(8)
        self.view.set_insert_spaces_instead_of_tabs(False)

        self.cleanup()
        self.type_file_into_buffer(name)
        self.check_result(name)


    def cleanup(self):
        self.buffer.set_text('')


    def type_file_into_buffer(self, name):
        if self.view.get_insert_spaces_instead_of_tabs():
            backspaces = 4
        else:
            backspaces = 1

        contents = open('tests/' + name + '.input').read()
        for char in unicode(contents):
            if char == '←':
                for i in range(backspaces):
                    cursor_offset = self.buffer.get_property('cursor-position')
                    cursor = self.buffer.get_iter_at_offset(cursor_offset)
                    self.buffer.backspace(cursor, True, True)
            elif char == '«':
                cursor_line = self.indenter.get_cursor_line()
                end = cursor_line.copy()
                end.forward_chars(backspaces)
                self.buffer.delete(cursor_line, end)
            else:
                self.buffer.insert_at_cursor(char)

        # Saving the expected file adds a final newline to the file, in my
        # Gedit setup.
        cursor_line = self.indenter.get_cursor_line()
        end = self.buffer.get_end_iter()
        self.buffer.delete(cursor_line, end)


    def check_result(self, name):
        if self.view.get_insert_spaces_instead_of_tabs():
            contents = open('tests/' + name + '.expected').read()
        else:
            contents = open('tests/' + name + '-tabs.expected').read()

        start = self.buffer.get_start_iter()
        end = self.buffer.get_end_iter()
        result = start.get_visible_text(end)

        if contents == result:
            print 'PASSED'
            return

        if self.view.get_insert_spaces_instead_of_tabs():
            open('tests/' + name + '.actual', 'w').write(result)
        else:
            open('tests/' + name + '-tabs.actual', 'w').write(result)

        print 'FAILED'

        print 'Expected:'
        for line in contents.split('\n'):
            print '\t' + line

        print 'Got:'
        for line in result.split('\n'):
            print '\t' + line


class EmacsyIndent(GObject.Object, EmacsyIndentBase, Gedit.ViewActivatable):
    __gtype_name__ = "EmacsyIndent"
    view = GObject.property(type = Gedit.View)


    def do_activate(self):
        EmacsyIndentBase.do_activate(self)


    def do_deactivate(self):
        EmacsyIndentBase.do_deactivate(self)


    def do_update_state(self):
        EmacsyIndentBase.do_update_state(self)


    def get_language_name(self):
        language = self.view.get_buffer().get_language()
        if not language:
            return None
        return language.get_name()


if __name__ == '__main__':
    tester = EmacsyIndentTest()

    if len(sys.argv) > 1:
        for name in sys.argv[1:]:
            tester.run_test(name)
        sys.exit(0)

    tests = os.listdir('./tests')
    tests.sort()
    for filename in tests:
        if filename.endswith('.input'):
            tester.run_test(filename.split('.')[0])

