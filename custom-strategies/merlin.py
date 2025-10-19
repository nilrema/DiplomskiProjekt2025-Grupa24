import axelrod as axl

C = axl.Action.C  # C stands for cooperate
D = axl.Action.D  # D stands for defect


def strategy(me, opponent):
    if not me.history:
        return C

    return opponent.history[-1]
