import axelrod as axl

C = axl.Action.C
D = axl.Action.D

def strategy(me, opponent):
    oppHistory = opponent.history
    return D if len(oppHistory) >= 2 and oppHistory[-2] == D and oppHistory[-1] == D else C

