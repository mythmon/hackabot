"""
Reach out and ping somebody.

~ Corbin Simpson <simpsoco@osuosl.org>
"""

import re

from zope.interface import implements
from twisted.plugin import IPlugin
from hackabot.plugin import IHackabotPlugin
from hackabot import log

from twisted.internet.utils import getProcessOutputAndValue

class Ping(object):
    implements(IPlugin, IHackabotPlugin)

    def __init__(self):
        self.regex = re.compile(r"bytes from (\S+) \(([\d\.]*)\).*time=([\d\.]* ms)", re.M)

    def command_ping(self, conn, event):
        """
        Reach out and ping somebody! Pings a remote server.
        !ping <server>
        """

        server = event["text"].split()[0]
        if not server:
            conn.msg(event["reply_to"], "Which server should I ping?")
            return

        args = ("-c", "1", "-W", "2", server)

        d = getProcessOutputAndValue("/bin/ping", args)
        d.addCallback(self.handle_ping, conn, event)

    def handle_ping(self, out_err_code, conn, event):
        out, err, code = out_err_code
        if code == 0:
            server, ip, time = self.regex.search(out).groups()
            conn.msg(event["reply_to"], "%s [%s] is up: %s" % (server, ip, time))
        elif code == 1:
            conn.msg(event["reply_to"], "No response from the server.")
        elif code == 2:
            conn.msg(event["reply_to"], "Unknown server.")
        else:
            conn.msg(event["reply_to"], "Unknown error value %d, sorry." % code)

ping = Ping()
