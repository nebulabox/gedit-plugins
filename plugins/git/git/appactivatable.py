# -*- coding: utf-8 -*-

#  Copyright (C) 2014 - Garrett Regier
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

from gi.repository import GLib, GObject, Gio, Gedit, Ggit


class GitAppActivatable(GObject.Object, Gedit.AppActivatable):
    app = GObject.property(type=Gedit.App)

    __instance = None

    def __init__(self):
        super().__init__()

        Ggit.init()

        GitAppActivatable.__instance = self

    def do_activate(self):
        self.__repos = {}

    def do_deactivate(self):
        self.__repos = None

    @classmethod
    def get_instance(cls):
        return cls.__instance

    def clear_repositories(self):
        self.__repos = {}

    def get_repository(self, location, is_dir):
        dir_location = location if is_dir else location.get_parent()
        dir_uri = dir_location.get_uri()

        # Fast Path
        try:
            return self.__repos[dir_uri]

        except KeyError:
            pass

        # Doing remote operations is too slow
        if not location.has_uri_scheme('file'):
            return None

        # Must check every dir, otherwise submodules will have issues
        try:
            repo_file = Ggit.Repository.discover(location)

        except GLib.Error:
            # Prevent trying to find a git repository
            # for every file in this directory
            self.__repos[dir_uri] = None
            return None

        repo_uri = repo_file.get_parent().get_uri()

        # Reuse the repo if requested multiple times
        try:
            repo = self.__repos[repo_uri]

        except KeyError:
            repo = Ggit.Repository.open(repo_file)
            repo_workdir_uri = repo.get_workdir().get_uri()

            # TODO: this was around even when not used, on purpose?
            head = repo.get_head()
            commit = repo.lookup(head.get_target(), Ggit.Commit.__gtype__)
            tree = commit.get_tree()

            self.__repos[repo_uri] = repo
            self.__repos[repo_workdir_uri] = repo

        else:
            repo_workdir_uri = repo.get_workdir().get_uri()

        # Avoid trouble with symbolic links
        while dir_uri.startswith(repo_workdir_uri):
            self.__repos[dir_uri] = repo

            dir_location = dir_location.get_parent()
            dir_uri = dir_location.get_uri()

        return repo

# ex:ts=4:et:
