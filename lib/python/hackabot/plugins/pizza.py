"""
Tally pizza votes for LUG.

~ C.
"""

import operator

from zope.interface import implements
from twisted.plugin import IPlugin
from hackabot.plugin import IHackabotPlugin
from hackabot import log

toppings = [
    "bacon",
    "green peppers",
    "mushrooms",
    "pepperoni",
]

class Pizza(object):
    implements(IPlugin, IHackabotPlugin)

    def __init__(self):
        self.toppings = {}
        self.reset()

    def reset(self):
        for topping in toppings:
            self.toppings[topping.lower()] = 0

    def leaders(self, count):
        # XXX
        return sorted(self.toppings,
            key=lambda x: -self.toppings[x])[:count]

    def command_pizza(self, conn, event):
        """
        Control pizza tallies.
        !pizza [list | reset]
        """

        if event["text"] == "list":
            conn.msg(event["reply_to"],
                "Toppings: %s" % ", ".join(self.toppings))
        elif event["text"] == "reset":
            self.reset()
            conn.msg(event["reply_to"], "Reset tallies!")
        else:
            top_toppings = self.leaders(5)
            conn.msg(event["reply_to"], "Top 5:")
            for i, topping in enumerate(top_toppings):
                conn.msg(event["reply_to"], "#%d: %s" % (i + 1, topping))

    def msg(self, conn, event):
        if event["sent_by"] == conn.nickname:
            return

        message = event["text"].lower()
        for topping in self.toppings:
            if topping in message:
                log.debug("Incrementing %s" % topping)
                self.toppings[topping] += 1

    me = msg

pizza = Pizza()
