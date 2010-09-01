"""
Display fortunes.

~ C.
"""

import functools
import os.path
import subprocess

from zope.interface import implements
from twisted.internet import defer, reactor
from twisted.plugin import IPlugin
from hackabot.plugin import IHackabotPlugin

class Fortune(object):

    implements(IPlugin, IHackabotPlugin)

    def __init__(self):
        config = hbc.conf.find(".//plugins/fortune")

        if config is None:
            print "The fortune plugin has not been configured!"
            sys.exit();

        self.fortune_dir = config.get("directory")
        self.refresh_cache()
        self.make_commands()

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

    def dispatch(self, conn, event, db=None):
        d = defer.Deferred()
        d.addCallback(self.get_fortune)
        d.addCallback(self.deferred_reply, conn, event)

        reactor.callLater(0, d.callback, db)

    def make_commands(self):
        for f in self.files:
            func = functools.partial(self.dispatch, db=f)
            func.__doc__ = """
                Retrieve a fortune.
                !%s
            """

            setattr(self.__class__, "command_%s" % f, func)

    def command_fortune(self, conn, event):
        """
        Retrieve a fortune.
        !fortune (list | <type>)
        """

        if event["text"] == "list":
            conn.msg(event["reply_to"],
                "Fortunes: %s" % ", ".join(self.files))
        else:
            self.dispatch(conn, event)

    def deferred_reply(self, msg, conn, event):
        lines = msg.replace("\t", "    ").split("\n")
        for line in lines:
            conn.msg(event['reply_to'], line)

fortune = Fortune()
