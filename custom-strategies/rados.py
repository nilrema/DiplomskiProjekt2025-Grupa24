import axelrod as axl

C = axl.Action.C  # C stands for cooperate
D = axl.Action.D  # D stands for defect


def strategy(me, opponent):
    myHistory = me.history
    oppHistory = opponent.history
    
    receipt = 5
    numOfC = 0
    numOfD = 0
    for i in range(-1, -receipt - 1, -1):
        if abs(i) > len(oppHistory):
            break
        if oppHistory[i] == axl.Action.C:
            numOfC += 1
        else:
            numOfD += 1

    if numOfD >= numOfC:
        response = axl.Action.D
    else:
        response = axl.Action.C

    return response
