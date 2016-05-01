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

import gi
gi.require_version("Notify", "0.7")
gi.require_version("Gtk",    "3.0")

from client_config import GtkPushBulletConfig
from event_stream import event_stream

from gi.repository import Notify, GdkPixbuf, Gtk
from pushbullet.pushbullet import PushBullet
from base64 import b64decode
from threading import Thread
import sys

class GtkThread(Thread):
    def run(self):
        Gtk.main()

def register_device():
    if config.has_option("main", "device_iden"):
        return

    r = pushbullet.addDevice("gtk-pushbullet")
    config.set("main", "device_iden", r["iden"])
    config.save()

    print("Registered device 'gtk-pushbullet', iden: " + r["iden"])

config = GtkPushBulletConfig()

if not config.has_option("main", "api_key"):
    sys.stderr.write("Error: api_key is not set\n")
    sys.exit(1)

Notify.init('net.lyude.pushbullet.notifications')
pushbullet = PushBullet(config.get("main", "api_key"))

register_device()

gtk_thread = GtkThread()
gtk_thread.start()

print("Connected, listening for notifications...")
event_stream(pushbullet)
