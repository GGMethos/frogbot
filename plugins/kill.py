from util import hook, perm
import re
import random

kills = ["rips off <who>'s <body> and leaves them to die.",
        "grabs <who>'s head and rips it clean off their body.",
        "grabs a machine gun and riddles <who>'s body with bullets.",
        "gags and ties <who> then throws them off a bridge.",
        "crushes <who> with a huge spiked boulder.",
        "rams a rocket launcher up <who>'s ass and lets off a few rounds.",
        "crushes <who>'s skull in with a spiked mace.",
        "feeds <who> to an owlbear.",
        "puts <who> into a sack, throws the sack in the river, and hurls the river into space.",
        "goes bowling with <who>'s head.",
        "sends <who> to /dev/null!",
        "feeds <who> coke and mentos till they pop!",
        "rips apart the atomic bonds that hold <who> together.",
        "rips apart the atomic bonds that hold <who> together.",
        "rips apart the atomic bonds that hold <who> together.",
        "removes <body> from <who> and leaves <who> to bleed out.",
        "removes <body> from <who> and leaves <who> to bleed out.",
        "removes <body> from <who> and leaves <who> to bleed out.",
        "picks up <who> and throws <who> into the sun.",
        "picks up <who> and throws <who> into the sun.",
        "picks up <who> and throws <who> into the sun."
        ]

body = ['head',
        'arms',
        'leg',
        'arm',
        '"special parts"',
        'atomic bonds',
        'atomic bonds',
        'atomic bonds',
        'atomic bonds',
        'atomic bonds',
        'atomic bonds'
        ]

@hook.command
def kill(inp, me = None, nick = None, input=None, notice=None):
    ".kill <user> - kill a user"
    inuserhost = input.user+'@'+input.host
    if inp in input.conn.conf["admins"]: 
        return("I am not killing one of my admins!")
    if perm.isignored(input):
        return None
    inp = inp.strip()

    if not re.match("^[A-Za-z0-9_|.-\]\[]*$", inp.lower()):
        notice("Invalid username!")
        return

    if inp == input.conn.nick.lower() or inp == "itself":
        msg = 'kills ' + nick + ' and rakes their corpse (:3)'
    else:
        kill = random.choice(kills)
        kill = re.sub ('<who>', inp, kill)
        msg = re.sub ('<body>', random.choice(body), kill)

    me(msg)

