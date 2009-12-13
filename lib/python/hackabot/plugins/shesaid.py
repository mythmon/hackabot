"""
The eternal retort, or at least this decade's version of it.

~ Corbin Simpson <simpsoco@osuosl.org>
"""

import re

from zope.interface import implements
from twisted.plugin import IPlugin
from hackabot.plugin import IHackabotPlugin

class SheSaid(object):
    implements(IPlugin, IHackabotPlugin)

    def __init__(self):
        self.regex = re.compile("(?:^|\s)(?:it in|need(?:ed)? it)", re.I)

    def msg(self, conn, event):
        if event["sent_by"] == conn.nickname:
            return

        if self.regex.search(event["text"]):
            conn.msg(event["reply_to"], "%s: That's what she said." %
                event["sent_by"])

    me = msg

shesaid = SheSaid()
