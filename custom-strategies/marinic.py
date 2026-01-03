import axelrod as axl

C = axl.Action.C
D = axl.Action.D

def strategy(me, opponent):
    oppHistory = opponent.history
    return C if len(oppHistory) >= 3 and oppHistory[-3] == C and oppHistory[-2] == C and oppHistory[-1] == C else D

