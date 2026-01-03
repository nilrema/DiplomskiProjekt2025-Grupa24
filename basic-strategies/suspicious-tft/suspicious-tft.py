import axelrod as axl

C = axl.Action.C
D = axl.Action.D


def strategy(me, opponent):
    return D if len(me.history) == 0 else opponent.history[-1]