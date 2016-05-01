#!/usr/bin/python3

# Copyright © 2016 Lyude Paul <thatslyude@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import errno
from configparser import ConfigParser

class GtkPushBulletConfig(ConfigParser):
    def __init__(self):
        super().__init__()

        if "XDG_CONFIG_HOME" in os.environ:
            self.path = os.environ["XDG_CONFIG_HOME"] + "/gtk-pushbullet.conf"
        else:
            self.path = os.environ["HOME"] + "/.config/gtk-pushbullet.conf"

        if os.path.exists(self.path):
            self.read(self.path)

    def save(self):
        self.write(open(self.path, "w+"))
