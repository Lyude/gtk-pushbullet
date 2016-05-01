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

import threading

from gi.repository import Notify, GdkPixbuf
from pushbullet.pushbullet import PushBullet
from base64 import b64decode
from threading import Thread

class PushBulletNotification():
    def dismiss(self):
        if self.notification is not None:
            self.notification.disconnect(self.__dismiss_cb_id)
            self.notification.close()

    def __dismiss_cb(self, notification):
        self.pushbullet.dismissEphemeral(self.notification_id,
                                         self.notification_tag,
                                         self.package_name,
                                         self.source_user_iden)
        self.notification_id = None
        self.notification_tag = None
        self.package_name = None
        self.source_user_iden = None
        self.notification = None

    def update(title, body):
        self.notification.update(title, body)

    def __init__(self, push, pushbullet):
        self.pushbullet = pushbullet
        self.notification = Notify.Notification.new(push["title"], push["body"])

        self.notification_id  = push["notification_id"]
        self.package_name     = push["package_name"]
        self.source_user_iden = push["source_user_iden"]

        if "notification_tag" in push:
            self.notification_tag = push["notification_tag"]
        else:
            self.notification_tag = None

        if push["icon"] is not None:
            pbl = GdkPixbuf.PixbufLoader()
            pbl.write(bytes(b64decode(push["icon"])))
            pbl.close()

            self.notification.set_icon_from_pixbuf(pbl.get_pixbuf())

        if push["dismissible"] == True:
            self.__dismiss_cb_id = self.notification.connect_after("closed", self.__dismiss_cb)

        self.notification.set_timeout(0)
        self.notification.set_urgency(Notify.Urgency.LOW)
        self.notification.show()

class EventStreamThread(Thread):
    def __init__(self, pushbullet, config):
        super().__init__()

        self.pushbullet = pushbullet
        self.config = config

        self.notifications = dict()

    def __event_cb(self, data):
        if data["type"] == "push":
            push = data["push"]

            if push["type"] == "mirror":
                if push["notification_id"] in self.notifications:
                    pass # We need to handle this later
                else:
                    self.notifications[push["notification_id"]] = \
                            PushBulletNotification(push, self.pushbullet)

            elif push["type"] == "dismissal":
                try:
                    notification = self.notifications[push["notification_id"]]
                except KeyError:
                    return

                del self.notifications[push["notification_id"]]

                notification.dismiss()

    def run(self):
        self.pushbullet.realtime(self.__event_cb)
