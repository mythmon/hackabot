"""
Display fortunes.

~ C.
"""

import os.path
import subprocess

from zope.interface import implements
from twisted.internet import defer, reactor
from twisted.plugin import IPlugin
from hackabot.plugin import IHackabotPlugin

class Fortune(object):

    implements(IPlugin, IHackabotPlugin)

    def __init__(self):
        self.fortune_dir = "/home/simpson/hackabot/misc/cookies"
        self.refresh_cache()

    def refresh_cache(self):
        l = os.listdir(self.fortune_dir)
        self.files = [i for i in l if i + ".dat" in l and
            os.path.isfile(os.path.join(self.fortune_dir, i))]

    def get_fortune(self, db):
        cmd = ["fortune"]
        if db and db in self.files:
            cmd.append(os.path.join(self.fortune_dir, db))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        fortune, chaff = p.communicate()
        return fortune

    def command_fortune(self, conn, event):
        """
        Retrieve a fortune.
        !fortune (list | <type>)
        """

        d = defer.Deferred()
        d.addCallback(self.get_fortune)
        d.addCallback(self.deferred_reply, conn, event)

        reactor.callLater(0, d.callback, None)

    def deferred_reply(self, msg, conn, event):
        lines = msg.replace("\t", "    ").split("\n")
        for line in lines:
            conn.msg(event['reply_to'], line)

fortune = Fortune()
