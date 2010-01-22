"""
Tally pizza votes for LUG.

~ C.
"""

import operator
import shelve

from zope.interface import implements
from twisted.plugin import IPlugin
from hackabot.plugin import IHackabotPlugin
from hackabot import log

class Pizza(object):
    implements(IPlugin, IHackabotPlugin)

    def __init__(self):
        self.reset()

    def save(self):
        shelf = shelve.open("pizza")
        toppings_only = dict((i, 0) for i in self.toppings)
        shelf.clear()
        shelf.update(toppings_only)
        shelf.sync()
        shelf.close()

    def reset(self):
        shelf = shelve.open("pizza")
        self.toppings = dict(shelf)
        shelf.close()

    def leaders(self, count):
        # XXX
        return sorted(self.toppings,
            key=lambda x: -self.toppings[x])[:count]

    def command_pizza(self, conn, event):
        """
        Control pizza tallies.
        !pizza [add <topping> | (del|remove) <topping> | list | reset]
        """

        if event["text"].startswith("add"):
            new_topping = event["text"].split(" ", 1)[1].lower()
            self.toppings[new_topping] = 0
        elif event["text"].startswith(("del", "remove")):
            topping_to_del = event["text"].split(" ", 1)[1].lower()
            if topping_to_del in self.toppings:
                del self.toppings[topping_to_del]
                self.save()
        elif event["text"] == "list":
            conn.msg(event["reply_to"],
                "Toppings: %s" % ", ".join(self.toppings))
        elif event["text"] == "reset":
            self.reset()
            conn.msg(event["reply_to"], "Reset tallies!")
        else:
            count = 5
            if event["text"]:
                try:
                    count = int(event["text"])
                except ValueError:
                    pass
            top_toppings = self.leaders(count)
            conn.msg(event["reply_to"], "Top %d:" % count)
            for i, topping in enumerate(top_toppings):
                conn.msg(event["reply_to"], "#%d: %s (%d votes)"
                    % (i + 1, topping, self.toppings[topping]))

    def msg(self, conn, event):
        if event["sent_by"] == conn.nickname:
            return

        message = event["text"].lower()
        for topping in self.toppings:
            if topping in message:
                if "no " + topping in message or "not " + topping in message:
                    log.debug("Decrementing %s" % topping)
                    self.toppings[topping] -= 1
                else:
                    log.debug("Incrementing %s" % topping)
                    self.toppings[topping] += 1

    me = msg

pizza = Pizza()
