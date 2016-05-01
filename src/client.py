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

from client_config import GtkPushBulletConfig

from gi.repository import Notify, GdkPixbuf
from pushbullet.pushbullet import PushBullet
from base64 import b64decode
import sys

def extract_icon(base64_icon):
    pbl = GdkPixbuf.PixbufLoader()
    pbl.write(bytes(b64decode(base64_icon)))
    pbl.close()

    return pbl.get_pixbuf()

def notification_cb(data):
    if data["type"] != "push":
        return

    push = data["push"]
    notification = Notify.Notification.new(push["title"], push["body"])

    if push["icon"] is not None:
        notification.set_icon_from_pixbuf(extract_icon(push["icon"]))

    notification.set_timeout(0)
    notification.set_urgency(Notify.Urgency.LOW)
    notification.show()

config = GtkPushBulletConfig()

if not config.has_option("main", "api_key"):
    sys.stderr.write("Error: api_key is not set\n")
    sys.exit(1)

Notify.init('net.lyude.pushbullet.notifications')
pushbullet = PushBullet(config.get("main", "api_key"))

print("Connected, listening for notifications...")
pushbullet.realtime(notification_cb)
