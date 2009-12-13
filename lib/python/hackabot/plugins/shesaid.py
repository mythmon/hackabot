"""
The eternal retort, or at least this decade's version of it.

~ Corbin Simpson <simpsoco@osuosl.org>
"""

from zope.interface import implements
from twisted.plugin import IPlugin
from hackabot.plugin import IHackabotPlugin

class Ponies(object):
    implements(IPlugin, IHackabotPlugin)

    @staticmethod
    def msg(conn, event):
        if event["sent_by"] == conn.nickname:
            return


        if "it in" in event["text"].lower():
            conn.msg(event["reply_to"], "%s: That's what she said." %
                event["sent_by"])

    me = msg

ponies = Ponies()
