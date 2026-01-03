import axelrod as axl

C = axl.Action.C
D = axl.Action.D

def strategy(me, opponent):
    myHistory = me.history
    oppHistory = opponent.history

    if len(myHistory) == 0:
        return C
    
    if oppHistory[-1] == C:
        return myHistory[-1]
    elif oppHistory[-1] == D:
        return D if myHistory[-1] == C else C 
    
    
